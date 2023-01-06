import gspread
from datetime import datetime
from mee6_py_api import API
import time
import asyncio

# get service account credentials
gc = gspread.service_account(filename='')

# get user xp stats
user_id = {
    "Ethan": [390601966423900162, 60614],
    "Sam": [501505695091392527, 60224]
}
xp_vals = []
max_xp = 0

# Open a sheet from a spreadsheet in one go
wks = gc.open("Sam vs. Ethan Graph").sheet1


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list) + 1)

async def get_levels():
    mee6API = 0
    while True:
        try:
            await asyncio.sleep(898)
            mee6API = API(423583970328838154)
            time_elapsed = time.time() - 1602525600  # 2 pm 10/12/2020
            stats = []
            for x in user_id:
                xp = await mee6API.levels.get_user_xp(user_id[x][0])
                # original_xp = user_id[x][1]
                max_xp = round((time_elapsed / 60) * 25)
                now = datetime.now()
                formatted = now.strftime("%m/%d/%Y %H:%M:%S")
                stats.append(xp)
            next_row = next_available_row(wks)
            values = [formatted, stats[0], stats[1], max_xp]
            wks.update(f'A{next_row}', [values], value_input_option='USER_ENTERED')
            print(f"updated with {values}")
        except Exception as e:
            print(e)

loop = asyncio.get_event_loop()
loop.run_until_complete(get_levels())