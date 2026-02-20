import asyncio
from typing import List, Optional
from playwright.async_api import async_playwright, TimeoutError, Browser
from models import College
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.colleges_temp_repo import select_college_temp_by_division
from scrape_per_college import copy_types_into_college

college_names = select_college_temp_by_division('i')
# print(len(college_names))

colleges = copy_types_into_college(college_names)

CONCURRENCY = 5

async def get_school_id(browser: Browser, college: College) -> int: 
    context = await browser.new_context()
    page = await context.new_page()
    
    try:
        school_name = college['school_name']
        await page.goto(f"https://app.utrsports.net/search?query={school_name}&type=colleges", wait_until="domcontentloaded") # dodge ad blockers
        gender = 'W' if college['gender'] == 'f' else 'M'
        await page.get_by_text(college['school_name']+" - "+gender).nth(1).click(timeout=10000)

        school_id = page.url.split('/')[-1]
        college['school_id'] = school_id
        print(college)

        return school_id
    except TimeoutError:
        print(f"Can't find school_id for {school_name}")
        return None
    finally:
       await context.close()
       await page.close()
 
async def run() -> List[Optional[int]]:
    sem = asyncio.Semaphore(CONCURRENCY)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        async def batch(college):
            async with sem:
                return await get_school_id(browser, college)

    results = await asyncio.gather(*(batch(c) for c in colleges), return_exceptions=True)
    await browser.close()
    return results

asyncio.run(run())