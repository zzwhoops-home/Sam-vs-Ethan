from __future__ import print_function
import pickle
import os
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint
from googleapiclient import discovery
from mee6_py_api import API
import time
import asyncio
from datetime import datetime

# sheet ID and edit range
sheetID = ''
sheetRange = 'Ethan vs Sam!A2:F100'

# get user xp stats
mee6API = API(423583970328838154)
user_id = {
    "Ethan": [390601966423900162, 60614],
    "Sam": [501505695091392527, 60224]
}
xp_vals = []
max_xp = 0


async def get_levels():
    time_elapsed = time.time() - 1602525600  # 2 pm 10/12/2020
    stats = []
    for x in user_id:
        xp = await mee6API.levels.get_user_xp(user_id[x][0])
        original_xp = user_id[x][1]
        max_xp = round((time_elapsed / 60) * 25)
        now = datetime.now()
        formatted = now.strftime("%m/%d/%Y %H:%M:%S")
        stats.append(xp)

    write_stats(main(), formatted, stats, max_xp)

# generate credentials or something

def main():
    for x in range(2):
        try:
            creds = None
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
            # The file token.pickle stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
            # return credentials
            return creds
        except:
            print("Invalid credentials or some stupid shit with Sheets API, try again")
            os.remove("token.pickle")
            main()
        x += 1

# write player stats to google sheets


def write_stats(creds, timestamp, stats, max):
    service = discovery.build('sheets', 'v4', credentials=creds)

    values = [

    ]
    values.append([timestamp, stats[0], stats[1], max])
    data = [
        {
            'range': sheetRange,
            'values': values
        }
        # Additional ranges to update ...
    ]
    body = {
        'valueInputOption': "USER_ENTERED",
        'data': data
    }
    result = service.spreadsheets().values().batchUpdate(
        spreadsheetId=sheetID, body=body).execute()
    values = result.get('values', [])
    print('{0} cells updated.'.format(result.get('totalUpdatedCells')))

if __name__ == '__main__':
    main()

asyncio.run(get_levels())
