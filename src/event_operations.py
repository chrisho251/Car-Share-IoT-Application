import pickle
from googleapiclient import discovery
from datetime import datetime, timedelta

# This class contains methods for event-related operations on Google Calendar
# Methods use credentials stored in token.pickle to access calendar.


class CalendarOps():
    def getEvent(self, email, start_time, end_time, summary,
                 location, description, timezone):
        return {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'attendees': [{
                'email': email
            }],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

    def createEvent(self, email, start_time, end_time, summary):
        try:
            credentials = pickle.load(open("token.pickle", "rb"))
            service = discovery.build(
                "calendar", "v3", credentials=credentials
            )
            timezone = 'Asia/Ho_Chi_Minh'
            location = 'Ho Chi Minh'
            description = 'Car Booking'
            result = service.calendarList().list().execute()
            calendar_id = result['items'][0]['id']
            event = self.getEvent(
                email, start_time, end_time, summary,
                location, description, timezone
            )
            service.events().insert(
                calendarId=calendar_id, body=event
                ).execute()
            print("Event created!")  # Debug
        except Exception as exception:
            print("Error while creating event: ", str(exception))
        return True

    def deleteEvent(self, event_id):
        try:
            credentials = pickle.load(open("token.pickle", "rb"))
            service = discovery.build(
                "calendar", "v3", credentials=credentials
            )
            result = service.calendarList().list().execute()
            calendar_id = result['items'][0]['id']

            service.events().delete(
                calendarId=calendar_id, eventId=event_id
            ).execute()
            print("Event deleted!")  # Debug
        except Exception as exception:
            print("Error while deleting event: ", str(exception))
        return True
