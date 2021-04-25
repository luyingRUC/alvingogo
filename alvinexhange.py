import datetime
import json 
import pattern.text.en as ptt_en
import difflib
import nltk.stem as ns
import numpy as np 


def read_exchangeRate_from_btc_to_usd(jasonPath):
    #  This function read in a json format file as the historical exchange rate between btc and usd
    #  return a dict, <tiemstamp, rate value>
    f = open(jasonPath)

    data = json.load(f)

    rates = data["bpi"]
    return rates