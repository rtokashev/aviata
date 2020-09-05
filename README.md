**Low price calendar for air travel**
----
  Returns a json list of flights with the cheapest price for each day, from the current day one month ahead. <br />
  The source is the REST-API kiwi.com - https://api.skypicker.com. 
  
* **URL**
    
  /skypicker

* **Method:**
  
  `GET` 
  
*  **URL Params**

   **Required:**

   `fly_from=[string]`
   `fly_to=[string]`
   
    Available directions, where VKO=MOW, TSE=NQZ: <br />
     in format fly_from-fly_to
     
     `"CIT-ALA"` <br />
     `"ALA-NQZ"` <br />
     `"ALA-CIT"` <br />
     `"NQZ-VKO"` <br />
     `"VKO-NQZ"` <br />
     `"VKO-ALA"` <br />
     `"LED-NQZ"` <br />
     `"NQZ-LED"` <br />
     `"ALA-VKO"` <br />
     `"NQZ-ALA"` <br />

* **Flights object fields data types** <br />
  `airline` - string <br />
  `airline_url` - string <br />
  `src_city` - string <br />
  `dst_city` -  string <br />
  `src_airport` - string <br />
  `dst_airport` - string <br />
  `dtime` - datetime, "%d/%m/%Y %H:%M:%S" <br />
  `atime` - datetime, "%d/%m/%Y %H:%M:%S" <br />
  `flight_time` - string <br />
  `direct` - boolean <br />
  `price_change` - boolean <br />
  `price` - string (float + str) <br />
  
* **Flight object fields definitions:** <br />
  `airline` - airline company name <br />
  `airline_url` - airline company web-site, if exists <br />
  `src_city` - the same as GET fly_from parameter <br />
  `dst_city` -  the same as GET fly_to parameter <br />
  `src_airport` - departure airport <br />
  `dst_airport` - arrival airport <br />
  `dtime` - departure time <br />
  `atime` - arrival time <br />
  `flight_time` - total flight time, in format days:hours:minutes <br />
  `direct` - if direct flight is equal True or if with transfers is equal False <br />
  `price_change` - if price has changed is equal True else False <br />
  `price` - flight price, by default in KZT <br />
  
  
* **Success Response:**
  
  * **Code:** 200 <br />
    **Content:**  
    ```json
    [
      {
        "airline": "FlyArystan",
        "airline_url": "https://flyarystan.com/en/Home",
        "src_city": "Almaty",
        "dst_city": "Nur-Sultan",
        "src_airport": "Almaty International",
        "dst_airport": "Nursultan Nazarbayev International Airport",
        "dtime": "01/10/2020 16:25:00",
        "atime": "01/10/2020 18:00:00",
        "flight_time": "1:35:00",
        "direct": true,
        "price_change": false,
        "price": "14041.04 KZT"
      },
      {
        "airline": "FlyArystan",
        "airline_url": "https://flyarystan.com/en/Home",
        "src_city": "Almaty",
        "dst_city": "Nur-Sultan",
        "src_airport": "Almaty International",
        "dst_airport": "Nursultan Nazarbayev International Airport",
        "dtime": "06/10/2020 16:25:00",
        "atime": "06/10/2020 18:00:00",
        "flight_time": "1:35:00",
        "direct": true,
        "price_change": false,
        "price": "14041.04 KZT"
      }
    ]

 
  * **Code:** 200 <br />
    **Content:**
    ```json
    {"data": "flights for ALA-UID direction no in the cache"}
    ```
* **Error Response:**
  * **Code:** 400 <br />
    **Content:**
    ```json
    {"error": "Missed required parameters - [fly_from, fly_to]"}
    ```

* **Dev Notes:** <br />
  **Services** <br/>
  
  * `api` - Django REST-API <br>
  * `redis` - Redis Cache Server <br>
  * `crawler` - Custom client for requesting remote flights API, such as https://api.skypicker.com <br />
  
  **Logic**
  * The REST API only reads data from 1 Redis index which is updated by a crawler service requesting available flights per
   month from a remote API like https://api.skypicker.com. <br />
  * All available flights per month are collected by the crawler once a day and recorded in the 0 Redis index. <br />
  * The crawler periodically checks all cached flights for validity via https://api.skypicker.com/api/v0.1/check_flights
   and updates 1 Redis index with valid flights. <br />
  * The cache of all available flights is cleared after 00:00 and the crawler, having not found any cached flights for a 
  month, again initiates a request to receive a list of flights a month ahead of the current day. <br/>
  
  **How to run** <br />
  * Download the project
  * Make sure you have prerequisites
  
  **Prerequisites** <br />
  * `docker version >= 19`
  * `docker-compose version >= 1.26 `
  
  **Definitions of .env variables** <br />
  * `REDIS_HOST` - redis ip addr
  * `REDIS_PORT` - redis available port
  * `REFRESH_TIMEOUT` - the parameter for the crawler service, for refresh all valid flights
  
  **Run in docker-compose** <br />
  
  `docker-compose up --bu -d` - No need any optional arguments
  
  **Local run** <br />
  If no docker, but have local Redis Cache Server. <br />
  Follow this steps(For Linux only). <br />
  
  In th terminal(bash) execute this
  * `export REDIS_HOST=YOUR_REDIS_HOST`
  * `export REDIS_PORT=YOUR_REDIS_PORT`
  * `export REFRESH_TIMEOUT=REFRESH_TIMEOUT`
  * `cd project`
  * create virtual environment for python and install dependencies via `pip install -r requirements.txt`
  * `python aviata/manage.py runserver` for run API
  * `python flights/main.py` for run crawler
  
  There may be errors with importing modules while running python modules,
   if you have custom PYTHONPATH values(try fix it, if it happened) <br />
  Make sure, that Redis Cache Server is available <br />
