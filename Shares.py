#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd
import numpy as np
from technical_indicators_lib import *
import yfinance as yf
import math
import matplotlib.pyplot as plt
from williamsR import *
from Database import *
from analyzing_algorithms import *
from operator import itemgetter


# In[16]:


# Simple Average Movement 
def get_smas(stocks, names, period):
    # Erstellen des SMAs (Periode in den variablen übergeben)
    sma = SMA()
    for stock in stocks:
        stock = sma.get_value_df(stock, period)
    #print(stocks)
    add_buy_and_sell_sma(stocks)
    #print_smas(stocks, names)
    
    
# Methode zum bewerten der SMA Ergebnisse 
def add_buy_and_sell_sma(stocks):
    for stock in stocks:
        stock.dropna(subset = ["close"], inplace=True)
        # variable um den allgemeinen trend zu erfragen (hold, buy, sell)
        trend = [] 
        # Alle Tage an denen gebuyt wird werden mit dem Aktienkurs aufgefüllt, sonst nan
        helper_buy = []
        # Alle Tage an denen gesellt wird werden mit dem Aktienkurs aufgefüllt, sonst nan
        helper_sell = []
        flag = 0
        days_signal_persists = 0
        for day in stock.index:
            # wenn undefinierte Werte erscheinen machen wir nichts
            if math.isnan(stock["SMA"][day]): 
                helper_buy.append(np.nan)
                helper_sell.append(np.nan)
                trend.append("hold")
            else:    
                # wenn der Aktienkurs über dem Durchschnitt (SMA) liegt
                if stock["close"][day] >= stock["SMA"][day]:
                    # Prüdung, ob wir vorher ein Buy oder Sell Rating gegeben haben (Wichtig um nachzuvollziehen wie viele tage ein Signal besteht)
                    if flag == 0: # flag == 0 bedeutet vorher ein Sell
                        # Das signal besteht zum 0ten Tag
                        days_signal_persists = 0
                        # Keine Aussagekraft, daher ein hold
                        helper_buy.append(np.nan)
                        helper_sell.append(np.nan)
                        trend.append("hold")
                        flag = 1
                    else:
                        # wenn wir vorher schon im Buy waren, wird tage an dem signal besteht erhöht
                        days_signal_persists+=1
                        # wenn wir lange genug ein Signal haben kaufen wir
                        if days_signal_persists >= 1:
                            helper_buy.append(stock["close"][day])
                            helper_sell.append(np.nan)
                            trend.append("buy")
                        else:
                            # sonst halten wir
                            helper_sell.append(np.nan)
                            helper_buy.append(np.nan)
                            trend.append("hold")        
                # wenn der Kurs unter dem Durchschnitt ist
                if stock["close"][day] < stock["SMA"][day]:
                    # Abprüfung aus welchem Bereich wir kommen
                    if flag == 1:
                        # Zurücksetzen des Counters, und hold als Wert zuweisen
                        days_signal_persists=0
                        helper_buy.append(np.nan)
                        helper_sell.append(np.nan)
                        trend.append("hold")
                        flag = 0
                    else:
                        # wenn das signal lange genug besteht, verkaufen wir
                        days_signal_persists+=1
                        if days_signal_persists >= 1: 
                            helper_buy.append(np.nan)
                            helper_sell.append(stock["close"][day])
                            trend.append("sell")
                        else:
                            # sonst nicht
                            helper_sell.append(np.nan)
                            helper_buy.append(np.nan)
                            trend.append("hold")  
        # hinzufügen der Kaufempfehlungen an das Dataframe
        stock["sma_buy"] = helper_buy
        stock["sma_sell"] = helper_sell
        stock["sma_trend"] = trend
        
# funktion zum Ausgeben der Aktie
def print_smas(stocks, names):
    counter = 0
    for stock in stocks:
        fig, ax = plt.subplots(figsize=(15,10))  # Create a figure and an axes.
        ax.plot(stock["close"], label="close")  # Plot some data on the axes.
        ax.plot(stock["sma_buy"], label="buy", marker=10, color="g")
        ax.plot(stock["sma_sell"], label="sell", marker=11, color="r")
        ax.plot(stock["SMA"], label="sma", color="y")
        ax.set_xlabel('Time')  # Add an x-label to the axes.
        ax.set_ylabel('Value')  # Add a y-label to the axes.
        ax.set_title("SMA of "+names[counter])  # Add a title to the axes.
        ax.legend()  # Add a legend.
        counter+=1


# In[17]:


def get_sma_ema(stocks, names, period):
    for stock in stocks:
        # variable um den allgemeinen trend zu erfragen (hold, buy, sell)
        trend = [] 
        # Alle Tage an denen gebuyt wird werden mit dem Aktienkurs aufgefüllt, sonst nan
        helper_buy = []
        # Alle Tage an denen gesellt wird werden mit dem Aktienkurs aufgefüllt, sonst nan
        helper_sell = []
        flag = 0
        days_signal_persists = 0
        for day in stock.index:
            # wenn undefinierte Werte erscheinen machen wir nichts
            if math.isnan(stock["SMA"][day]) or math.isnan(stock["EMA"][day]): 
                helper_buy.append(np.nan)
                helper_sell.append(np.nan)
                trend.append("hold")
            else:    
                # wenn der Aktienkurs über dem Durchschnitt (SMA) liegt
                if stock["SMA"][day] >= stock["EMA"][day]:
                    # Prüdung, ob wir vorher ein Buy oder Sell Rating gegeben haben (Wichtig um nachzuvollziehen wie viele tage ein Signal besteht)
                    if flag == 0: # flag == 0 bedeutet vorher ein Sell
                        # Das signal besteht zum 0ten Tag
                        days_signal_persists = 0
                        # Keine Aussagekraft, daher ein hold
                        helper_buy.append(np.nan)
                        helper_sell.append(np.nan)
                        trend.append("hold")
                        flag = 1
                    else:
                        # wenn wir vorher schon im Buy waren, wird tage an dem signal besteht erhöht
                        days_signal_persists+=1
                        # wenn wir lange genug ein Signal haben kaufen wir
                        if days_signal_persists >= 2:
                            helper_buy.append(stock["close"][day])
                            helper_sell.append(np.nan)
                            trend.append("buy")
                        else:
                            # sonst halten wir
                            helper_sell.append(np.nan)
                            helper_buy.append(np.nan)
                            trend.append("hold")        
                # wenn der Kurs unter dem Durchschnitt ist
                if stock["SMA"][day] < stock["EMA"][day]:
                    # Abprüfung aus welchem Bereich wir kommen
                    if flag == 1:
                        # Zurücksetzen des Counters, und hold als Wert zuweisen
                        days_signal_persists=0
                        helper_buy.append(np.nan)
                        helper_sell.append(np.nan)
                        trend.append("hold")
                        flag = 0
                    else:
                        # wenn das signal lange genug besteht, verkaufen wir
                        days_signal_persists+=1
                        if days_signal_persists >= 2: 
                            helper_buy.append(np.nan)
                            helper_sell.append(stock["close"][day])
                            trend.append("sell")
                        else:
                            # sonst nicht
                            helper_sell.append(np.nan)
                            helper_buy.append(np.nan)
                            trend.append("hold")  
        # hinzufügen der Kaufempfehlungen an das Dataframe
        stock["sma_ema_buy"] = helper_buy
        stock["sma_ema_sell"] = helper_sell
        stock["sma_ema_trend"] = trend
        
   # counter = 0
   # for stock in stocks:
   #     fig, ax = plt.subplots(figsize=(15,10))  # Create a figure and an axes.
   #     ax.plot(stock["close"], label="close")  # Plot some data on the axes.
   #     ax.plot(stock["sma_ema_buy"], label="buy", marker=10, color="g")
   #     ax.plot(stock["sma_ema_sell"], label="sell", marker=11, color="r")
   #     ax.plot(stock["SMA"], label="sma", color="y")
   #     ax.plot(stock["EMA"], label="ema", color="b")
   #     ax.set_xlabel('Time')  # Add an x-label to the axes.
   #     ax.set_ylabel('Value')  # Add a y-label to the axes.
   ##     ax.set_title("SMA and EMA of "+names[counter])  # Add a title to the axes.
    #    ax.legend()  # Add a legend.
    #    counter+=1


# In[18]:


# WilliamsR

def get_wr(stocks, names, period):
    wr = WilliamsR()
    for stock in stocks:
        stock = wr.get_value_df(stock, period)
    #print(stocks)
    add_buy_and_sell_wr(stocks)
    #print_wr(stocks, names)

def add_buy_and_sell_wr(stocks):
     for stock in stocks:
        trend = []
        helper_buy = []
        helper_sell = []
        flag = 0
        days_signal_persists = 0
        for day in stock.index:
            if math.isnan(stock["WilliamsR"][day]): 
                helper_buy.append(np.nan)
                helper_sell.append(np.nan)
                trend.append("hold")
            else:    
                if stock["WilliamsR"][day] <= -80:
                    if flag == 0:
                        days_signal_persists = 0
                        helper_buy.append(np.nan)
                        helper_sell.append(np.nan)
                        flag = 1
                        trend.append("hold")
                    else:
                        days_signal_persists+=1
                        if days_signal_persists >= 2 and days_signal_persists < 7:
                            helper_buy.append(stock["close"][day])
                            helper_sell.append(np.nan)
                            trend.append("buy")
                        else:
                            helper_buy.append(np.nan)
                            helper_sell.append(np.nan)
                            trend.append("hold")
                if stock["WilliamsR"][day] >= -20:
                    if flag == 1:
                        days_signal_persists = 0
                        helper_sell.append(np.nan)
                        helper_buy.append(np.nan)
                        trend.append("hold")
                        flag = 0
                    else:
                        days_signal_persists+=1
                        if days_signal_persists >= 2 and days_signal_persists < 7:
                            helper_buy.append(np.nan)
                            helper_sell.append(stock["close"][day])
                            trend.append("sell")
                        else:
                            helper_buy.append(np.nan)
                            helper_sell.append(np.nan)
                            trend.append("hold")                        
                if  stock["WilliamsR"][day] > -80 and stock["WilliamsR"][day] < -20:
                    helper_sell.append(np.nan)
                    helper_buy.append(np.nan)
                    trend.append("hold")
        stock["wr_buy"] = helper_buy
        stock["wr_sell"] = helper_sell
        stock["wr_trend"] = trend

def print_wr(stocks, names):
    counter = 0
    for stock in stocks:
        fig, ax = plt.subplots(2,figsize=(15,10))  # Create a figure and an axes.
        ax[0].plot(stock["close"], label="close")  # Plot some data on the axes.
        ax[0].plot(stock["wr_buy"], label="buy", marker=10, color="g")
        ax[0].plot(stock["wr_sell"], label="sell", marker=11, color="r")
        ax[0].set_xlabel('Time')  # Add an x-label to the axes.
        ax[0].set_ylabel('Value')  # Add a y-label to the axes.
        ax[0].set_title("WR of "+names[counter])  # Add a title to the axes.
        ax[0].legend()  # Add a legend.
        ax[1].plot(stock["WilliamsR"], label="WR")  # Plot some data on the axes.
        ax[1].set_xlabel('Time')  # Add an x-label to the axes.
        ax[1].set_ylabel('Value')  # Add a y-label to the axes.
        ax[1].legend()  # Add a legend.
        counter+=1


# In[19]:


# Relative Strength Index

def get_rsi(stocks, names, period):
    rsi = RSI()
    for stock in stocks:
        stock = rsi.get_value_df(stock, period)
    #print(stocks)
    add_buy_and_sell_rsi(stocks)
    #print_rsi(stocks, names)

def add_buy_and_sell_rsi(stocks):
     for stock in stocks:
        trend = []
        helper_buy = []
        helper_sell = []
        flag = 0
        days_signal_persists = 0
        for day in stock.index:
            if math.isnan(stock["RSI"][day]): 
                helper_buy.append(np.nan)
                helper_sell.append(np.nan)
                trend.append("hold")
            else:    
                if stock["RSI"][day] <= 30:
                    if flag == 0:
                        days_signal_persists = 0
                        helper_buy.append(np.nan)
                        helper_sell.append(np.nan)
                        flag = 1
                        trend.append("hold")
                    else:
                        days_signal_persists+=1
                        if days_signal_persists >= 2 and days_signal_persists < 7:
                            helper_buy.append(stock["close"][day])
                            helper_sell.append(np.nan)
                            trend.append("buy")
                        else:
                            helper_buy.append(np.nan)
                            helper_sell.append(np.nan)
                            trend.append("hold")
                if stock["RSI"][day] >= 70:
                    if flag == 1:
                        days_signal_persists = 0
                        helper_sell.append(np.nan)
                        helper_buy.append(np.nan)
                        trend.append("hold")
                        flag = 0
                    else:
                        days_signal_persists+=1
                        if days_signal_persists >= 2 and days_signal_persists < 7:
                            helper_buy.append(np.nan)
                            helper_sell.append(stock["close"][day])
                            trend.append("sell")
                        else:
                            helper_buy.append(np.nan)
                            helper_sell.append(np.nan)
                            trend.append("hold")                        
                if  stock["RSI"][day] < 70 and stock["RSI"][day] > 30:
                    helper_sell.append(np.nan)
                    helper_buy.append(np.nan)
                    trend.append("hold")
        stock["rsi_buy"] = helper_buy
        stock["rsi_sell"] = helper_sell
        stock["rsi_trend"] = trend

def print_rsi(stocks, names):
    counter = 0
    for stock in stocks:
        fig, ax = plt.subplots(2,figsize=(15,10))  # Create a figure and an axes.
        ax[0].plot(stock["close"], label="close")  # Plot some data on the axes.
        ax[0].plot(stock["rsi_buy"], label="buy", marker=10, color="g")
        ax[0].plot(stock["rsi_sell"], label="sell", marker=11, color="r")
        ax[0].set_xlabel('Time')  # Add an x-label to the axes.
        ax[0].set_ylabel('Value')  # Add a y-label to the axes.
        ax[0].set_title("RSI of "+names[counter])  # Add a title to the axes.
        ax[0].legend()  # Add a legend.
        ax[1].plot(stock["RSI"], label="RSI")  # Plot some data on the axes.
        ax[1].set_xlabel('Time')  # Add an x-label to the axes.
        ax[1].set_ylabel('Value')  # Add a y-label to the axes.
        ax[1].legend()  # Add a legend.
        counter+=1


# In[20]:


# MACD
def get_macd(stocks, names, period):
    macd = MACD()
    for stock in stocks:
        stock = macd.get_value_df(stock, 12, 26, True, 9)
    #print(stocks)
    add_buy_and_sell_macd(stocks)
    #print_macd(stocks, names)

    # macd needs both holds since only crosses are taking effect

def add_buy_and_sell_macd(stocks):
     for stock in stocks:
        trend = []
        helper_buy = []
        helper_sell = []
        flag = 0
        days_signal_persists = 0
        for day in stock.index:
            if math.isnan(stock["MACD_signal_line"][day]) or math.isnan(stock["MACD"][day]): 
                helper_buy.append(np.nan)
                helper_sell.append(np.nan)
                trend.append("hold")
            else:   
                    if (stock["MACD"][day] <= stock["MACD_signal_line"][day]):
                        if flag == 1:
                            days_signal_persists=0
                            helper_sell.append(np.nan)
                            helper_buy.append(np.nan)
                            trend.append("hold")
                            flag = 0
                        else:
                            days_signal_persists+=1
                            if days_signal_persists >= 3:
                                helper_buy.append(np.nan)
                                helper_sell.append(stock["close"][day])
                                trend.append("sell")
                            else:
                                helper_sell.append(np.nan)
                                helper_buy.append(np.nan)
                                trend.append("hold")                                
                    elif stock["MACD"][day] > stock["MACD_signal_line"][day]:                               
                        if flag == 0:
                            days_signal_persists = 0
                            helper_buy.append(np.nan)
                            helper_sell.append(np.nan)
                            flag = 1
                            trend.append("hold")
                        else:
                            days_signal_persists+=1
                            if days_signal_persists >= 3:
                                helper_buy.append(stock["close"][day])
                                helper_sell.append(np.nan)
                                trend.append("buy")
                            else:
                                helper_sell.append(np.nan)
                                helper_buy.append(np.nan)
                                trend.append("hold")
        stock["macd_buy"] = helper_buy
        stock["macd_sell"] = helper_sell
        stock["macd_trend"] = trend
def print_macd(stocks, names):
    counter = 0
    for stock in stocks:
        fig, ax = plt.subplots(2,figsize=(15,10))  # Create a figure and an axes.
        ax[0].plot(stock["close"], label="close")  # Plot some data on the axes.
        ax[0].plot(stock["macd_buy"], label="buy", marker=10, color="g")
        ax[0].plot(stock["macd_sell"], label="sell", marker=11, color="r")
        ax[0].set_xlabel('Time')  # Add an x-label to the axes.
        ax[0].set_ylabel('Value')  # Add a y-label to the axes.
        ax[0].set_title("MACD of "+names[counter])  # Add a title to the axes.
        ax[0].legend()  # Add a legend.
        ax[1].plot(stock["MACD"], label="MACD")  # Plot some data on the axes.
        ax[1].plot(stock["MACD_signal_line"], label="signal line")  # Plot some data on the axes.
        ax[1].set_xlabel('Time')  # Add an x-label to the axes.
        ax[1].set_ylabel('Value')  # Add a y-label to the axes.
        ax[1].legend()  # Add a legend.
        counter+=1


# In[21]:


# EMA EMA
def get_ema(stocks, names, period):
    ema = EMA()
    for stock in stocks:
        stock = ema.get_value_df(stock, period)
    add_buy_and_sell_ema(stocks)
    #print_ema(stocks, names)
        
def add_buy_and_sell_ema(stocks):
     for stock in stocks:
        stock.dropna(subset = ["close"], inplace=True)
        #stock = stock.resample('1D').interpolate()
        trend = []
        helper_buy = []
        helper_sell = []
        flag = 0
        days_signal_persists = 0
        for day in stock.index:
            if math.isnan(stock["EMA"][day]): 
                helper_buy.append(np.nan)
                helper_sell.append(np.nan)
                trend.append("hold")
            else:    
                if stock["EMA"][day] <= stock["close"][day]:
                    if flag == 0:
                        days_signal_persists = 0
                        helper_buy.append(np.nan)
                        helper_sell.append(np.nan)
                        trend.append("hold")
                        flag = 1
                    else:
                        days_signal_persists+=1
                        if days_signal_persists >= 1:
                            helper_buy.append(stock["close"][day])
                            helper_sell.append(np.nan)
                            trend.append("buy")
                        else:
                            helper_sell.append(np.nan)
                            helper_buy.append(np.nan)
                            trend.append("hold")        
                elif stock["EMA"][day] > stock["close"][day]:
                    if flag == 1:
                        days_signal_persists = 0
                        helper_sell.append(np.nan)
                        helper_buy.append(np.nan)
                        trend.append("hold")
                        flag = 0
                    else:
                        days_signal_persists+=1
                        if days_signal_persists >= 1:
                            helper_buy.append(np.nan)
                            helper_sell.append(stock["close"][day])
                            trend.append("sell")
                        else:
                            helper_sell.append(np.nan)
                            helper_buy.append(np.nan)
                            trend.append("hold")  
        #print("helper - "+str(len(helper_buy)))
        #if len(stock["close"]) > len(helper_buy):
            
        stock["ema_buy"] = helper_buy
        stock["ema_sell"] = helper_sell
        stock["ema_trend"] = trend
        
def print_ema(stocks, names):
    counter = 0
    for stock in stocks:
        fig, ax = plt.subplots(figsize=(15,10))  # Create a figure and an axes.
        ax.plot(stock["close"], label="close")  # Plot some data on the axes.
        ax.plot(stock["ema_buy"], label="buy", marker=10, color="g")
        ax.plot(stock["ema_sell"], label="sell", marker=11, color="r")
        ax.plot(stock["EMA"], label="ema", color="y")
        ax.set_xlabel('Time')  # Add an x-label to the axes.
        ax.set_ylabel('Value')  # Add a y-label to the axes.
        ax.set_title("EMA of "+names[counter])  # Add a title to the axes.
        ax.legend()  # Add a legend.
        counter+=1


# In[22]:


# Stochastik StochasticKAndD
def get_stoch(stocks, names, period):
    stoch = StochasticKAndD()
    for stock in stocks:
        stock = stoch.get_value_df(stock, period)
    #print(stocks)
    add_buy_and_sell_stoch(stocks)
    #print_stoch(stocks, names)


def add_buy_and_sell_stoch(stocks):
     for stock in stocks:
        trend = []
        helper_buy = []
        helper_sell = []
        flag = 0
        days_signal_persists = 0
        for day in stock.index:
            if math.isnan(stock["stoc_d"][day]) or math.isnan(stock["stoc_k"][day]): 
                helper_buy.append(np.nan)
                helper_sell.append(np.nan)
                trend.append("hold")
            else:   
                if stock["stoc_k"][day] <= 20 or stock["stoc_d"][day] <= 20:
                    if flag == 0:
                        days_signal_persists = 0
                        helper_buy.append(np.nan)
                        helper_sell.append(np.nan)
                        flag = 1
                        trend.append("hold")
                    else:
                        days_signal_persists+=1
                        if days_signal_persists >= 2 and days_signal_persists < 7:
                            helper_buy.append(stock["close"][day])
                            helper_sell.append(np.nan)
                            trend.append("buy")
                        else:
                            helper_sell.append(np.nan)
                            helper_buy.append(np.nan)
                            trend.append("hold")        
                elif stock["stoc_k"][day] >= 80 or stock["stoc_d"][day] >= 80:
                    if flag == 1:
                        days_signal_persists = 0
                        helper_sell.append(np.nan)
                        helper_buy.append(np.nan)
                        trend.append("hold")
                        flag = 0
                    else:
                        days_signal_persists+=1
                        if days_signal_persists >= 2 and days_signal_persists < 7:
                            helper_buy.append(np.nan)
                            helper_sell.append(stock["close"][day])
                            trend.append("sell")
                        else:
                            helper_sell.append(np.nan)
                            helper_buy.append(np.nan)
                            trend.append("hold")        
                else:
                    helper_buy.append(np.nan)
                    helper_sell.append(np.nan)
                    trend.append("hold")
        stock["stoch_buy"] = helper_buy
        stock["stoch_sell"] = helper_sell
        stock["stoch_trend"] = trend
        
def print_stoch(stocks, names):
    counter = 0
    for stock in stocks:
        fig, ax = plt.subplots(2, figsize=(15,10))  # Create a figure and an axes.
        ax[0].plot(stock["close"], label="close")  # Plot some data on the axes.
        ax[0].plot(stock["stoch_buy"], label="buy", marker=10, color="g")
        ax[0].plot(stock["stoch_sell"], label="sell", marker=11, color="r")
        ax[0].set_xlabel('Time')  # Add an x-label to the axes.
        ax[0].set_ylabel('Value')  # Add a y-label to the axes.
        ax[0].set_title("Stochastik K%D of "+names[counter])  # Add a title to the axes.
        ax[0].legend()  # Add a legend.
        ax[1].plot(stock["stoc_d"], label="stoc_d")  # Plot some data on the axes.
        ax[1].plot(stock["stoc_k"], label="stoc_k")  # Plot some data on the axes.
        ax[1].set_xlabel('Time')  # Add an x-label to the axes.
        ax[1].set_ylabel('Value')  # Add a y-label to the axes.
        ax[1].legend()  # Add a legend.
        counter+=1


# In[23]:


# OBV (on balance volume)

def get_obv(stocks, names, period):
    obv = OBV()
    for stock in stocks:
        stock = obv.get_value_df(stock)
    #print(stocks)
    add_average_obv(stocks, period)
    add_buy_and_sell_obv(stocks)
    #print_obv(stocks, names)

def add_average_obv(stocks, period):
    for stock in stocks:
        lookback = period
        values = []
        length = len(stock["close"])
        for day in range(length):
            if day <= lookback:
                values.append(np.nan)
            else:
                helper = stock[day-lookback:day]["OBV"].values
                values.append(np.mean(helper))
        stock["OBV_average"] = values

def add_buy_and_sell_obv(stocks):
     for stock in stocks:
        trend = []
        helper_buy = []
        helper_sell = []
        flag = 0
        days_signal_persists = 0
        length = len(stock["close"])
        for day in range (length):
            if not np.isnan(stock["OBV_average"][day]) and not np.isnan(stock["OBV_average"][day-1]): 
                # korridore hinzufügen etwa 10 % schewankung soll auf  hold fallen ( wenn volumen mehr als 5 % mehr ist dann erst buy, oder eben sell)
                if stock["OBV"][day] >= 1.05*stock["OBV_average"][day-1]:
                    if flag == 0:
                        days_signal_persists = 0
                        helper_buy.append(np.nan)
                        helper_sell.append(np.nan)
                        flag = 1
                        trend.append("hold")
                    else:
                        days_signal_persists+=1
                        if days_signal_persists >= 1:
                            helper_buy.append(stock["close"][day])
                            helper_sell.append(np.nan)
                            trend.append("buy")
                        else:
                            helper_sell.append(np.nan)
                            helper_buy.append(np.nan)
                            trend.append("hold")        
                elif stock["OBV"][day] < 0.95*stock["OBV_average"][day-1]:
                    if flag == 1:
                        days_signal_persists = 0
                        helper_sell.append(np.nan)
                        helper_buy.append(np.nan)
                        trend.append("hold")
                        flag = 0
                    else:
                        days_signal_persists+=1
                        if days_signal_persists >= 1:
                            helper_buy.append(np.nan)
                            helper_sell.append(stock["close"][day])
                            trend.append("sell")
                        else:
                            helper_sell.append(np.nan)
                            helper_buy.append(np.nan)
                            trend.append("hold")   
                else:
                    helper_buy.append(np.nan)
                    helper_sell.append(np.nan)
                    trend.append("hold")
            else:
                helper_buy.append(np.nan)
                helper_sell.append(np.nan)
                trend.append("hold")
        stock["obv_buy"] = helper_buy
        stock["obv_sell"] = helper_sell
        stock["obv_trend"] = trend
        
def print_obv(stocks, names):
    counter = 0
    for stock in stocks:
        fig, ax = plt.subplots(2, figsize=(15,10))  # Create a figure and an axes.
        ax[0].plot(stock["close"], label="close")  # Plot some data on the axes.
        ax[0].plot(stock["obv_buy"], label="buy", marker=10, color="g")
        ax[0].plot(stock["obv_sell"], label="sell", marker=11, color="r")
        ax[0].set_xlabel('Time')  # Add an x-label to the axes.
        ax[0].set_ylabel('Value')  # Add a y-label to the axes.
        ax[0].set_title("reccomandations from OBV for "+names[counter])  # Add a title to the axes.
        ax[0].legend()  # Add a legend.
        ax[1].plot(stock["OBV"], label="OBV")  # Plot some data on the axes.
        ax[1].plot(stock["OBV_average"], label="average")  # Plot some data on the axes.
        ax[1].set_xlabel('Time')  # Add an x-label to the axes.
        ax[1].set_ylabel('Value')  # Add a y-label to the axes.
        ax[1].legend()  # Add a legend.
        counter+=1


# In[24]:


# Bolliunger bands

def get_bb(stocks, names, period):
    bb = BollingerBands()
    for stock in stocks:
        stock = bb.get_value_df(stock, period, 2)
    #print(stocks)
    add_buy_and_sell_bb(stocks)
    #print_bb(stocks, names)


def add_buy_and_sell_bb(stocks):
     for stock in stocks:
        trend = []
        helper_buy = []
        helper_sell = []
        flag = 0
        days_signal_persists = 0
        for day in stock.index:
            if math.isnan(stock["bb_lower"][day]) or math.isnan(stock["bb_upper"][day]): 
                helper_buy.append(np.nan)
                helper_sell.append(np.nan)
                trend.append("hold")
            else:   
                if stock["close"][day] <= 1.02*stock["bb_lower"][day]:
                    if flag == 0:
                        days_signal_persists = 0
                        helper_buy.append(np.nan)
                        helper_sell.append(np.nan)
                        flag = 1
                        trend.append("hold")
                    else:
                        days_signal_persists+=1
                        if days_signal_persists >= 1 and days_signal_persists <= 5:
                            helper_buy.append(stock["close"][day])
                            helper_sell.append(np.nan)
                            trend.append("buy")
                        else:
                            helper_sell.append(np.nan)
                            helper_buy.append(np.nan)
                            trend.append("hold")        
                elif stock["close"][day] >= 0.98*stock["bb_upper"][day]:
                    if flag == 1:
                        days_signal_persists = 0
                        helper_sell.append(np.nan)
                        helper_buy.append(np.nan)
                        trend.append("hold")
                        flag = 0
                    else:
                        days_signal_persists+=1
                        if days_signal_persists >= 1 and days_signal_persists <= 5:
                            helper_buy.append(np.nan)
                            helper_sell.append(stock["close"][day])
                            trend.append("sell")
                        else:
                            helper_sell.append(np.nan)
                            helper_buy.append(np.nan)
                            trend.append("hold")        
                else:
                    helper_buy.append(np.nan)
                    helper_sell.append(np.nan)
                    trend.append("hold")
        stock["bb_buy"] = helper_buy
        stock["bb_sell"] = helper_sell
        stock["bb_trend"] = trend
        
def print_bb(stocks, names):
    counter = 0
    for stock in stocks:
        fig, ax = plt.subplots(figsize=(15,10))  # Create a figure and an axes.
        ax.plot(stock["close"], label="close")  # Plot some data on the axes.
        ax.plot(stock["bb_buy"], label="buy", marker=10, color="g")
        ax.plot(stock["bb_sell"], label="sell", marker=11, color="r")
        ax.plot(stock["bb_upper"], label="upper", color="y")
        ax.plot(stock["bb_lower"], label="lower", color="m")
        ax.set_xlabel('Time')  # Add an x-label to the axes.
        ax.set_ylabel('Value')  # Add a y-label to the axes.
        ax.set_title("Recommendations from BB of "+names[counter])  # Add a title to the axes.
        ax.legend()  # Add a legend.
        counter+=1


# In[25]:


# create chart for displaying all indicators
def combine_indicators(permutation, stocks, names):
    counter=0
    for stock in stocks:
        print("Aktie "+str(counter))
        counter+=1
        # define all indicators and according values
        data=[stock["macd_trend"], stock["rsi_trend"], stock["sma_trend"], stock["ema_trend"], stock["stoch_trend"], stock["obv_trend"], stock["bb_trend"], stock["wr_trend"], stock["sma_ema_trend"]]
        headers=["macd_trend", "rsi_trend", "sma_trend", "ema_trend", "stoch_trend", "obv_trend", "bb_trend", "wr_trend", "sma_ema_trend"]
        # ctreate dataframe with only the indicators and recommandations in it
        helper = pd.concat(data, axis=1, keys=headers)
        length = len(data[0])
        weighted_signal = []
        buy_weak = []
        buy_middle = []
        buy_strong = []
        hold = []
        sell_weak = []
        sell_middle = []
        sell_strong = []
        for x in range(0,length):
            # for every day get indicator recommandation
            macd = helper.iloc[x]["macd_trend"]
            rsi = helper.iloc[x]["rsi_trend"]
            wr =  helper.iloc[x]["wr_trend"]
            bb = helper.iloc[x]["bb_trend"]
            stoch = helper.iloc[x]["stoch_trend"]
            sma = helper.iloc[x]["sma_trend"]
            ema = helper.iloc[x]["ema_trend"]
            sma_ema = helper.iloc[x]["sma_ema_trend"]
            obv = helper.iloc[x]["obv_trend"]
            signal_indicators=[rsi, wr, bb, stoch]
            trend_indicators=[macd, obv, sma, ema, sma_ema]
            decision = decide_perm(permutation, signal_indicators, trend_indicators)
            weighted_signal.append(decision[0])
            decision = decision[1]
            if decision == "buy_weak":
                buy_weak.append(stock.iloc[x]["close"])
                buy_middle.append(np.nan)
                buy_strong.append(np.nan)
                sell_weak.append(np.nan)
                sell_middle.append(np.nan)
                sell_strong.append(np.nan)
                hold.append(np.nan)
            if decision == "buy_middle":
                buy_middle.append(stock.iloc[x]["close"])
                buy_weak.append(np.nan)
                buy_strong.append(np.nan)
                sell_weak.append(np.nan)
                sell_middle.append(np.nan)
                sell_strong.append(np.nan)
                hold.append(np.nan)
            if decision == "buy_strong":
                buy_strong.append(stock.iloc[x]["close"])
                buy_middle.append(np.nan)
                buy_weak.append(np.nan)
                sell_weak.append(np.nan)
                sell_middle.append(np.nan)
                sell_strong.append(np.nan)
                hold.append(np.nan)
            if decision == "sell_weak":
                sell_weak.append(stock.iloc[x]["close"])
                buy_middle.append(np.nan)
                buy_weak.append(np.nan)
                buy_strong.append(np.nan)
                sell_middle.append(np.nan)
                sell_strong.append(np.nan)
                hold.append(np.nan)
            if decision == "sell_middle":
                sell_middle.append(stock.iloc[x]["close"])
                buy_middle.append(np.nan)
                buy_weak.append(np.nan)
                sell_weak.append(np.nan)
                buy_strong.append(np.nan)
                sell_strong.append(np.nan)
                hold.append(np.nan)
            if decision == "sell_strong":
                sell_strong.append(stock.iloc[x]["close"])
                buy_middle.append(np.nan)
                buy_weak.append(np.nan)
                sell_weak.append(np.nan)
                sell_middle.append(np.nan)
                buy_strong.append(np.nan)
                hold.append(np.nan)
            if decision == "hold":
                buy_middle.append(np.nan)
                buy_weak.append(np.nan)
                sell_weak.append(np.nan)
                sell_middle.append(np.nan)
                sell_strong.append(np.nan)
                buy_strong.append(np.nan)
                hold.append(stock.iloc[x]["close"])
        stock["buy_weak"] = buy_weak
        stock["buy_middle"] = buy_middle
        stock["buy_strong"] = buy_strong
        stock["sell_weak"] = sell_weak
        stock["sell_middle"] =sell_middle
        stock["hold"] = hold
        stock["sell_strong"] = sell_strong
        stock["weighted_signal"] = weighted_signal
    print("done")
    #print_all_perm(stocks,names)
            
def decide_perm(permutation, signal_indicators, trend_indicators):
    #trend_summe=sum(trend_indicators)
    #signal_summe=sum(signal_indicators)
    trend_rating = 0
    signal_rating = 0
    indicator_count = 0
    length = len(permutation)
    indicators=trend_indicators+signal_indicators
    
    signal_summe=sum(permutation[len(trend_indicators):])
    trend_summe=sum(permutation[:len(trend_indicators)])   
    
    
    # trend indicators
    for x in range(len(trend_indicators)):
        if indicators[x] == "buy":
            trend_rating+=permutation[x]
        if indicators[x] == "sell":
            trend_rating-=permutation[x]
        if indicators[x] == "hold":
            trend_rating=trend_rating            
    # signal indicators 
    for x in range(len(trend_indicators),len(indicators)):
        if indicators[x] == "buy":
            signal_rating+=permutation[x]
        if indicators[x] == "sell":
            signal_rating-=permutation[x]
        if indicators[x] == "hold":
            signal_rating=signal_rating            
    
    # sell if uptrend
    if trend_rating >= round(0.5*trend_summe):
        if signal_rating <= round(0.2*-signal_summe) and signal_rating > round(0.4*-signal_summe):
            return signal_rating, "sell_weak"
        elif signal_rating <= round(0.4*-signal_summe) and signal_rating > round(0.6*-signal_summe):
            return signal_rating, "sell_middle"
        elif signal_rating <= round(0.6*-signal_summe):
            return signal_rating, "sell_strong"
    # buy if down trend 
    elif trend_rating <= round(0.5*-trend_summe):
        if signal_rating >= round(0.2*signal_summe) and signal_rating < round(0.4*signal_summe):
            return signal_rating, "buy_weak"
        elif signal_rating >= round(0.4*signal_summe) and signal_rating < round(0.6*signal_summe):
            return signal_rating, "buy_middle"
        elif signal_rating >= round(0.6*signal_summe):
            return signal_rating, "buy_strong"
    
    return signal_rating,"hold"

def print_indicator(trade, indicators, length):
    print(trade)
    for x in range(length):
        if x == 0:
            if indicators[x] == "buy":
                print("MACD buy")
            elif indicators[x] == "sell":
                print("MACD sell")    
        elif x == 1:
            if indicators[x] == "buy":
                print("RSI buy")
            elif indicators[x] == "sell":
                print("RSI sell")
  
        elif x == 2:
            if indicators[x] == "buy":
                print("SMA buy")
            elif indicators[x] == "sell":
                print("SMA sell") 

        elif x == 3:
            if indicators[x] == "buy":
                print("EMA buy")
            elif indicators[x] == "sell":
                print("EMA sell")   

        elif x == 4:
            if indicators[x] == "buy":
                print("STOCH buy")
            elif indicators[x] == "sell":
                print("STOCH sell")
 
        elif x == 5:
            if indicators[x] == "buy":
                print("OBV buy")
            elif indicators[x] == "sell":
                print("OBV sell")

        elif x == 6:
            if indicators[x] == "buy":
                print("BB buy")
            elif indicators[x] == "sell":
                print("BB sell") 

        elif x == 7:
            if indicators[x] == "buy":
                print("WR buy")
            elif indicators[x] == "sell":
                print("WR sell")   
 
        elif x == 8:
            if indicators[x] == "buy":
                print("SMA-EMA buy")
            elif indicators[x] == "sell":
                print("SMA-EMA sell")     
            
    
def print_all_perm(stocks, names):
    counter = 0
    for stock in stocks:
        fig, ax = plt.subplots(figsize=(15,10))  # Create a figure and an axes.
        ax.plot(stock["close"], label="close")  # Plot some data on the axes.
        #ax.plot(stock["buy_weak"], label="buy_weak", marker=10, color="y")
        #ax.plot(stock["sell_weak"], label="sell_weak", marker=11, color="m")
        ax.plot(stock["buy_middle"], label="buy_middle", marker=10, color="c")
        ax.plot(stock["sell_middle"], label="sell_middle", marker=11, color="r")
        ax.plot(stock["buy_strong"], label="buy_strong", marker=10, color="g")
        ax.plot(stock["sell_strong"], label="sell_strong", marker=11, color="k")
        #ax.plot(stock["hold"], label="hold", marker=9, color="y")
        ax.set_xlabel('Time')  # Add an x-label to the axes.
        ax.set_ylabel('Value')  # Add a y-label to the axes.
        ax.set_title("All Indicators of "+names[counter])  # Add a title to the axes.
        ax.legend()  # Add a legend.
        counter+=1    


# In[26]:


def initialize_stocks(portfolio,days):
    stock_array=get_stocks_from_portfolio(portfolio)
    stocks=[]
    names=[]
    for stock in stock_array:
        name = stock[0]
        identifier = stock[1]
        ticker= yf.Ticker(identifier)
        hist = ticker.history(days)
        hist = hist.rename(columns={"Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"})
        stocks.append(hist)
        names.append(name)
    get_smas(stocks, names, 14)
    get_ema(stocks, names, 48)
    get_rsi(stocks, names, 21)
    get_macd(stocks, names, 21)
    get_stoch(stocks, names, 21)
    get_obv(stocks, names, 14)
    get_bb(stocks, names, 21)
    get_wr(stocks, names, 21)
    get_sma_ema(stocks, names,14)
    return stocks, names


# In[27]:


def get_stocks(portfolio, all_stocks, all_names):
    stock_array=get_stocks_from_portfolio(portfolio)
    names=[]
    stocks=[]
    print(stock_array)
    for stock in stock_array:
        names.append(stock[0])
    for name in names:
        for count in range(len(all_names)):
            if name == all_names[count]:
                stocks.append(all_stocks[count])
    return stocks, names      

def get_portfolio_data(portfolio, stocks, names):
    return get_stocks(portfolio, stocks, names)


# In[28]:


def calculate_day(portfolio):
    stocks, names= initialize_stocks(portfolio, "50d")
    max_stocks, max_names = get_portfolio_data(portfolio, stocks, names)
    permutation = [1, 1, 1, 1, 2, 1, 3, 2, 1]
    summe = sum(permutation[5:])
    combine_indicators(permutation, max_stocks, max_names)
    #return max_stocks
    buy_suggestions, sell_suggestions, portfolio_value, Startkapital = evaluate_day(summe,portfolio, max_stocks, max_names)
    print(buy_suggestions)
    print(sell_suggestions)
    print(portfolio_value)
    print(Startkapital)
    # mail stuff


# In[32]:


#calculate_day("Max Portfolio")


# In[1]:


#import time 
#cleanup()
#stocks, names= initialize_stocks("200d")
##max_stocks, max_names = init("Test-Set2", stocks, names)

#permutations=[]
#for a in range(1,3):
#    for b in range(1,3):
#        for c in range(1,3):
#            for d in range(1,3):
#                for e in range(1,3):
#                    for f in range(1,3):
#                        for g in range(1,3):
#                            for h in range(1,3):
#                                for i in range(1,3):
#                                    #permutations.append([a,b,c,d,e,f,g,h,i])
#                                    permutations.append([i,h,g,f,e,d,b,c,a])
#                                    
##permutations=[[1, 1, 2, 2, 2, 1, 2, 1, 1],[2, 1, 2, 2, 2, 1, 2, 1, 1],[1, 1, 2, 2, 2, 2, 1, 2, 1],[1, 1, 1, 2, 2, 2, 1, 2, 1],[1, 1, 1, 1, 1, 1, 2, 2, 1],[2, 2, 2, 2, 1, 1, 1, 2, 1],[1, 1, 1, 1, 1, 1, 1, 1, 1],[1, 1, 1, 2, 2, 1, 1, 2, 1],[1, 1, 1, 1, 1, 1, 2, 1, 1],[1, 1, 1, 1, 1, 1, 2, 1, 2],[2, 2, 1, 2, 2, 1, 1, 2, 1],[1, 2, 2, 2, 2, 2, 1, 2, 2],[2, 2, 2, 2, 2, 1, 2, 1, 1],[1, 2, 1, 2, 1, 1, 1, 2, 1],[1, 2, 2, 2, 1, 1, 1, 1, 1],[2, 1, 2, 2, 2, 1, 2, 2, 1],[1, 1, 1, 2, 2, 2, 1, 1, 1],[1, 2, 2, 2, 2, 1, 2, 2, 1],[2, 1, 1, 2, 1, 1, 1, 2, 1],[1, 2, 2, 2, 1, 1, 2, 2, 1],[2, 1, 1, 1, 2, 2, 1, 1, 2],[1, 1, 1, 1, 1, 1, 1, 2, 2],[2, 1, 1, 1, 2, 1, 2, 2, 1],[2, 1, 1, 1, 2, 2, 1, 1, 1],[2, 1, 1, 1, 2, 1, 2, 1, 2],[2, 1, 1, 1, 2, 1, 2, 2, 2],[0, 0, 1, 1, 0, 0, 0, 1, 1],[0, 0, 1, 1, 1, 0, 0, 0, 1],[0, 1, 1, 0, 0, 0, 0, 0, 1],[0, 0, 1, 0, 1, 0, 0, 0, 1],[0, 0, 1, 0, 0, 0, 0, 1, 1],[0, 0, 1, 0, 0, 0, 1, 0, 1],[0, 0, 1, 1, 0, 0, 1, 0, 0],[1, 0, 0, 0, 0, 1, 0, 0, 1],[0, 0, 1, 1, 0, 0, 0, 0, 1],[0, 1, 1, 1, 0, 0, 0, 0, 0],[0, 0, 0, 1, 0, 1, 1, 1, 1],[0, 0, 0, 0, 0, 1, 1, 1, 1],[0, 0, 1, 1, 0, 0, 1, 0, 1],[1, 1, 0, 0, 0, 0, 0, 0, 1],[1, 1, 0, 1, 0, 0, 0, 0, 0],[0, 1, 0, 1, 1, 0, 0, 1, 1],[0, 1, 0, 1, 0, 0, 0, 1, 0],[1, 1, 0, 1, 1, 0, 0, 1, 1],[1, 1, 1, 1, 0, 1, 1, 0, 0],[1, 0, 0, 0, 0, 0, 1, 1, 0],[1, 0, 1, 1, 0, 0, 0, 1, 0],[1, 0, 1, 1, 1, 1, 0, 1, 0],[1, 0, 0, 1, 0, 1, 1, 0, 0],[0, 1, 0, 1, 0, 0, 1, 0, 0],[0, 1, 1, 0, 1, 0, 0, 1, 0],[1, 0, 0, 1, 1, 1, 0, 0, 0],[0, 1, 0, 0, 0, 0, 1, 1, 0],[1, 1, 1, 1, 0, 0, 1, 1, 1],[1, 0, 1, 1, 0, 0, 1, 1, 1],[1, 0, 1, 1, 0, 1, 1, 0, 0],[1, 0, 0, 0, 1, 1, 0, 1, 0],[0, 0, 0, 1, 0, 1, 1, 1, 1],[0, 0, 1, 1, 1, 1, 0, 0, 0],[0, 0, 0, 0, 1, 0, 0, 1, 1],[0, 1, 1, 1, 1, 1, 0, 0, 0],[1, 0, 1, 0, 0, 0, 0, 0, 1],[0, 1, 1, 0, 1, 1, 0, 1, 0],[0, 1, 0, 1, 1, 1, 1, 1, 1],[0, 0, 0, 1, 1, 1, 1, 0, 1],[1, 0, 1, 0, 1, 0, 0, 1, 1],[0, 0, 0, 1, 1, 1, 1, 0, 0],[0, 1, 0, 0, 1, 1, 0, 1, 1],[0, 1, 1, 0, 0, 1, 0, 1, 0],[0, 1, 1, 0, 1, 1, 0, 0, 0],[0, 0, 0, 0, 1, 1, 0, 1, 1],[0, 0, 1, 1, 0, 0, 1, 0, 1],[0, 0, 1, 1, 0, 0, 0, 0, 1],[0, 1, 1, 1, 0, 0, 0, 0, 1],[1, 1, 1, 1, 0, 0, 0, 0, 1],[1, 0, 1, 1, 0, 0, 1, 0, 1],[0, 0, 0, 0, 0, 1, 0, 1, 1],[0, 1, 0, 0, 0, 1, 0, 0, 1],[0, 1, 1, 1, 0, 0, 1, 0, 1],[0, 0, 0, 0, 1, 1, 0, 0, 1],[1, 1, 1, 1, 0, 0, 1, 0, 1],[0, 0, 0, 0, 0, 1, 1, 0, 1],[1, 1, 1, 1, 1, 1, 1, 1, 0],[1, 1, 1, 1, 0, 1, 1, 0, 1],[0, 0, 1, 1, 0, 0, 0, 1, 1],[1, 0, 1, 1, 0, 1, 1, 0, 0],[0, 0, 1, 1, 0, 1, 1, 0, 1],[0, 0, 1, 1, 0, 1, 0, 1, 1],[0, 1, 1, 1, 0, 1, 0, 0, 1],[1, 0, 0, 0, 0, 1, 1, 0, 0],[0, 0, 1, 1, 1, 1, 0, 0, 1],[1, 1, 0, 0, 0, 1, 1, 0, 0],[1, 0, 1, 1, 0, 0, 0, 0, 1],[0, 0, 1, 1, 0, 0, 1, 0, 1],[0, 0, 1, 1, 0, 1, 0, 0, 1],[0, 0, 0, 0, 0, 1, 1, 1, 0],[0, 0, 1, 1, 1, 0, 0, 0, 1],[0, 0, 1, 1, 0, 0, 0, 1, 1],[0, 0, 0, 0, 1, 1, 1, 0, 0],[0, 1, 0, 0, 0, 1, 1, 0, 0],[0, 0, 1, 1, 0, 0, 0, 0, 1],[0, 0, 1, 0, 0, 0, 1, 1, 0],[0, 1, 1, 1, 1, 1, 0, 1, 0],[0, 1, 0, 0, 1, 0, 0, 0, 1],[0, 1, 0, 0, 0, 1, 0, 1, 0],[1, 1, 0, 0, 0, 0, 0, 1, 0],[0, 1, 0, 1, 1, 0, 0, 0, 0],[0, 1, 0, 0, 1, 1, 0, 0, 0],[0, 0, 1, 1, 0, 1, 0, 0, 0],[1, 1, 1, 1, 1, 1, 0, 1, 0],[1, 1, 0, 1, 0, 0, 0, 0, 0],[0, 1, 0, 0, 0, 0, 0, 1, 1],[1, 0, 1, 1, 0, 0, 0, 0, 0],[0, 0, 0, 1, 1, 0, 1, 0, 1],[1, 0, 1, 1, 1, 1, 0, 1, 0],[0, 1, 1, 0, 0, 0, 0, 1, 0]]
##permutations = [[2, 1, 1, 1, 2, 1, 2, 2, 2],[2, 1, 1, 1, 2, 1, 2, 1, 2]]
#permutations=[[1, 1, 1, 1, 1, 1, 1, 1, 1],[1, 1, 1, 1, 1, 1, 2, 3, 1]]
#start = time.time()
#list = []
##max_gesamt=0##

#for perm in permutations:
#    if sum(perm) <= 2:
#        print("continue")
#        continue
#    # only use the last 4 indicators (signal indicators)
#    summe = sum(perm[5:])
#    weighted_merge_perm(perm, max_stocks, max_names)
#    gesamt = evaluate_model_weighted_perm(summe,"Test-Set2", max_stocks, max_names)
#    list.append([perm,gesamt])
#    end = time.time()
#    print(end - start)
#    time.sleep(1.5)
#    cleanup()
 #   time.sleep(1.5)
#    if gesamt > max_gesamt:
#        print("Permutation "+str(perm)+" ist besser ------ "+str(gesamt))
#        max_gesamt=gesamt
#        
#                
#test3=list
#len(test3)
#test3=sorted(test3,key=itemgetter(1))
#for x in test3:
#    print(x)
#    
#print("####################################"#)#


# In[ ]:




