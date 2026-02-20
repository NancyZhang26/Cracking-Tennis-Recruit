from typing import List, Optional
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.connection import get_conn
from backend.models import College_Temp, College

#  College_Temp(TypedDict, total=False):
#     school_name: str
#     gender: str
#     division: str
#     conference: str
#     location: str
#     url: str 
#     type: str | None
def insert_college_temp(college: College_Temp) -> None:
    sql = """
        INSERT INTO colleges_temp (school_name, type, gender, location, division, conference, url)
        values(%s, %s, %s, %s, %s, %s, %s)
    """ 
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, 
                (college["school_name"],
                 college["type"], 
                 college["gender"], 
                 college["location"], 
                 college["division"], 
                 college["conference"], 
                 college["url"]
            ))

# Test value
# college: College_Temp = {
#     "gender": "f",
#     "location": "Waltham, MA",
#     "division": "III",
#     "conference": "University Athletic Association",
#     "url": None,
#     "school_name": "Your dad",
#     "type": "Private"
# }
# insert_college_temp(college)

def delete_college_temp(school_name: str, gender: str) -> None:
    sql = """
        DELETE FROM colleges_temp
        WHERE school_name = %s AND gender = %s
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (school_name, gender,)) # Returns a list of dicts, thanks to dict_row 

def select_college_temp_by_division(division: str) -> List[College_Temp]:
    sql = """
        SELECT school_name, gender, division, conference, location, url, type from colleges_temp
        WHERE division = %s
    """

    res = []

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (division,))
            res = cur.fetchall() # returns a list of tuple of dict
    
    return res

# print(select_college_temp_by_division('III'))

# delete_college_temp("Your mom", "f")