from datetime import datetime
from icalendar import Calendar
from analyzers.parser import parse_events


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
        date_format = "%d/%m/%y %H:%M"
        return {
            "start": self.start.strftime(date_format),
            "end": self.end.strftime(date_format),
            "duration": (self.end - self.start).total_seconds() / 3600,
            "total_events": self.total_events,
            "run_time": self.total_seconds,
        }

    def print(self):
        print("-------------------------")
        print(self.start, "start time")
        print(self.end, "end time")
        print((self.end - self.start).total_seconds() / 60 / 60, "hours in time range")
        print(self.total_seconds / 60 / 60, "hours runtime")
        print(self.total_events, "total events")
        print("-------------------------")


class GenericAnalyzer:
    def analyze(self, calendar: Calendar, start: datetime, end: datetime):
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

