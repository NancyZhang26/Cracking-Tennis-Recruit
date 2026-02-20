from typing import List
import os, sys, re, requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import College, College_Temp, Player
from backend.constants import *
from db.colleges_repo import insert_college
from db.colleges_temp_repo import insert_college_temp, select_college_temp_by_division
from pprint import pprint

def get_batch_of_college_temp(division: str) -> List[College_Temp]:
    return select_college_temp_by_division(division)

"""
    Copy info from college_temp into college
"""
def copy_types_into_college(list_of_college_temp: List[College_Temp]) -> List[College]:
    colleges = []
    for ct in list_of_college_temp:
        c: College = {}
        for pair in ct:
            c[pair] = ct[pair]
        colleges.append(c)
    return colleges


# TODO: Bathc request to get the school_id
# def get_school_name_to_id_mapping(colleges: List[College]) -> List[College]:


# GET:
# school_id (id), club_id (schoolProfile/id), conference_id, url
"""
    Fill missing info in colleges (types) by checking the utr website
"""
def get_school_id_and_club_id_and_conference_id_and_url(college: College, school_id: int) -> None:
    url = f"https://api.utrsports.net/v1/club/{school_id}?optimized=true" 

    resp = requests.get(url, headers={}, timeout=10)
    data = resp.json()
    college['school_id'] = data['id']
    college['club_id'] = data['schoolProfile']['id']
    college['conference_id'] = data['schoolProfile']['conferenceId']
    college['official_url'] = data['url'];
    
# Retrieving an array of utrs from the line up
"""
    @param: gender -> f or m
"""
def get_line_up_arr(college: College) -> List[str]:
    url = f"https://api.utrsports.net/v1/college/conference/{college['conference_id']}/p6strength?gender={college['gender']}" 

    resp = requests.get(url, headers={}, timeout=10)
    data = resp.json()
    line_up_arr = []
    line_up_player = []

    for player in data['indexAndRatings']:
        p: Player = {}
        if player['schoolId'] == college['club_id']:
            line_up_arr.append(player['rating'])
            descriptions = player['description'] # "John Doe 7.38, Case Western Reserve University 2029"
            temp = re.match(r'^(.+?)\s+(\d+(?:\.\d+)?)', descriptions) 
            # capture the first group that matches: any char, space, num (potentially decimals), so, name, x.xx
            name = temp.group(1).strip()
            rating = temp.group(2).strip()

            p['player_name'] = name
            p['singles_utr'] = rating
            p['gender'] = college['gender']

            # TODO: insert the player into the db, update their info later

            line_up_player.append(name)
            
    college['line_up_utr'] = line_up_arr

    return line_up_player;

"""
    Requires cookie to view the full roster
"""
def get_roster_utr_arr(college: College, line_up_player: List[str]) -> None:
    url = f"https://api.utrsports.net/v1/club/{college['school_id']}/school" 

    headers = {
        "cookie": os.getenv("COOKIE_02_10"),
    }

    resp = requests.get(url, headers=headers)
    data = resp.json()
    rosters = data['roster']

    roster_arr = []

    for player in rosters:
        player_name = player['displayName']
        print(player_name)
        if player_name not in line_up_player and player['singlesUtr']!=0.0:
            roster_arr.append(player['singlesUtr'])

    for rating in college['line_up_utr']:
        roster_arr.append(rating)

    college['roster_utr'] = [roster_arr]

def main():
    temp = get_batch_of_college_temp('ii')
    # for t in temp:
        # print(t)
    temp_c = copy_types_into_college(temp)
    for c in temp_c:
        print(c)

main()