import json, sys
import matplotlib.pyplot as plt
import datetime
from dateutil.parser import parse
from collections import Counter
from email.utils import parsedate_tz
import pandas as pd
import matplotlib

#filename = sys.argv[1]

class Return_TimeData(object):
    
    def __init__(self, hr, mn, sc):
        self.hr = hr
        self.mn = mn
        self.sc = sc

def to_datetime(datestring):
    time_tuple = parsedate_tz(datestring.strip())
    dt = datetime.datetime(*time_tuple[:6])
    return dt - datetime.timedelta(seconds=time_tuple[-1])

def Time_Analysis(filename):
    
    dates = []
    with open(filename, 'rU') as f:
        data = f.readlines()
        for line in data:            
            dates.append(to_datetime(json.loads(line)['created_at']))
            print json.loads(line)['created_at']
        
    tts_per_hr = Counter([x-datetime.timedelta(minutes=x.minute, seconds=x.second) for x in dates])
    tts_per_min = Counter([x-datetime.timedelta(seconds=x.second) for x in dates])
    tts_per_sec = Counter(dates)
    return Return_TimeData(sorted(tts_per_hr.iteritems()), 
                           sorted(tts_per_min.iteritems()), 
                           sorted(tts_per_sec.iteritems()))
