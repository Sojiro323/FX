import datetime
import time

def unixtime(year, month, day, hour, minute, second):
    d = datetime.datetime(year,month,day,hour,minute,second)
    return int(time.mktime(d.timetuple()))
