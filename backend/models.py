from numbers import Real
from typing import TypedDict, List

class College(TypedDict, total=False):
    school_id: int
    club_id: int
    gender: str
    location: str | None
    division: str
    p6high: Real | None
    p6low: Real | None
    conference: str | None
    url: str | None
    school_name: str
    line_up_utr: List[Real] 
    roster_utr: List[Real]
    line_up_utr_avg: Real
    roster_utr_avg: Real
    conference_id: int
    type: str | None
    official_url: str | None

class Player(TypedDict, total=False):
    player_name: str
    gender: str | None
    player_id: int
    singles_utr: Real | None
    doubles_utr: Real | None 
    location: str | None
    school_id: Real | None

class College_Temp(TypedDict, total=False):
    school_name: str
    gender: str
    division: str
    conference: str
    location: str
    url: str 
    type: str | None