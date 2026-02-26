import asyncio
from typing import List, Optional
from playwright.async_api import async_playwright, TimeoutError, Browser
from models import College
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.colleges_temp_repo import select_college_temp_by_division, select_college_temp_by_division_and_gender
from db.colleges_repo import insert_college
from scrape_per_college import copy_types_into_college
from urllib.parse import quote_plus

college_names = select_college_temp_by_division_and_gender('iii', 'm')
colleges = copy_types_into_college(college_names)
# print(colleges)

CONCURRENCY = 5
RETRY_GROUP = []

def regex_school_names(college: College) -> str:
   gender = 'W' if college['gender'] == 'f' else 'M'
   return  college['school_name'] + " - " + gender

async def get_school_id(browser: Browser, college: College) -> int: 
    context = await browser.new_context()
    page = await context.new_page()
    
    try:
        school_name = college['school_name']
        await page.goto(f"https://app.utrsports.net/search?query={quote_plus(school_name)}&type=colleges", wait_until="domcontentloaded") # dodge ad blockers
        await page.wait_for_timeout(1000)
        await page.get_by_text(regex_school_names(college)).nth(1).click(timeout=10000)

        school_id = page.url.split('/')[-1]
        college['school_id'] = school_id
        print(college)

        return school_id
    except TimeoutError:
        print(f"Can't find school_id for {school_name}")
        RETRY_GROUP.append({college['school_name'], college['gender']})
        return None
    finally:
       await page.close()
       await context.close()
 
async def run(colleges) -> List[Optional[int]]:
    sem = asyncio.Semaphore(CONCURRENCY)

    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        async def batch(college):
            async with sem:
                return await get_school_id(browser, college)

        results = await asyncio.gather(*(batch(c) for c in colleges), return_exceptions=True)

        await browser.close()
        return results

asyncio.run(run(colleges))
print(RETRY_GROUP)