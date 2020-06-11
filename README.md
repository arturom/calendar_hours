# calendar_hours
A command line tool that provides stats about the events from an iCal file or CalDAV server
between a date/time range 

## Sample usage

### Reading from a CalDAV server
```bash
python app.py \
  --url="http://localhost:5232/cals/cal_01" \
  --start="2020-01-01" \
  --end="2021-01-01" \
  --ts="US/Eastern"
```

### Reading from an iCal file
```bash
python app.py \
  --file="path/to/cal.ical" \
  --start="2020-01-01" \
  --end="2021-01-01" \
  --ts="US/Eastern"
```
