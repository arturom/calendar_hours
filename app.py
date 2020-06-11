from argparse import ArgumentParser
from pytz import timezone
from datetime import datetime
from icalendar import Calendar

from readers.file_reader import FileReader
from readers.server_reader import ServerReader
from analyzers.generic import GenericAnalyzer


def main(args):
    tz = timezone(args.tz)

    start = tz.localize(datetime.strptime(args.start, args.iformat))
    end = tz.localize(datetime.strptime(args.end, args.iformat))

    if args.file is not None:
        content = FileReader(args.file).read()
    else:
        content = ServerReader(args.url).read()

    calendar = Calendar.from_ical(content)  # type: Calendar
    analysis = GenericAnalyzer().analyze(calendar, start, end)
    analysis.print()


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("--url", type=str, help="caldav server url")  # 
    parser.add_argument("--file", type=str, help="local file") # cal.ical
    parser.add_argument("--start", type=str, required=True, help="ISO-8601 formated date")
    parser.add_argument("--end", type=str, required=True, help="ISO-8601 formated date")
    parser.add_argument("--tz", type=str, required=True, help="timezone. i.e.: US/Eastern")
    parser.add_argument("--iformat", type=str, default="%Y-%m-%d", help="input format");

    args = parser.parse_args()

    if not args.url and not args.file:
        raise Exception("Either --url or --file is required ")

    main(args)
