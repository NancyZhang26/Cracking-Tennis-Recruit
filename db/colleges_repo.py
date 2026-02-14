import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.connection import get_conn
from backend.models import College

# school_id: int
# club_id: int
# gender: str
# location: str | None
# division: str
# p6high: int | None
# p6low: int | None
# conference: str | None
# url: str | None
def insert_college(college: College) -> None:
    sql = """
        INSERT INTO colleges (school_name, school_id, club_id, gender, location, division, p6_high, p6_low, conference, official_url)
        values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (school_id) DO UPDATE SET
            school_name = EXCLUDED.school_name,
            school_id = EXCLUDED.school_id,
            club_id = EXCLUDED.club_id,
            gender = EXCLUDED.gender,
            location = EXCLUDED.location,
            division = EXCLUDED.division,
            p6_high = EXCLUDED.p6_high,
            p6_low = EXCLUDED.p6_low, 
            conference = EXCLUDED.conference, 
            url = EXCLUDED.url;
    """ 
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, 
                (college["school_name"],
                 college["school_id"], 
                 college["club_id"], 
                 college["gender"], 
                 college["location"], 
                 college["division"], 
                 college["p6high"], 
                 college["p6low"], 
                 college["conference"], 
                 college["official_url"]
            ))

college: College = {
    "school_id": 1534,
    "club_id": 378,
    "gender": "f",
    "location": "Waltham, MA",
    "division": "III",
    "p6high": 8.9,
    "p6low": 9.1,
    "conference": "University Athletic Association",
    "official_url": None,
    "school_name": "Brandeis University"
}

insert_college(college)

def delete_college(school_id: int) -> None:
    sql = """
        DELETE FROM colleges 
        WHERE school_id = %s 
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (school_id,)) # Second param needs to be a list of items, need the comma too to show it is a tuple

delete_college(1534)