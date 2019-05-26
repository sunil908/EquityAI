# -*- coding: utf-8 -*-
"""
Created on Sat May 18 2019

@author: Gaurang
"""

from datetime import date
from datetime import timedelta
import pandas as pd
import talib
from nsepy.history import get_price_list
from sqlalchemy import create_engine
import matplotlib
matplotlib.use('PS')

#ta-lib library for analysis

holidaydf = pd.read_excel('HolidayList.xlsx', sheet_name='Sheet1')
holidaylist=[item.date() for item in holidaydf['Date'].tolist()]

start_date = date(2019,3,1)
end_date = date(2019,5,23)

filename = 'output'
script_start_date = "02-MAR-2019"
script_end_date = "23-MAY-2019"

def getNSEDailyQuote(start_date,end_date,filename):

    day_count = (end_date - start_date).days + 1
    one_day=timedelta(1,0,0)
    for dayloop in range(0,day_count,1):
        tradingdate = start_date + timedelta(dayloop,0,0)
        if(tradingdate in holidaylist or tradingdate.weekday() in (5,6)):
            continue
        print('trading date ->', tradingdate)
        prices = get_price_list(tradingdate)

        # writing to CSV
        prices.to_csv('{}.csv'.format(filename), index=False, mode='a',header=None) 


def readNSEDailyQuote(filename,stock_name,series='EQ',find_start_date=None,find_end_date=None):

    data = pd.read_csv('{}.csv'.format(filename),names= getNSEDailyQuoteColList(),dtype=setNSEDailyQuoteColList(),usecols=list(setNSEDailyQuoteColList().keys()))

    if stock_name:
        new_data = data.loc[(data['SYMBOL']=='{}'.format(stock_name)) & (data['SERIES']=='{}'.format(series))]
        
    if find_start_date and find_end_date:
        new_data = new_data.loc[(new_data['TIMESTAMP'] >= find_start_date) & (new_data['TIMESTAMP'] <= find_end_date)]

    return new_data

def getNSEDailyQuoteColList():
    col_list = ['SYMBOL','SERIES','OPEN','HIGH','LOW','CLOSE','LAST','PREVCLOSE','TOTTRDQTY','TOTTRDVAL','TIMESTAMP','TOTALTRADES','ISIN']
    return col_list

def setNSEDailyQuoteColList():
    dtypesdict = {'SYMBOL':'str','SERIES':'str','OPEN':'float','HIGH':'float','LOW':'float','CLOSE':'float','LAST':'float','PREVCLOSE':'float','TOTTRDQTY':'float','TOTTRDVAL':'float','TIMESTAMP':'str','TOTALTRADES':'int','ISIN':'str'}
    return dtypesdict

def applyADX(nsedailyquoteDF):
    
    adxdf = pd.Series(talib.ADX(nsedailyquoteDF['HIGH'].values, nsedailyquoteDF['LOW'].values, nsedailyquoteDF['CLOSE'].values, timeperiod = 14), index = nsedailyquoteDF.TIMESTAMP, name = 'ADX_%s' % str(14))
    print(adxdf)
    adxdf.to_csv('adx.csv',index=True) 

def applyADXR(nsedailyquoteDF):

    adxrdf = pd.Series(talib.ADXR(nsedailyquoteDF['HIGH'].values, nsedailyquoteDF['LOW'].values, nsedailyquoteDF['CLOSE'].values, timeperiod = 14), index = nsedailyquoteDF.TIMESTAMP, name = 'ADX_%s' % str(14))
    return adxrdf

def applyAPO(nsedailyquoteDF):

    apodf = pd.Series(talib.APO(nsedailyquoteDF['CLOSE'].values, fastperiod=12, slowperiod=26, matype=0), index = nsedailyquoteDF.TIMESTAMP, name = 'ADX_%s' % str(14))
    return apodf

def applyAROONOSC(nsedailyquoteDF):

    arronoscdf = pd.Series(talib.AROONOSC(nsedailyquoteDF['HIGH'].values, nsedailyquoteDF['LOW'].values, timeperiod = 14), index = nsedailyquoteDF.TIMESTAMP, name = 'ADX_%s' % str(14))
    return arronoscdf

def applyCCI(nsedailyquoteDF):

    ccidf = pd.Series(talib.CCI(nsedailyquoteDF['HIGH'].values, nsedailyquoteDF['LOW'].values, nsedailyquoteDF['CLOSE'].values, timeperiod = 14), index = nsedailyquoteDF.TIMESTAMP, name = 'ADX_%s' % str(14))
    return ccidf

# getNSEDailyQuote(start_date,end_date,filename)
nsedailyquoteDF = readNSEDailyQuote(filename,'RELIANCE',find_start_date=script_start_date,find_end_date=script_end_date)
# print(nsedailyquoteDF)
print(applyADX(nsedailyquoteDF))
# readNSEDailyQuote(filename,'SBIN',find_start_date=script_start_date,find_end_date=script_end_date)