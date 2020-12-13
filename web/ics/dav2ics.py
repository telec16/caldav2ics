from datetime import datetime
import json
from pytz import UTC # timezone
from typing import List, Tuple

import caldav
from icalendar import Calendar, Event, vText

import ids


def __processEvent(event: Event, clear: bool) -> Event:
    eventClean = Event()

    # Event
    if clear and "SUMMARY" in event:
        eventClean.add('SUMMARY', event["SUMMARY"], encode=0)
    if not clear and "CATEGORIES" in event:
        eventClean.add('SUMMARY', ', '.join(event["CATEGORIES"].cats), encode=1)
    if "CATEGORIES" in event:
        eventClean.add('CATEGORIES', event["CATEGORIES"], encode=0)
    if False and clear and "DESCRIPTION" in event:
        eventClean.add('DESCRIPTION', event["DESCRIPTION"], encode=0)
    if clear and "LOCATION" in event:
        eventClean.add('LOCATION', event["LOCATION"], encode=0)

    # Date
    if "DTSTART" in event:
        eventClean.add('DTSTART', event["DTSTART"], encode=0)
    if "DURATION" in event:
        eventClean.add('DURATION', event["DURATION"], encode=0)
    if "DTEND" in event:
        eventClean.add('DTEND', event["DTEND"], encode=0)
    if "DTSTAMP" in event:
        eventClean.add('DTSTAMP', event["DTSTAMP"], encode=0)

    # Recurrence
    if "RECURRENCE-ID" in event:
        eventClean.add('RECURRENCE-ID', event["RECURRENCE-ID"], encode=0)
    if "SEQUENCE" in event:
        eventClean.add('SEQUENCE', event["SEQUENCE"], encode=0)
    if "RRULE" in event:
        eventClean.add('RRULE', event["RRULE"], encode=0)
    if "RDATE" in event:
        eventClean.add('RDATE', event["RDATE"], encode=0)
    if "EXDATE" in event:
        eventClean.add('EXDATE', event["EXDATE"], encode=0)

    # Meta
    if "UID" in event:
        eventClean.add('UID', event["UID"], encode=0)
    if "CREATED" in event:
        eventClean.add('CREATED', event["CREATED"], encode=0)
    if "LAST-MODIFIED" in event:
        eventClean.add('LAST-MODIFIED', event["LAST-MODIFIED"], encode=0)

    return eventClean


def getDavCalendar(calN: str) -> caldav.Calendar:
    URLFULL = ids.URL+"calendars/"+ids.USERN+"/"+calN

    client = caldav.DAVClient(url=ids.URL, username=ids.USERN, password=ids.PASSW)
    calendar = caldav.Calendar(client=client, url=URLFULL)

    return calendar


def convert(calD: caldav.Calendar, clear: bool) -> List[Event]:
    results = calD.events(baikal=True)
    events = []

    for subcalendar in results:
        cal = Calendar.from_ical(subcalendar._data)
        for component in cal.walk():
            if component.name == "VEVENT":
                event = __processEvent(component, clear)
                events.append(event)

    return events


def getEvents(calN: str, clear: bool) -> List[Event]:
    return convert(getDavCalendar(calN), clear)


def getStrCalendar(calN: str, clear: bool) -> str:
    return getStrCalendars([(calN, clear)])


def getStrCalendars(calendars: List[Tuple[str, bool]]) -> str:
    cal = Calendar()
    for calendar in calendars:
        events = getEvents(*calendar)
        for event in events:
            cal.add_component(event)
    return cal.to_ical().decode("utf-8")


if __name__ == "__main__":
    print(getStrCalendars([("default", True), ("personnal", False)]))
    
    c = getDavCalendar("default")
    r = c.events(baikal=True)
    for subcalendar in r:
        cal = Calendar.from_ical(subcalendar._data)
        for component in cal.walk():
            if component.name == "VEVENT":
                if 'RRULE' in component and 'EXDATE' in component:
                    e = component
