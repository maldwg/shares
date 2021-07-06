#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import numpy as np
import math
import time
from Database import *
import matplotlib.pyplot as plt


# init the trading values
def evaluate_model_weighted_perm(summe, portfolio, stocks, names):
    Startkapital = get_startkapital(portfolio)
    aktien_list = get_stocks_from_portfolio(portfolio)
    aktien_list= get_names(aktien_list)
    performance=[]
    days=[]
    gesamt_performance=[]
    for aktie in aktien_list:
        performance.append([aktie,0])
    length=len(stocks[0]["close"])
    for day in range(length):
        if day % 25 == 0 and day != 0:
            increase_kapital(portfolio, 0)
        print("---------------")
        print("Day " + str(day+1))
        # get the portfolio value per day
        gesamt_wert = print_summary_day(portfolio,aktien_list,stocks,day)
        print("Portfolio Wert and Tag "+str(day)+": "+str(gesamt_wert))
        signal_aktien=create_signal_array(aktien_list)
        count_aktie = 0
        for stock in stocks:
            stock=stock[["close","buy_weak","buy_middle","buy_strong","sell_weak","sell_middle","sell_strong","hold","weighted_signal"]]
            # skip share if no data available
            if day >= len(stock["close"]):
                count_aktie += 1      
                continue
            signal_aktien[count_aktie][1] = stock.iloc[day]["weighted_signal"]
            count_aktie += 1      
        for weight in range(-summe, 0):
            aktie_numbers = contains(signal_aktien, weight)
            if weight < -0.4*summe:
                for aktie_number in aktie_numbers:
                    # since to small sells were made, the count of the indicators is used instead of the sum
                    # -9 because otherwise the value is negative
                    sell(aktie_number, performance, portfolio, aktien_list[aktie_number], 1.35*weight/-summe, stocks[aktie_number].iloc[day]["close"])            
        for weight in range(0, summe+1): 
            aktie_numbers = contains(signal_aktien, weight)
            if weight > 0.4*summe:
                for aktie_number in aktie_numbers:
                    buy(portfolio, aktien_list[aktie_number], (weight*weight)/(summe*summe)*0.2, stocks[aktie_number].iloc[day]["close"],gesamt_wert)   
        increment_trade_values(portfolio)
        gesamt_performance.append(gesamt_wert)
        print("Kapital: "+str(get_kapital(portfolio)))
    gesamt= print_summary(portfolio, aktien_list, stocks)
    summary(stocks, portfolio, performance)
    print("Now the graph")
    for x in range(len(stocks[0]["close"])):
        days.append(x)
    plt.plot(days, gesamt_performance)
    plt.title("Performance of Portfolio")
    plt.xlabel('Time')  
    plt.ylabel('Value')
    return gesamt
        
def buy (portfolio, Aktie, prozent_kapital, value, gesamt_wert):
    # skip trade if bought within last 3 days
    days = get_last_buy(portfolio, Aktie)
    if days <= 5:
        return
    Kapital=get_kapital(portfolio)
    momentane_anzahl=get_anzahl(portfolio,Aktie)
    momentaner_wert=value*momentane_anzahl
    kaufwert = prozent_kapital*gesamt_wert
    if kaufwert > Kapital:
        kaufwert = Kapital
    # only buy stocks that are worth 50 € in total, othwerwise penny trades
    if kaufwert > 50 and kaufwert > value:
        anzahl = math.floor(kaufwert/value)
    else: 
        return
    if momentaner_wert+anzahl*value > 0.2*gesamt_wert:
        # dann anpassen der anzahl, sodass maximal x % des portfolios daraus bestehen
        # ansonsten bei kursschwankungen auf einmal zu viele Aktien für Kapitalwert --> - Käufe
        if momentane_anzahl < math.floor(gesamt_wert*0.2/value):
            anzahl = math.floor(gesamt_wert*0.2/value)-momentane_anzahl
        else:
            return
    buy_stock(portfolio, Aktie, value, anzahl)
    print("Es wurden "+str(anzahl)+" Aktien von "+str(Aktie)+" gekauft für "+str(anzahl*value)+" entspricht "+str(prozent_kapital)+"%")
    time.sleep(0.1)

def sell(number, performance, portfolio, Aktie, prozent_aktie, value):
    # skip trade if sold within last 3 days
    days = get_last_sell(portfolio, Aktie)
    if days <= 5:
        return
    if prozent_aktie > 1:
        prozent_aktie = 1
    Kapital=get_kapital(portfolio)
    anzahl=get_anzahl(portfolio,Aktie)
    einstandskurs = get_einstandskurs(portfolio, Aktie)
    
    if anzahl <= 0:
        return
    # Totalverkauf bei 20 % verlust
    #elif value < 0.5*einstandskurs:
    #    aktien_to_sell = 0.5*anzahl
    # sell all, if pennystock, since no sense to keep only few stocks
    elif value < 10 and (anzahl-round(prozent_aktie*anzahl) <= 5):
        aktien_to_sell = anzahl        
    else:
        aktien_to_sell = round(prozent_aktie*anzahl)
    # only sell 1 share if 1 share is held, otherwise to many minor trades take place
    if aktien_to_sell < 1 and anzahl == 1:
        aktien_to_sell = 1
    gewinn=aktien_to_sell*(value-einstandskurs)
    # need to make more money than 5 euro with a trade -- otherwise to many small trades
    if (value > 1.10*einstandskurs and gewinn > 7.5) or (value < 0.9*einstandskurs):
        sell_stock(portfolio, Aktie, value, aktien_to_sell)
        print("Es sind insgesamt "+str(anzahl)+" Aktien von "+str(Aktie)+" vorhanden, neuer Stand = "+str(anzahl-aktien_to_sell)+" , "+str(prozent_aktie)+"%")
        print("Es wurden "+str(aktien_to_sell)+" Aktien von "+str(Aktie)+" verkauft, Gewinn: "+str(gewinn))
        performance[number][1] += gewinn
    #else:
        #print("Gewinn zu gering")
    time.sleep(0.1)
        
def contains(signal_aktien, weight):
    count_list = []
    count = 0
    for signal_aktie in signal_aktien:
        if signal_aktie[1] == weight:
            count_list.extend([count])
        count += 1
    return count_list
    
def create_signal_array(list):
    signal_aktien_list=[]
    for aktie in list:
        signal_aktien_list.append([aktie,""])
    return signal_aktien_list

def print_summary_day(portfolio,aktien_list,stocks,day):
    Kapital=float(get_kapital(portfolio))
    geld=0.0
    for counter in range(len(aktien_list)):
        #print(aktien_list[counter])
        if day > len(stocks[counter]["close"]):
            continue
        anzahl=get_anzahl(portfolio,aktien_list[counter])
        value=stocks[counter].iloc[day]["close"]
        geld += anzahl*value
    #print("Aktien Wert: " + str(geld))
    #print("Gesamt: " + str(Kapital+geld))
    helper =Kapital+geld
    return helper    


def print_summary(portfolio, aktien_list, stocks):
    Kapital=float(get_kapital(portfolio))
    geld=0.0
    for counter in range(len(aktien_list)):
        #print(aktien_list[counter])
        anzahl=get_anzahl(portfolio,aktien_list[counter])
        value=stocks[counter].iloc[-1]["close"]
        geld += anzahl*value
    #print("Aktien Wert: " + str(geld))
    #print("Gesamt: " + str(Kapital+geld))
    helper =Kapital+geld
    return helper

def get_names(list):
    helper_list=[]
    for x in list:
        helper_list.append(x[0])
    return helper_list

def summary(stocks, portfolio, performance):
    counter = 0
    for aktie in performance:
        anzahl=get_anzahl(portfolio,aktie[0])
        einstandskurs = get_einstandskurs(portfolio, aktie[0])
        print("Performance gesamt von "+str(aktie[0])+" = "+str(anzahl*(stocks[counter].iloc[-1]["close"]-einstandskurs)+aktie[1])+" gewinn aus Trades = "+str(aktie[1])+" anzahl * marge = "+str(anzahl)+" "+str(stocks[counter].iloc[-1]["close"]-einstandskurs))
        counter+=1


# In[1]:


import pandas as pd
import numpy as np
import math
import time
from Database import *
import matplotlib.pyplot as plt


# init the trading values
def evaluate_day(summe, portfolio, stocks, names):
    Startkapital = get_startkapital(portfolio)
    aktien_list = get_stocks_from_portfolio(portfolio)
    aktien_list= get_names(aktien_list)
    suggestions_buy=[]
    suggestions_sell=[]
    # only look at the last day
    day = -1
    # get the portfolio value per day
    gesamt_wert = print_summary_day(portfolio,aktien_list,stocks,day)
    signal_aktien=create_signal_array(aktien_list)
    count_aktie = 0
    for stock in stocks:
        signal_aktien[count_aktie][1] = stock.iloc[day]["weighted_signal"]
        count_aktie += 1      
    for weight in range(-summe, 0):
        aktie_numbers = contains(signal_aktien, weight)
        if weight < -0.4*summe:
            for aktie_number in aktie_numbers:
                # since to small sells were made, the count of the indicators is used instead of the sum
                # -9 because otherwise the value is negative
                stock_suggestion=sell(aktie_number, portfolio, aktien_list[aktie_number], 1.35*weight/-summe, stocks[aktie_number].iloc[day]["close"], weight)            
                if stock_suggestion != None:
                    suggestions_sell.append(stock_suggestion)
    for weight in range(0, summe+1): 
        aktie_numbers = contains(signal_aktien, weight)
        if weight > 0.4*summe:
            for aktie_number in aktie_numbers:
                stock_suggestion=buy(portfolio, aktien_list[aktie_number], (weight*weight)/(summe*summe)*0.2, stocks[aktie_number].iloc[day]["close"],gesamt_wert, weight)   
                if stock_suggestion != None:
                    suggestions_buy.append(stock_suggestion)
    increment_trade_values(portfolio)
    return suggestions_buy, suggestions_sell, gesamt_wert, Startkapital
        
def buy (portfolio, Aktie, prozent_kapital, value, gesamt_wert, weight):
    # skip trade if bought within last 3 days
    days = get_last_buy(portfolio, Aktie)
    if days <= 5:
        return
    Kapital=get_kapital(portfolio)
    momentane_anzahl=get_anzahl(portfolio,Aktie)
    momentaner_wert=value*momentane_anzahl
    kaufwert = prozent_kapital*gesamt_wert
    if kaufwert > Kapital:
        kaufwert = Kapital
    # only buy stocks that are worth 50 € in total, othwerwise penny trades
    if kaufwert > 50 and kaufwert > value:
        anzahl = math.floor(kaufwert/value)
    else: 
        return
    # maximal 5 % des Portfoliowerts pro trade
    if anzahl*value > 0.05*gesamt_wert:
        anzahl = math.floor((gesamt_wert*0.05)/value)
    if momentaner_wert+anzahl*value > 0.15*gesamt_wert:
        # dann anpassen der anzahl, sodass maximal x % des portfolios daraus bestehen
        # ansonsten bei kursschwankungen auf einmal zu viele Aktien für Kapitalwert --> - Käufe
        if momentane_anzahl < math.floor(gesamt_wert*0.15/value):
            anzahl = math.floor(gesamt_wert*0.15/value)-momentane_anzahl
        else:
            return
    #buy_stock(portfolio, Aktie, value, anzahl)
    return [Aktie, anzahl, value, weight]

def sell(number, portfolio, Aktie, prozent_aktie, value, weight):
    # skip trade if sold within last 3 days
    days = get_last_sell(portfolio, Aktie)
    if days <= 5:
        return
    if prozent_aktie > 1:
        prozent_aktie = 1
    Kapital=get_kapital(portfolio)
    anzahl=get_anzahl(portfolio,Aktie)
    einstandskurs = get_einstandskurs(portfolio, Aktie)
    
    if anzahl <= 0:
        return
    # sell all, if pennystock, since no sense to keep only few stocks
    elif value < 10 and (anzahl-round(prozent_aktie*anzahl) <= 5):
        aktien_to_sell = anzahl        
    else:
        aktien_to_sell = round(prozent_aktie*anzahl)
    # only sell 1 share if 1 share is held, otherwise to many minor trades take place
    if aktien_to_sell < 1 and anzahl == 1:
        aktien_to_sell = 1
    gewinn=aktien_to_sell*(value-einstandskurs)
    # need to make more money than 5 euro with a trade -- otherwise to many small trades
    if (value > 1.10*einstandskurs and gewinn > 7.5) or (value < 0.9*einstandskurs) or(days > 90):
        #sell_stock(portfolio, Aktie, value, aktien_to_sell)
        return [Aktie, anzahl, value, weight]
    else:
        return
        
def contains(signal_aktien, weight):
    count_list = []
    count = 0
    for signal_aktie in signal_aktien:
        if signal_aktie[1] == weight:
            count_list.extend([count])
        count += 1
    return count_list
    
def create_signal_array(list):
    signal_aktien_list=[]
    for aktie in list:
        signal_aktien_list.append([aktie,""])
    return signal_aktien_list

def get_names(list):
    helper_list=[]
    for x in list:
        helper_list.append(x[0])
    return helper_list

def print_summary_day(portfolio,aktien_list,stocks,day):
    Kapital=float(get_kapital(portfolio))
    geld=0.0
    for counter in range(len(aktien_list)):
        #print(aktien_list[counter])
        if day > len(stocks[counter]["close"]):
            continue
        anzahl=get_anzahl(portfolio,aktien_list[counter])
        value=stocks[counter].iloc[day]["close"]
        geld += anzahl*value
    #print("Aktien Wert: " + str(geld))
    #print("Gesamt: " + str(Kapital+geld))
    helper =Kapital+geld
    return helper    


# In[ ]:





# In[ ]:




