from typing import Optional

from typing_extensions import TypedDict


class FlightSearchParams(TypedDict, total=False):
    fly_from: str
    fly_to: str
    date_from: str
    date_to: str


class SkyPickerSearchParams(FlightSearchParams, total=False):
    partner: str  # picky
    curr: str  # KZT, USD, EUR
    one_city_for: bool
    partner_market: str  # kz, us, ru
    adults: Optional[int]  # Default value 1
    children: Optional[int]  # Default value 0
    infants: Optional[int]  # Default value 0


class SkyPickerCheckParams(TypedDict):
    v: int
    booking_token: str
    bnum: int
    pnum: int
    affily: str  # Example: picky_{market}
    currency: Optional[str]  # Example: KZT, USD, EUR
