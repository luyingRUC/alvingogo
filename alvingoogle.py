from pytrends.request import TrendReq
import pandas as pd 
import time
from alvingogo.alvintime import getDateByN
from alvingogo.alvinprogress import alvinSleep


def getGoogleKeywords(kwlist):       
    pytrend = TrendReq()
    # keyword_codes is only to save keywords that passed to google api
    KEYWORDS_CODES = []
    # result returns a dictionary where key is the converted google-keyword code, value is the orginal keyword
    result = {}
    for kw in kwlist: 
        if (len(kw.split(" ")) >1):
            try:
                if(len(pytrend.suggestions(keyword=kw)) > 0):
                    KEYWORDS_CODES.append(pytrend.suggestions(keyword=kw)[0])
                    result[pytrend.suggestions(keyword=kw)[0]["mid"]] = kw
                else: 
                    KEYWORDS_CODES.append({"mid":kw, "title": kw, "type":""})
                    result[kw] = kw
            except Exception as e:
                print(e)
        else:
            KEYWORDS_CODES.append({"mid":kw, "title": kw, "type":""})
            result[kw] = kw
    # KEYWORDS_CODES=[pytrend.suggestions(keyword=i)[0] for i in KEYWORDS] 
    df_CODES= pd.DataFrame(KEYWORDS_CODES)

    EXACT_KEYWORDS = df_CODES['mid'].to_list()

    # Individual_EXACT_KEYWORD = list(zip(*[iter(EXACT_KEYWORDS)]*1))
    # Individual_EXACT_KEYWORD = [list(x) for x in Individual_EXACT_KEYWORD]

    # print(EXACT_KEYWORDS)
    print(result)

    return EXACT_KEYWORDS, result


def getGoogleTrendsByKeywordsDaily(keywords, startDate, endDate, outputCsvPath,  mode = "csv"):
    # This function returns a dataframe where row is timestamp and column is keywords
        # mode: 
            # = csv:write the dataframe into csv file directly
            # = mysql-csv: convert to a csv where each record contains (keyword_name, date, googleindex value)


    # Please pay attention: This function is aborted because the results are not good enough, detailed reason please refer to this page:
    #   https://www.thenextad.com/blog/exploring-the-benefits-of-google-trends/#:~:text=Interpreting%20Google%20Trends&text=The%20numbers%20represent%20the%20search,term%20is%20half%20as%20popular.
    

    # THIS FUNCTION IS NOT RIGHT BECAUSE WE DID NOT CONVERT TO THE SAME BASE

    dataset = []
    pytrend = TrendReq(hl='en-GB')

    if(getDateByN(startDate, 90) >= endDate ):
        # this means we can get all the google trend index results by using only one time request
              
        pytrend.build_payload(kw_list= keywords, cat= 0, timeframe= '{0} {1}'.format(startDate, endDate), geo= "GB")
        # pytrend.build_payload(kw_list= keywords, cat= 0, timeframe= 'all', geo= "GB")

        data = pytrend.interest_over_time()
        if not data.empty:
            data = data.drop(labels = ['isPartial'], axis = "columns")
            dataset.append(data)

    else: 
        # this means we are trying to get data from a time period longer than 3 months 
        dstart = startDate
        while(1):
            if(getDateByN(dstart, 90) > endDate): 
                pytrend.build_payload(kw_list= keywords, cat= 0, timeframe= '{0} {1}'.format(dstart, endDate), geo= "GB")
                data = pytrend.interest_over_time()
                if not data.empty:
                    data = data.drop(labels = ['isPartial'], axis = "columns")
                    dataset.append(data)                
                break
            else:                                                
                dend = getDateByN(dstart, 90)
                pytrend.build_payload(kw_list= keywords, cat= 0, timeframe= '{0} {1}'.format(dstart, dend), geo= "GB")

                data = pytrend.interest_over_time()
                if not data.empty:
                    data = data.drop(labels = ['isPartial'], axis = "columns")
                    dataset.append(data)
                dstart = getDateByN(dstart, 90)
    
    # prepare the output into one unified dataframe
    if(len(dataset)):
        googleDf = pd.concat(dataset, axis=0)
        if(mode == "csv"):
            googleDf.to_csv(outputCsvPath)
        elif(mode == "mysql-csv"):
            # convert the dataframe to mysql format
            with open(outputCsvPath, "a", encoding= "utf-8") as outputfile:
                # outputfile.write("date,keyword,googleTrendIndex" + "\n")
                for kw in keywords:            
                    for index, row in googleDf.iterrows():
                        _date = index.strftime("%Y-%m-%d")
                        _gtrend = row[kw]
                        _kw = kw
                        outputfile.write(_date + "," + _kw + "," + str(_gtrend)  + "\n")
        else:
            print("input mode invalid... please retry")
    else:
        print("No google index historical values found, function returns ")
        return

def getGoogleTrends_multiple_daily_vertical(wordList, startDate, endDate, category):
    result_df = pd.DataFrame()

    vertical_list = []
    pytrend = TrendReq(hl='en-GB')

    if(getDateByN(startDate, 90) >= endDate ):
        # this means we can get all the google trend index results by using only one time request
              
        pytrend.build_payload(kw_list= wordList, cat= category, timeframe= '{0} {1}'.format(startDate, endDate), geo= "GB")
        # pytrend.build_payload(kw_list= wordList, cat= 0, timeframe= 'all', geo= "GB")

        data = pytrend.interest_over_time()
        if not data.empty:
            data = data.drop(labels = ['isPartial'], axis = "columns")
            vertical_list.append(data)

    else: 
        # this means we are trying to get data from a time period longer than 3 months 
        dstart = startDate
        while(1):
            if(getDateByN(dstart, 90) > endDate): 
                pytrend.build_payload(kw_list= wordList, cat= category, timeframe= '{0} {1}'.format(dstart, endDate), geo= "GB")
                data = pytrend.interest_over_time()
                if not data.empty:
                    data = data.drop(labels = ['isPartial'], axis = "columns")
                    vertical_list.append(data)                
                break
            else:                                                
                dend = getDateByN(dstart, 90)
                pytrend.build_payload(kw_list= wordList, cat= category, timeframe= '{0} {1}'.format(dstart, dend), geo= "GB")

                data = pytrend.interest_over_time()
                if not data.empty:
                    data = data.drop(labels = ['isPartial'], axis = "columns")
                    vertical_list.append(data)
                dstart = getDateByN(dstart, 90)

            # alvinSleep(10)
            

            

    # get the number of vertical blocks returned
    n_vertical_blks = len(vertical_list)

    if(n_vertical_blks == 1): 
        # there is only one vertical block get extracted: no process needed
        result_df = pd.concat(vertical_list, axis=0)
    else:        
        # first save ratios between (i+1)-th block and (i)-th block: which means max(v(i+1))/ max(v(i))
        vertical_max_ratios = []
        for i in range(0, n_vertical_blks-1):
            v1 = vertical_list[i].iloc[-1, 0]
            v2 = vertical_list[i+1].iloc[0,0]

            # some kw may have very little search trend, even to 0, do processing in case of null/ divided by zero
            if(v1 + v2 == 0):
                # if search value for kw in v1 and v2 both equal to zero, then the ratio should be 1 
                vertical_max_ratios.append(1.)
            elif(v2 == 0):
                vertical_max_ratios.append(v1-v2)
            else:
                vertical_max_ratios.append(v1/v2)
        
        # then save the ratio of max values compare with first max value
        # so vertical_max_ratios_converted[0] = 1 since max(v1) = 1* max(v1)
        # max(v2) = (max(v2)/max(v1)) * max(v1), where  (max(v2)/max(v1)) is the first value of vertical_max_ratios[]
        # max(v3) = (max(v3)/max(v2)) * (max(v2)/max(v1)) * max(v1), where  (max(v2)/max(v1)) is vertical_max_ratios[0], (max(v3)/max(v2)) is vertical_max_ratios[1]
        # ...
        vertical_max_ratios_converted = {}
        vertical_max_ratios_converted[0] = 1. 
        _multiplor = 1.
        for i in range(0, len(vertical_max_ratios)):
            vertical_max_ratios_converted[i + 1] = vertical_max_ratios[i] * _multiplor
            _multiplor = _multiplor * vertical_max_ratios[i]
        
        # sorted vertical_max_ratios_converted{} to find the max value of which block is the most max among all the blocks
        ratios_converted_sorted = sorted(vertical_max_ratios_converted.items(), key=lambda item: item[1], reverse= True)
        _ultimate_max = ratios_converted_sorted[0]
        _ultimate_max_index = _ultimate_max[0]

        # for each vertical block, convert every element to vertical* element( vertical* is the ideal case where if we are able to fetch data without 90-day restriction)
        for i in range(0,n_vertical_blks): 
            if(i == _ultimate_max_index): 
                # if current max value of current block is exactly the ultimate max value of all blocks, the elements in this block remain unchanged
                vertical_list[i] = vertical_list[i].iloc[0:-1,:]
                
            else:
                # if current index is not ultimate max value index
                """ insert the math fomula here """
                vertical_list[i] = vertical_list[i] * (vertical_max_ratios_converted[i] / vertical_max_ratios_converted[_ultimate_max_index])
                vertical_list[i] = vertical_list[i].iloc[0:-1,:]

        result_df = pd.concat(vertical_list, axis=0)
    
    return result_df


def getGoogleTrendsByMultipleWordsDaily(kwDict, startDate, endDate, outputCsvPath, category, mode = "csv"):
    # this function returns google trend values for multiple words as csv file 
    # we did quite convertion due to google api's restriction
   
    result_df = pd.DataFrame()

    # this is the keywords that are input to google api, some are original words, some are google-format code       
        # please see function `getGoogleKeywords` for details  
    wordList = [kw for kw in kwDict.keys()]


    if(len(wordList) <= 3):
        # if only have at most 3 keywords, then only use the vertical merging is enough
        result_df = getGoogleTrends_multiple_daily_vertical(wordList, startDate, endDate, category)
    else:
        # Do horizonal merge only if we have more than 5 keywords
        horizonal_list = []
        kw_start = 0
        while(1):
            if(kw_start + 3 > len(wordList)): 
                # why wordlist[kw_start -1, -1]: kw_start -1 is to let different horizonal units have overlaping one keyword
                if( len(horizonal_list)):
                    df_unit = getGoogleTrends_multiple_daily_vertical(wordList[kw_start-1: ], startDate, endDate,category)
                else: 
                    df_unit = getGoogleTrends_multiple_daily_vertical(wordList[kw_start:], startDate, endDate, category)
                horizonal_list.append(df_unit)              
                break
            else:                                                
                kw_end = kw_start + 3
                if( len(horizonal_list)):
                    df_unit = getGoogleTrends_multiple_daily_vertical(wordList[kw_start-1: kw_end], startDate, endDate, category)
                else: 
                    df_unit = getGoogleTrends_multiple_daily_vertical(wordList[kw_start: kw_end], startDate, endDate, category)
                horizonal_list.append(df_unit)
                kw_start = kw_start + 3

            # sleep for five seconds incase of block from google anti-crawling
            # alvinSleep(10)
        
        # get the number of horizonal blocks returned
        n_horizonal_blks = len(horizonal_list)

        # first save ratios between (i+1)-th block and i-th block
        horizonal_max_ratios = []
        for i in range(0, n_horizonal_blks-1):
            v1 = horizonal_list[i].iloc[0, -1]
            v2 = horizonal_list[i+1].iloc[0,0]

            # some kw may have very little search trend, even to 0, do processing in case of null/ divided by zero
            if(v1 + v2 == 0):
                # if search value for kw in v1 and v2 both equal to zero, then the ratio should be 1 
                horizonal_max_ratios.append(1.)
            elif(v2 == 0):
                # v2 = 0.1
                horizonal_max_ratios.append(v1-v2)
            else:
                horizonal_max_ratios.append(v1/v2)

        
        # then save the ratio of max values compare with first max value
        # so horizonal_max_ratios_converted[0] = 1 since max(v1) = 1* max(v1)
        # max(v2) = (max(v2)/max(v1)) * max(v1), where  (max(v2)/max(v1)) is the first value of horizonal_max_ratios[]
        # max(v3) = (max(v3)/max(v2)) * (max(v2)/max(v1)) * max(v1), where  (max(v2)/max(v1)) is horizonal_max_ratios[0], (max(v3)/max(v2)) is horizonal_max_ratios[1]
        # ...
        horizonal_max_ratios_converted = {}
        horizonal_max_ratios_converted[0] = 1. 
        _multiplor = 1.
        for i in range(0, len(horizonal_max_ratios)):
            horizonal_max_ratios_converted[i + 1] = horizonal_max_ratios[i] * _multiplor
            _multiplor = _multiplor * horizonal_max_ratios[i]
        
        # sorted horizonal_max_ratios_converted{} to find the max value of which block is the most max among all the blocks
        ratios_converted_sorted = sorted(horizonal_max_ratios_converted.items(), key=lambda item: item[1], reverse= True)
        _ultimate_max = ratios_converted_sorted[0]
        _ultimate_max_index = _ultimate_max[0]

        # for each horizonal block, convert every element to horizonal* element( horizonal* is the ideal case where if we are able to fetch data without 90-day restriction)
        for i in range(0,n_horizonal_blks): 
            if(i == _ultimate_max_index): 
                # if current max value of current block is exactly the ultimate max value of all blocks, the elements in this block remain unchanged
                if (i == n_horizonal_blks -1):
                    # if current horizonal block is the last horizonal unit, then we keep all the keywords in this dataframe
                    horizonal_list[i] = horizonal_list[i].iloc[:,:]
                else:
                    # if this is not the last horizonal unit, then we should always tease out the last keyword because we overlap in order to get the relative raio betweeen max values among blocks
                    horizonal_list[i] = horizonal_list[i].iloc[:,:-1]

                
            else:
                # if current index is not ultimate max value index
                """ insert the math fomula here """
                horizonal_list[i] = horizonal_list[i] * (horizonal_max_ratios_converted[i] / horizonal_max_ratios_converted[_ultimate_max_index])
                if (i == n_horizonal_blks -1):
                    # if current horizonal block is the last horizonal unit, then we keep all the keywords in this dataframe
                    horizonal_list[i] = horizonal_list[i].iloc[:,:]
                else:
                    # if this is not the last horizonal unit, then we should always tease out the last keyword because we overlap in order to get the relative raio betweeen max values among blocks
                    horizonal_list[i] = horizonal_list[i].iloc[:,:-1]

        result_df = pd.concat(horizonal_list, axis=1)

        # change column names to keyword original format according to kwDict
        result_df = result_df.rename(columns=kwDict)

        if(mode == "csv"):
            result_df.to_csv(outputCsvPath)
            
        elif(mode == "mysql-csv"):
            # convert the dataframe to mysql format
            with open(outputCsvPath, "a", encoding= "utf-8") as outputfile:
                outputfile.write("date,keyword,googleTrendIndex" + "\n")
                for kw in result_df.columns:            
                    for index, row in result_df.iterrows():
                        _date = index.strftime("%Y-%m-%d")
                        _gtrend = row[kw]
                        _kw = kw
                        outputfile.write(_date + "," + _kw + "," + str(_gtrend)  + "\n")
        else:
            print("ouput mode invalid... please retry")
    
    return


def getGoogleTrendsByKeywordsWeekly(keywords, startDate, endDate, outputCsvPath,  mode = "csv"):
    # This function writes google search trend values into csv file for a list of keywords
        # mode: 
            # = csv:write the dataframe into csv file directly
            # = mysql-csv: convert to a csv where each record contains (keyword_name, date, googleindex value)
    dataset = []
    pytrend = TrendReq(hl='en-GB')
    pytrend.build_payload(kw_list= keywords, cat= 0, timeframe= '{0} {1}'.format(startDate, endDate), geo= "GB")
    # pytrend.build_payload(kw_list= keywords, cat= 0, timeframe= 'all', geo= "GB")

    data = pytrend.interest_over_time()
    if not data.empty:
        data = data.drop(labels = ['isPartial'], axis = "columns")
        dataset.append(data)
   
    # prepare the output into one unified dataframe
    if(len(dataset)):
        googleDf = pd.concat(dataset, axis=0)
        if(mode == "csv"):
            googleDf.to_csv(outputCsvPath)
        elif(mode == "mysql-csv"):
            # convert the dataframe to mysql format
            with open(outputCsvPath, "a", encoding= "utf-8") as outputfile:
                # outputfile.write("date,keyword,googleTrendIndex" + "\n")
                for kw in keywords:            
                    for index, row in googleDf.iterrows():
                        _date = index.strftime("%Y-%m-%d")
                        _gtrend = row[kw]
                        _kw = kw
                        outputfile.write(_date + "," + _kw + "," + str(_gtrend)  + "\n")
        else:
            print("input mode invalid... please retry")
    else:
        print("No google index historical values found, function returns ")
        return
