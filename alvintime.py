import datetime

def getDateByN(startdate, interval):
    # startdate: "YYYY-MM-DD" string formated timestamp
    # interval = the timetamp gap, can be positive, zero or negative

    starttmpt = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    if (interval > 0):
        _delta = datetime.timedelta(days=interval)
        endtmpt = starttmpt + _delta
    elif(interval == 0):
        endtmpt = starttmpt
    else:
        _delta = datetime.timedelta(days=interval)
        endtmpt = starttmpt + _delta

    timestampStr = endtmpt.strftime("%Y-%m-%d")
    return timestampStr