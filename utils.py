import datetime
import time
import json

def get_time(year, month, day, hour, minute, second):
    d = datetime.datetime(year, month, day, hour, minute, second)
    d=d-datetime.timedelta(hours=9)
    return "{0}-{1}-{2}T{3}:{4}:{5}.000000Z+09:00".format(
                                            str(d.year),str(d.month).zfill(2),str(d.day).zfill(2),
                                            str(d.hour).zfill(2),str(d.minute).zfill(2),str(d.second).zfill(2))

def get_now():
    d = datetime.datetime.now()
    japan = datetime.timedelta(hours=9)
    d=d-japan
    return "{0}-{1}-{2}T{3}:{4}:{5}.000000Z+09:00".format(
                                            str(d.year),str(d.month).zfill(2),str(d.day).zfill(2),
                                            str(d.hour).zfill(2),str(d.minute).zfill(2),str(0).zfill(2))

def get_next(span):
    sp =  {"S":60,"M":60,"H":24}
    f = True
    t = span[0]
    span=int(span[1:])
    d = datetime.datetime.now()
    if t == "S":
        target=d.second
        add = datetime.timedelta(seconds=span - (target%span))
        next=d+add
        return "{0}-{1}-{2} {3}:{4}:{5}".format(
                                            str(next.year),str(next.month).zfill(2),str(next.day).zfill(2),
                                            str(next.hour).zfill(2),str(next.minute).zfill(2),str(next.seconds).zfill(2))
    elif t == "M":
        target=d.minute
        add = datetime.timedelta(minutes=span - (target%span))
        next=d+add
        return "{0}-{1}-{2} {3}:{4}:{5}".format(
                                            str(next.year),str(next.month).zfill(2),str(next.day).zfill(2),
                                            str(next.hour).zfill(2),str(next.minute).zfill(2),str(0).zfill(2))
    elif t == "H":
        target=d.hour
        add = datetime.timedelta(hours=span - (target%span))
        next=d+add
        return "{0}-{1}-{2} {3}:{4}:{5}".format(
                                            str(next.year),str(next.month).zfill(2),str(next.day).zfill(2),
                                            str(next.hour).zfill(2),str(0).zfill(2),str(0).zfill(2))


def order_condition(flag, api):
    response = json.loads(api.get_tickets().text)
    trades = response['trades']
    #units = 0
    #for trade in trades: units+=trade["units"]
    if int(api.UpperBound_tickets) < len(trades): flag = False
    return flag
