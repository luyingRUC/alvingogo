import datetime
import calendar

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



def geneTimePeriodWeekly(central, movenment, stride = 1, direction = "both"):
    # This function generate a string-formatted tiemstamp list for a specific time span, with following paras: 
        # central: the focal week timestamp, in the faormat of "YYYY-WW"
            # example: 2020-01 means the first week of 2020s
        # Direction:
            # "both" : generate timestamp string both before the central stamp and after
            # "left" : generate timestamp string only before the central stamp
            # "right" : generate timestamp string only after the central stamp
        # stride: the span for either forward or backward movenment
            # default value : 1
            # int
        # how many weeks to move, 
            # int
    if("-" in central):
        year, week = central.split("-")[0], central.split("-")[1]
        year, week = int(year), int(week)
        if ((week - movenment * stride) <0 &  (week + movenment * stride) > 53 ):
            print("geneTimePeriodWeekly: timeperiod beyond current year")
            return
        else: 
            if(direction == "both"):                
                _week_min = week - movenment * stride
                _week_max = week + movenment * stride
            elif (direction == "left"):
                _week_min = week - movenment * stride
                _week_max = week
            elif (direction == "right"):
                _week_min = week
                _week_max = week + movenment * stride
            else:
                print("the parameter Direction is not good")
                return
            weeks = range(_week_min, _week_max+1, stride)
            _timestamps = []
            for w in weeks:
                if(len(str(w)) >1):
                    _timestamps.append(str(year)+ "-" + str(w))
                else:
                    _timestamps.append(str(year)+ "-0" + str(w))
            # _timestamps = [str(year)+ "-" + str(s) for s in weeks]
            return _timestamps
    else:
        print("the format of weekly input: %s is not right" %(central))   
        return 


def getCurrentDayMonth():
    # This function returns a "MM-DD" format timestamp for current date
    i = datetime.datetime.now()
    month = i.month
    if month < 10:
        month = "0" + str(month)
    else:
        month = str(month)
    day= i.day
    if day < 10:
        day = "0" + str(day)
    else:
        day = str(day)
    
    result = month  + day
    return result

def calStringSimilarity(stirng1, string2):
    # return similarity value of two strings
    return difflib.SequenceMatcher(None, stirng1, string2).quick_ratio()


def geneDayWeeksBefore(inputTimeString, n_week):
    # this function return the timestamp of the first day of N week that is prior to the input timestamp 
        # inputTime : a string of a timestamp
        # n_week: how many weeks that we want to trace back, if it is 0: then is the current week
    
    currentTime = datetime.datetime.strptime(inputTimeString, '%Y-%m-%d %H:%M:%S')

    result = currentTime

    # weeknum = currentTime.isocalendar()[1]
    if (n_week == 0):
        weekday = currentTime.weekday()
        diff_days = weekday -0
        if(diff_days == 0):
            result = currentTime
        else: 
            result = currentTime - datetime.timedelta(days= diff_days)
    else:
        result = currentTime - datetime.timedelta(days= n_week * 7)
        weekday = result.weekday()
        diff_days = weekday -0
        if(diff_days == 0):
            result = result
        else: 
            result = result - datetime.timedelta(days= diff_days)

    return result

def geneLastDaysMonthly(year):
    # This function returns a list of dateformated strings which indicate the last day of each month for the specific year
    result = []
    for i in range(1, 13):
        last_day_of_month = calendar.monthrange(year,i)[1]
        timestamp = datetime.datetime(year, i, last_day_of_month).strftime("%Y-%m-%d")
        result.append(timestamp)

    return result

def geneLastDaysWeekly(year):
    # This function returns a list of dateformated strings which indicate the last day of each week for the specific year
    result = []
    # first day of one year
    _date = datetime.datetime(year, 1, 7)
    while(1):
        if(_date.year != year):
            break
        else: 
            timestamp = _date.strftime("%Y-%m-%d")
            result.append(timestamp)
            _date = _date + datetime.timedelta(days=7)

    return(result)


def geneDays(year):
    # This function returns a list of dateformated strings which indicate each day for the specific year
    result = []
    # first day of one year
    _date = datetime.datetime(year, 1, 7)
    while(1):
        if(_date.year != year):
            break
        else: 
            timestamp = _date.strftime("%Y-%m-%d")
            result.append(timestamp)
            _date = _date + datetime.timedelta(days=1)

    return(result)


def unifyDateFormat(input_date_string): 
    if(isinstance(input_date_string, str) == False):
        # first check whether input is a string, sometimes the input is nonetype, then should return direclty
        return
    else: 
        if(len(input_date_string) > 0):
            result = input_date_string
            if("/" in input_date_string):
                if(len(input_date_string.strip()) >11):
                    _date = datetime.datetime.strptime(input_date_string, '%m/%d/%Y %H:%M')
                    result =  _date.strftime("%Y-%m-%d")
                else: 
                    _date = datetime.datetime.strptime(input_date_string, '%m/%d/%Y')
                    result =  _date.strftime("%Y-%m-%d")
            elif("-" in input_date_string): 
                if(len(input_date_string.strip()) >11):
                    _date = datetime.datetime.strptime(input_date_string, '%Y-%m-%d %H:%M:%S')
                    result =  _date.strftime("%Y-%m-%d")
                else:
                    _date = datetime.datetime.strptime(input_date_string, '%Y-%m-%d')
                    result = _date.strftime("%Y-%m-%d")
        else: 
            result = ""
        return result


def getWeekNum(year):
    result = datetime.date(year, 12, 28).isocalendar()[1]
    return result

def getBiweekNum(year):
    weeknum = datetime.date(year, 12, 28).isocalendar()[1]
    return round(weeknum/2)


def geneYearWeekList(yearweek_min, yearweek_max):
    # Generate all "year_week" format string within the given scope
    result = []
    year1, week1 = yearweek_min.split("-")[0], yearweek_min.split("-")[1]
    year2, week2 = yearweek_max.split("-")[0], yearweek_max.split("-")[1]
    if(year1 == year2):
        for i in range(int(week1), int(week2) + 1, 1):
            if (i <10):
                result.append(year1+ "-0" +str(i) )
            else:
                result.append(year1+ "-" +str(i) )     
    else: 
        y = int(year1)
        while(y<= int(year2)):
            if( y == int(year1)):
                for i in range(int(week1), getWeekNum(int(year1)) + 1, 1):
                    if (i <10):
                        result.append(str(y)+ "-0" +str(i) )
                    else:
                        result.append(str(y)+ "-" +str(i) )            
            elif(y < int(year2) and y > int(year1)):
                for i in range(1,getWeekNum(y) + 1, 1):
                    if (i <10):
                        result.append(str(y)+ "-0" +str(i) )
                    else:
                        result.append(str(y)+ "-" +str(i) )
            elif(y == int(year2)):
                for i in range(1, int(week2) + 1, 1):
                    if (i <10):
                        result.append(str(y)+ "-0" +str(i) )
                    else:
                        result.append(str(y)+ "-" +str(i) )            
            y = y+1
    return result 



def geneYearBiWeekList(yearbiweek_min, yearbiweek_max):
    # Generate all "year_biweek" format string within the given scope
    result = []
    year1, week1 = yearbiweek_min.split("-")[0], yearbiweek_min.split("-")[1]
    year2, week2 = yearbiweek_max.split("-")[0], yearbiweek_max.split("-")[1]
    if(year1 == year2):
        for i in range(int(week1), int(week2) + 1, 1):
            if (i <10):
                result.append(year1+ "-0" +str(i) )
            else:
                result.append(year1+ "-" +str(i) )     
    else: 
        y = int(year1)
        while(y<= int(year2)):
            if( y == int(year1)):
                for i in range(int(week1), getBiweekNum(int(year1)) + 1, 1):
                    if (i <10):
                        result.append(str(y)+ "-0" +str(i) )
                    else:
                        result.append(str(y)+ "-" +str(i) )            
            elif(y < int(year2) and y > int(year1)):
                for i in range(1,getBiweekNum(y) + 1, 1):
                    if (i <10):
                        result.append(str(y)+ "-0" +str(i) )
                    else:
                        result.append(str(y)+ "-" +str(i) )
            elif(y == int(year2)):
                for i in range(1, int(week2) + 1, 1):
                    if (i <10):
                        result.append(str(y)+ "-0" +str(i) )
                    else:
                        result.append(str(y)+ "-" +str(i) )            
            y = y+1
    return result 