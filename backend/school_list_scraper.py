"""
    DON'T RUN THIS AGAIN
    Script to get the entire list of NCAA qualified school in tennis
    No need to run again in 6 months, or even longer, hopefully
    Unlike UTR, school lists barely change
"""
import requests, os
from bs4 import BeautifulSoup
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.constants import *
from db.colleges_temp_repo import insert_college_temp
from db.colleges_temp_repo import insert_college_temp
from backend.models import College_Temp
# I *don't* like parsing HTML

count = 0

for school in SCHOOL_URLS:
    college: College_Temp = {}

    URL = SCHOOL_URLS[school]
    
    str_arr = URL.split('/') # e.g. "https://www.ncsasports.org/mens-tennis/division-1-colleges" -> # ["https:", "", "www.ncsasports.org", "mens-tennis", "division-1-colleges"]
    if str_arr[len(str_arr)-1] == 'division-1-colleges':
        college['division'] = 'i'
    elif str_arr[len(str_arr)-1] == 'division-2-colleges':
        college['division'] = 'ii'
    elif str_arr[len(str_arr)-1] == 'division-3-colleges':
        college['division'] = 'iii'

    if str_arr[len(str_arr)-2] == 'mens-tennis':
        college['gender'] = 'm'
    else:
        college['gender'] = 'f'

    headers={'User-Agent': 'Mozilla/5.0'}
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find_all('div', class_="container", itemprop="item")

    # print(school.upper())

    for res in results:
        count+=1

        name = res.find('a').get_text()
        url = res.find('a')['href']
        type = res.find('div', itemprop=None).get_text()
        address = res.find('span', itemprop='addressLocality').get_text()+', '+res.find('span', itemprop='addressRegion').get_text()
        conference = res.find('div', itemprop='member').get_text()

        if name:
            # college['school_name'] = name
            print('Name of the college: ', name)
        if url:
            # college['url'] = url
            print(url)
        if type:
            # college['type'] = type
            print('Type: ', type)
        if address:
            # college['location'] = address
            print('Region of the college: ', address)
        if conference:
            # college['conference'] = conference
            print('Conference: ', conference)
        print('--------')
        
        # insert_college_temp(college)

print("There are " + str(count) + " school in total")
# 1521 schools!