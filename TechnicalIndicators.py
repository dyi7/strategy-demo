# -*- coding: utf-8 -*-
"""
Created on Wed  Nov 1 15:31:01 2023

@author: Deng Yiqi
"""

import numpy as np
import pandas as pd


## Trend Indicators
def moving_average(df,n):
        " n-day simple moving average of close price " 
        MA = pd.Series(df['last'].rolling(n,min_periods = n).mean(),name = 'MA_{}'.format(n))
        return MA
   
    
def exponential_moving_average(df,n):
        " n-day exponential moving average of close price " 
        EMA = pd.Series(df['last'].ewm(span=n,min_periods=n).mean(),name='EMA_{}'+ str(n))
        return EMA
  
    
def triangular_moving_average(df,n):
        " n-day triangular moving average of close price " 
        TMA = pd.Series(moving_average(df,n).rolling(n,min_periods=n).mean(),name = 'TMA_{}'+ str(n))
        return TMA


def macd(dataset):
    EMA12 = pd.Series(dataset['last'].ewm(span= 12).mean()) #2 weeks
    EMA26 = pd.Series(dataset['last'].ewm(span= 26).mean()) #1 month
    dataset['MACD'] = (EMA12-EMA26)
    return dataset




def trix(df, n):
    """Calculate TRIX for given data.
    
    :param df: pandas.DataFrame
    :param n: data window
    :return: pandas.DataFrame
    :range: oscillate around 0
    """
    EX1 = df['last'].ewm(span=n, min_periods=n).mean()
    EX2 = EX1.ewm(span=n, min_periods=n).mean()
    EX3 = EX2.ewm(span=n, min_periods=n).mean()
    i = 0
    ROC_l = [np.nan]
    while i + 1 <= df.index[-1]:
        ROC = (EX3[i + 1] - EX3[i]) / EX3[i] * 100
        ROC_l.append(ROC)
        i = i + 1
    Trix = pd.Series(ROC_l, name='Trix_' + str(n))
    return Trix




## 2 Volatility Indicators
def bollinger_bands(dataset, moving_average, pe): #pe=20
    """
    
    :range: almost price
    """
    # Create Bollinger Bands
    dataset['20sd'] = pd.Series(dataset['last'].rolling(window = pe).std())
    dataset['MA20'] = moving_average(dataset, pe)
    dataset['upper_band'] = dataset['MA20'] + (dataset['20sd'] * 2)
    dataset['lower_band'] = dataset['MA20'] - (dataset['20sd'] * 2)
    return dataset    



def standard_deviation(df, n):
    """Calculate Standard Deviation for given data.
    
    :param df: pandas.DataFrame
    :param n: data window
    :return: pandas.DataFrame
    """
    std = pd.Series(df['last'].rolling(n, min_periods=n).std(), name='STD_' + str(n))
    return std



### 3 Volume Indicators
    
def volume_moving_average(df,n):
    VMA = pd.Series(df['volume'].rolling(n,min_periods = n).mean(),name = 'VMA_{}'.format(n))
    return VMA
    


def force_index(df, n):
    """Calculate Force Index for given data.
    
    :param df: pandas.DataFrame
    :param n: data window
    :return: pandas.DataFrame
    """
    F = pd.Series(df['last'].diff(n) * df['volume'].diff(n), name='Force_' + str(n))
    return F


def on_balance_volume(df, n):
    """Calculate On-Balance Volume for given data.
    
    :param df: pandas.DataFrame
    :param n: data window
    :return: pandas.DataFrame
    """
    i = 0
    OBV = [0]
    while i < df.index[-1]:
        if df.loc[i + 1, 'last'] - df.loc[i, 'last'] > 0:
            OBV.append(df.loc[i + 1, 'Volume'])
        if df.loc[i + 1, 'last'] - df.loc[i, 'last'] == 0:
            OBV.append(0)
        if df.loc[i + 1, 'last'] - df.loc[i, 'last'] < 0:
            OBV.append(-df.loc[i + 1, 'volume'])
        i = i + 1
    OBV = pd.Series(OBV)
    OBV_ma = pd.Series(OBV.rolling(n, min_periods=n).mean(), name='OBV_' + str(n))
    return OBV_ma



# 4 Momentum Indicators
  
def true_strength_index(df, r, s):
    """Calculate True Strength Index (TSI) for given data.
    
    :param df: pandas.DataFrame
    :param r: 
    :param s: 
    :return: pandas.DataFrame
    """
    M = pd.Series(df['last'].diff(1))
    aM = abs(M)
    EMA1 = pd.Series(M.ewm(span=r, min_periods=r).mean())
    aEMA1 = pd.Series(aM.ewm(span=r, min_periods=r).mean())
    EMA2 = pd.Series(EMA1.ewm(span=s, min_periods=s).mean())
    aEMA2 = pd.Series(aEMA1.ewm(span=s, min_periods=s).mean())
    TSI = pd.Series(EMA2 / aEMA2, name='TSI_' + str(r) + '_' + str(s)) * 100
    return TSI



def momentum(df,n):
    ' Momentum close price '
    M = pd.Series(df['last'].diff(n),name='Momentum_' + str(n))
    return M
 

def rate_of_change(df, n):
    """
    :param df: pandas.DataFrame
    :param n: data window
    :return: pandas.DataFrame
    """
    M = df['last'].diff(n - 1)
    N = df['last'].shift(n - 1)
    ROC = pd.Series(M / N, name='ROC_' + str(n)) *100
    return ROC
    
    
        
# MA5 = MovingAverage(df,5)
# MA10 = MovingAverage(df,10)
# MA15 = MovingAverage(df,15)
# EMA5 = ExponentialMovingAverage(df,5)
# EMA10 = ExponentialMovingAverage(df,10)
# EMA15 = ExponentialMovingAverage(df,15)
# TMA5 = TriangularMovingAverage(df,5)
# Mom5 = Momentum(df,5)
    












