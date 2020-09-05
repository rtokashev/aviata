import datetime
import os
import json
import time

import redis

from client.searcher.searcher import Searcher
from client.checker.checker import Checker
from client.remote_api.skypicker import SkyPickerFlightsSearcher, SkyPickerFlightsChecker
from queries import directions


ALL_FLIGHTS = "all_flights"  # key for 0 Redis index , for storing all found flights for whole month(unchecked)

redis_host = os.environ.get("REDIS_HOST", '127.0.0.1')
redis_port = os.environ.get("REDIS_PORT", '6379')
refresh_timeout = os.environ.get("REFRESH_TIMEOUT", 60)

all_flights_cache = redis.Redis(host=redis_host, port=redis_port, db=0)
checked_flights_cache = redis.Redis(host=redis_host, port=redis_port, db=1)


def get_seconds_until_end_of_day() -> int:
    today = datetime.datetime.now()
    tomorrow = today + datetime.timedelta(days=1)
    seconds = (datetime.datetime.combine(tomorrow, datetime.time.min) - today).seconds
    return seconds


def main():
    searcher = Searcher(remote_api_client=SkyPickerFlightsSearcher())
    checker = Checker(remote_api_client=SkyPickerFlightsChecker())

    # Sorry for this
    while True:
        cache_timeout = get_seconds_until_end_of_day()

        if all_flights_cache.exists(ALL_FLIGHTS):
            all_flights = json.loads(all_flights_cache.get(ALL_FLIGHTS))
        else:
            all_flights = searcher.search(directions=directions)
            if all_flights:
                all_flights_cache.set(ALL_FLIGHTS, json.dumps(all_flights), ex=cache_timeout)
            else:
                print("Some error happened")
                exit(1)

        valid_flights = checker.check(all_flights)

        if valid_flights:
            batch = {}
            for valid_flight in valid_flights:
                direction = valid_flight.get("route")[0] + '-' + valid_flight.get("route")[1]
                if direction not in batch:
                    batch[direction] = []
                batch[direction].append(valid_flight)

            for key, value in batch.items():
                checked_flights_cache.set(key, json.dumps(value))

        time.sleep(refresh_timeout)


if __name__ == '__main__':
    main()
