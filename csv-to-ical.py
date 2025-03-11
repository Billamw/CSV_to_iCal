import pandas as pd
from icalendar import Calendar, Event, Alarm
from datetime import datetime

"""
This script reads a CSV file with contacts and their birthdays and creates an iCal file with all birthdays.
The CSV file is based on the export from Google Contacts.
"""
csv_datei = "contacts.csv"
df = pd.read_csv(csv_datei)

df.fillna("", inplace=True)

# create a new iCal calendar
cal = Calendar()

# iterate over the rows of the DataFrame
for index, row in df.iterrows():
    first_name = str(row.get("First Name", "")).strip()
    last_name = str(row.get("Last Name", "")).strip()
    birthday = str(row.get("Birthday", "")).strip()

    # if contact has enough information to create an event for their birthday
    if birthday and first_name:
        event = Event()
        if last_name:
            event.add("summary", f"{first_name} {last_name} birthday")
        else:
            event.add("summary", f"{first_name} birthday")
        bday = birthday.split("-")[-2:]
        month, day = map(int, bday)
        start_date = datetime(datetime.now().year, month, day).date()

        event.add("dtstart", start_date)  # all-day event
        event.add("dtend", start_date)
        event.add('TRANSP', 'TRANSPARENT')
        event.add("rrule", {"freq": "YEARLY"})

        # Add alarm for same day at 9 AM
        alarm = Alarm()
        alarm.add('action', 'DISPLAY')
        alarm.add('description', 'Reminder')
        alarm.add('trigger', datetime.timedelta(hours=-9))  # 9 hours before the event (9 AM on the same day)
        event.add_component(alarm)

        # add event to calendar
        cal.add_component(event)

# save calendar to file
ics_datei = "birthdays.ics"
with open(ics_datei, "wb") as f:
    f.write(cal.to_ical())

print(f"iCal-file made: {ics_datei}")