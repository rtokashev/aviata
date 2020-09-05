from typing import List

from client.models import FlightSearchParams

'''
Explicitly define the directions of flights using a pre-created dictionary
- ALA - TSE  NQZ instead TSE
- TSE - ALA
- ALA - MOW
- MOW - ALA
- ALA - CIT
- CIT - ALA
- TSE - MOW
- MOW - TSE
- TSE - LED
- LED - TSE

# in Redis
 1) "CIT-ALA"
 2) "ALA-NQZ"
 3) "ALA-CIT"
 4) "NQZ-VKO"
 5) "VKO-NQZ"
 6) "VKO-ALA"
 7) "LED-NQZ"
 8) "NQZ-LED"
 9) "ALA-VKO"
10) "NQZ-ALA"

'''


directions: List[FlightSearchParams] = [
    FlightSearchParams(
        fly_from="ALA",
        fly_to="NQZ",
    ),
    FlightSearchParams(
        fly_from="TSE",
        fly_to="ALA",
    ),
    FlightSearchParams(
        fly_from="ALA",
        fly_to="MOW",
    ),
    FlightSearchParams(
        fly_from="MOW",
        fly_to="ALA",
    ),
    FlightSearchParams(
        fly_from="ALA",
        fly_to="CIT",
    ),
    FlightSearchParams(
        fly_from="CIT",
        fly_to="ALA",
    ),
    FlightSearchParams(
        fly_from="TSE",
        fly_to="MOW",
    ),
    FlightSearchParams(
        fly_from="MOW",
        fly_to="TSE",
    ),
    FlightSearchParams(
        fly_from="TSE",
        fly_to="LED",
    ),
    FlightSearchParams(
        fly_from="LED",
        fly_to="TSE",
    ),
]
