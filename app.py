from httplib2 import Http
from icalevents.icaldownload import ICalDownload
from pytz import timezone
from datetime import datetime
from dateutil.rrule import rrulestr
from icalendar import Calendar
from icalendar.prop import vRecur, vDDDTypes
from icalendar.cal import Event
from typing import Generator


class SimpleEvent:
    def __init__(self, dtstart: datetime, dtend: datetime, summary: str):
        self.dtstart = dtstart
        self.dtend = dtend
        self.summary = summary

    def __str__(self):
        return '{}: "{}" to "{}" ({} hours)'.format(
            self.summary, self.dtstart, self.dtend,
            self.duration_seconds() / 3600)

    def duration_seconds(self) -> float:
        dur = self.dtend - self.dtstart
        return dur.total_seconds()


def parse_events(calendar: Calendar, start: datetime, end: datetime) -> Generator[SimpleEvent, None, None]:
    for component in calendar.walk('VEVENT'):
        component = component  # type: Event

        vrecur = component.get('rrule')  # type: vRecur
        dtstart = component.get('dtstart')  # type: vDDDTypes
        dtend = component.get('dtend')  # type: vDDDTypes
        summary = component.get('summary')  # type: str
        duration = dtend.dt - dtstart.dt

        if vrecur:
            vrecur_to_ical = vrecur.to_ical()
            rrule = rrulestr(vrecur_to_ical.decode("utf-8"))
            rrule = rrule.replace(dtstart=dtstart.dt)
            for e in rrule.between(start, end):
                yield SimpleEvent(summary=summary, dtstart=e, dtend=e + duration)
        else:
            if dtstart.dt >= start and dtend.dt <= end:
                yield SimpleEvent(summary=summary, dtstart=dtstart.dt, dtend=dtend.dt)


class Analysis:
    def __init__(
            self,
            start: datetime,
            end: datetime,
            total_events: int,
            total_seconds: float
    ):
        self.start = start
        self.end = end
        self.total_events = total_events
        self.total_seconds = total_seconds

    def to_dict(self):
        date_format = '%d/%m/%y %H:%M'
        return {
            'start': self.start.strftime(date_format),
            'end': self.end.strftime(date_format),
            'duration': (self.end - self.start).total_seconds() / 3600,
            'total_events': self.total_events,
            'run_time': self.total_seconds,
        }


def analyze(calendar: Calendar, start: datetime, end: datetime):
    total_seconds = 0
    total_events = 0
    for event in parse_events(calendar, start=start, end=end):
        total_events += 1
        total_seconds += event.duration_seconds()
        print(event)
    return Analysis(
        start=start, end=end,
        total_events=total_events,
        total_seconds=total_seconds)


def main(from_file=True):
    tz_str = 'US/Eastern'
    tz = timezone(tz_str)

    start = tz.localize(datetime(2018, 3, 6))
    end = tz.localize(datetime(2018, 3, 12))

    if from_file:
        content = ICalDownload(None).data_from_file('cal.ical')
    else:
        url = 'http://localhost:5232/cals/cal_01'
        http = Http('.cache')
        content = ICalDownload(http).data_from_url(url)

    calendar = Calendar.from_ical(content)  # type: Calendar
    analysis = analyze(calendar, start, end)

    print('-------------------------')
    print(analysis.start, 'start time')
    print(analysis.end, 'end time')
    print((analysis.end - analysis.start).total_seconds() / 60 / 60, 'hours in time range')
    print(analysis.total_seconds / 60 / 60, 'hours runtime')
    print(analysis.total_events, 'total events')
    print('-------------------------')


if __name__ == '__main__':
    main(from_file=False)
