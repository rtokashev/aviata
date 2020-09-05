import redis
import json
import datetime
import os

from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest

redis_host = os.environ.get("REDIS_HOST", '127.0.0.1')
redis_port = os.environ.get("REDIS_PORT", '6379')
cache = redis.Redis(host=redis_host, port=redis_port, db=1)


def to_human_readable(flights_list: list):
    result = []

    flight: dict
    for flight in flights_list:
        dtime = flight.get("flights")[0].get("dtime")
        src_city = flight.get("flights")[0].get("src_name")
        src_station = flight.get("flights")[0].get("src_station")

        if len(flight.get("flights")) > 1:
            atime = flight.get("flights")[len(flight.get("flights")) - 1].get("atime")
            dst_city = flight.get("flights")[len(flight.get("flights")) - 1].get("dst_name")
            dst_station = flight.get("flights")[len(flight.get("flights")) - 1].get("dst_station")
            direct = False
        else:
            direct = True
            dst_city = flight.get("flights")[0].get("dst_name")
            dst_station = flight.get("flights")[0].get("dst_station")
            atime = flight.get("flights")[0].get("atime")

        result.append(
            dict(
                airline=flight.get("flights")[0].get("operating_airline").get("name"),
                airline_url=flight.get("flights")[0].get("airline").get("url"),
                src_city=src_city,
                dst_city=dst_city,
                src_airport=src_station,
                dst_airport=dst_station,
                dtime=datetime.datetime.strftime(datetime.datetime.fromtimestamp(dtime), "%d/%m/%Y %H:%M:%S"),
                atime=datetime.datetime.strftime(datetime.datetime.fromtimestamp(atime), "%d/%m/%Y %H:%M:%S"),
                flight_time=str(datetime.timedelta(seconds=(atime - dtime))),
                direct=direct,
                price_change=flight.get("price_change"),
                price=f'{flight.get("conversion").get("amount")} {flight.get("conversion").get("currency")}'
            )
        )
    result = sorted(result, key=lambda flight_: flight_["price"])
    return result


def index(_: WSGIRequest):
    return JsonResponse(
        data={"info": "API для получения самых дешёвых билетов на месяц вперёд"}, safe=False, status=402
    )


def skypicker_flights_search(request: WSGIRequest) -> JsonResponse:
    fly_from = request.GET.get("fly_from")
    fly_to = request.GET.get("fly_to")
    if not fly_from or not fly_to:
        return JsonResponse(data={"error": "Missed required parameters - [fly_from, fly_to]"}, status=400)
    direction = f'{fly_from}-{fly_to}'
    if cache.exists(direction):
        return JsonResponse(data=to_human_readable(json.loads(cache.get(direction))), safe=False)
    return JsonResponse(data={"data": f"flights for {fly_from}-{fly_to} direction no in the cache"}, safe=False)
