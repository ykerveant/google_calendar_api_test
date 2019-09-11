#  https://towardsdatascience.com/accessing-google-calendar-events-data-using-python-e915599d3ae2
#  https://gist.github.com/cwurld/9b4e10dbeecab28345a3
#  https://developers.google.com/calendar/v3/reference/events/list

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

print('Getting tomorrow events')
tz = pytz.timezone('America/Montreal')

#  setting dates of analysis
the_datetime = tz.localize(datetime.datetime(2019, 9, 10, 6))
the_datetime2 = tz.localize(datetime.datetime(2019, 9, 10, 19))

#  converting date to the right format
minimum_time = the_datetime.isoformat()
maximum_time = the_datetime2.isoformat()

print("-"*50)

events_result = service.events().list(calendarId='primary', timeMin=minimum_time,
                                      timeMax=maximum_time, maxResults=10,
                                      singleEvents=True, orderBy='startTime').execute()
events = events_result.get('items', [])

#  printing header
print('start\tend\tevent')

for event in events:
    full_start = event['start'].get('dateTime', event['start'].get('date'))
    #  print('full start', full_start)
    #  issue : removing semicolon at timezone definition
    #  datetime.datetime.strptime(full_start, '%Y-%m-2%dT%H:%M:%S-04:00')
    full_end = event['end'].get('dateTime', event['end'].get('date'))
    print(full_start, "\t", full_end, "\t", event['summary'])
