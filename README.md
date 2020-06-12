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

### Sample output
```
-------------------------
2020-01-01 00:00:00-05:00 start time
2021-01-01 00:00:00-05:00 end time
8784.0 hours in selected time range
100.75 hours of events
201 total events
-------------------------
```
