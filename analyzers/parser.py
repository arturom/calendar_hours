from datetime import datetime
from typing import Generator
from dateutil.rrule import rrulestr
from icalendar import Calendar
from icalendar.prop import vRecur, vDDDTypes
from icalendar.cal import Event


class PlainEvent:
    def __init__(self, dtstart: datetime, dtend: datetime, summary: str):
        self.dtstart = dtstart
        self.dtend = dtend
        self.summary = summary

    def __str__(self):
        return "{} to {} ({} hours)\t{}".format(
            self.dtstart, self.dtend,
            self.duration_seconds() / 3600,
            self.summary)

    def duration_seconds(self) -> float:
        dur = self.dtend - self.dtstart
        return dur.total_seconds()


def parse_events(calendar: Calendar, start: datetime, end: datetime) -> Generator[PlainEvent, None, None]:
    for component in calendar.walk("VEVENT"):
        component = component  # type: Event

        vrecur = component.get("rrule")  # type: vRecur
        dtstart = component.get("dtstart")  # type: vDDDTypes
        dtend = component.get("dtend")  # type: vDDDTypes
        summary = component.get("summary")  # type: str
        duration = dtend.dt - dtstart.dt

        if vrecur:
            vrecur_to_ical = vrecur.to_ical()
            rrule = rrulestr(vrecur_to_ical.decode("utf-8"))
            rrule = rrule.replace(dtstart=dtstart.dt)
            for e in rrule.between(start, end):
                yield PlainEvent(summary=summary, dtstart=e, dtend=e + duration)
        else:
            if not isinstance(dtstart.dt, datetime):
                print("skippinng: {}...".format(summary)) 
                continue
            if dtstart.dt >= start and dtend.dt <= end:
                yield PlainEvent(summary=summary, dtstart=dtstart.dt, dtend=dtend.dt)

