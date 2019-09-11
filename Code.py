#  https://towardsdatascience.com/accessing-google-calendar-events-data-using-python-e915599d3ae2

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import datetime
import pytz

scopes = ['https://www.googleapis.com/auth/calendar']

flow = InstalledAppFlow.from_client_secrets_file("client_secret_googlecalendar.json", scopes=scopes)
#credentials = flow.run_console()

credentials = pickle.load(open("token.pkl", "rb"))
service = build('calendar', 'v3', credentials=credentials)

#pickle.dump(credentials, open("token.pkl", "wb"))

########### END OF SETUP ###############################################

"""
#  print all calendars
#  always : service + calendarList or events ? + list + execute
result = service.calendarList().list().execute()
for i in result['items']:
    print(i)

print('='*50)
"""
# calendar_id = result['items'][0]['id']

# result = service.events().list(calendarId=calendar_id).execute()
#  print(result['items'][0])

########### GETTING 10 UPCOMING EVENTS ###############################################
"""
now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
print('Getting the upcoming 10 events')
events_result = service.events().list(calendarId='primary', timeMin=now,
                                      maxResults=10, singleEvents=True,
                                      orderBy='startTime').execute()
events = events_result.get('items', [])

for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(start, event['summary'])
"""
########### GETTING EVENTS BY DATE ###############################################

"""
    Upper bound (exclusive) for an event's start time to filter by. Optional. 
    The default is not to filter by start time. 
    Must be an RFC3339 timestamp with mandatory time zone offset, 
    for example, 2011-06-03T10:00:00-07:00, 2011-06-03T10:00:00Z. 
    Milliseconds may be provided but are ignored. 
    If timeMin is set, timeMax must be greater than timeMin.
"""


print('Getting tomorrow events')
tz = pytz.timezone('America/Montreal')

#  minimum_time = datetime.date(2019, 9, 11)
minimum_time = datetime.datetime(year=2019, month=9, day=11, hour=6, minute=0, second=0, tzinfo=tz)
minimum_time2 = minimum_time.isoformat() + "Z"
#  maximum_time = datetime.date(2019, 9, 11)
maximum_time = datetime.datetime(year=2019, month=9, day=11, hour=18, minute=0, second=0, tzinfo=tz)
maximum_time2 = maximum_time.isoformat() + "Z"
print(minimum_time)
print(minimum_time2)
print("-"*50)

events_result = service.events().list(calendarId='primary', timeMin=minimum_time2,
                                      maxResults=10, singleEvents=True,
                                      orderBy='startTime').execute()
events = events_result.get('items', [])

for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(start, event['summary'])
