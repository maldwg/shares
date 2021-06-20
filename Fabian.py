#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import math
from Database import *

# init the trading values
def evaluate_modell_new(portfolio, stocks, names):
    Startkapital = get_startkapital(portfolio)
    aktien_list = get_stocks_from_portfolio(portfolio)
    aktien_list= get_names(aktien_list)
    length=len(stocks[0]["close"])
    for day in range(length-1):
        print("---------------")
        print("Day " + str(day+1))
        signal_aktien=create_signal_array(aktien_list)
        count_aktie = 0
        for stock in stocks:
            stock=stock[["close","buy_weak","buy_middle","buy_strong","sell_weak","sell_middle","sell_strong","hold"]]
            if not (math.isnan(stock.iloc[day]["sell_weak"])):
                signal_aktien[count_aktie][1] = "sell_weak"
            elif not (math.isnan(stock.iloc[day]["sell_middle"])):
                signal_aktien[count_aktie][1] = "sell_middle"
            elif not (math.isnan(stock.iloc[day]["sell_strong"])):
                signal_aktien[count_aktie][1] = "sell_strong"
            elif not (math.isnan(stock.iloc[day]["buy_weak"])):
                signal_aktien[count_aktie][1] = "buy_weak"
            elif not (math.isnan(stock.iloc[day]["buy_middle"])):
                signal_aktien[count_aktie][1] = "buy_middle"
            elif not (math.isnan(stock.iloc[day]["buy_strong"])):
                signal_aktien[count_aktie][1] = "buy_strong"
            else:
                signal_aktien[count_aktie][1] = "hold"
            count_aktie += 1
        
        aktie_numbers = contains(signal_aktien, "sell_strong")
        for aktie_number in aktie_numbers:
            sell(portfolio, aktien_list[aktie_number], 0.6, stocks[aktie_number].iloc[day]["close"])
            
        aktie_numbers = contains(signal_aktien, "sell_middle")
        for aktie_number in aktie_numbers:
            sell(portfolio, aktien_list[aktie_number], 0.4, stocks[aktie_number].iloc[day]["close"])
        
        aktie_numbers = contains(signal_aktien, "sell_weak")
        for aktie_number in aktie_numbers:
            sell(portfolio, aktien_list[aktie_number], 0.25, stocks[aktie_number].iloc[day]["close"])
            
        aktie_numbers = contains(signal_aktien, "buy_strong")
        for aktie_number in aktie_numbers:
            buy(portfolio, aktien_list[aktie_number], 0.3, stocks[aktie_number].iloc[day]["close"])
        
        aktie_numbers = contains(signal_aktien, "buy_middle")
        for aktie_number in aktie_numbers:
            buy(portfolio, aktien_list[aktie_number], 0.25, stocks[aktie_number].iloc[day]["close"])
            
        aktie_numbers = contains(signal_aktien, "buy_weak")
        for aktie_number in aktie_numbers:
            buy(portfolio, aktien_list[aktie_number], 0.1, stocks[aktie_number].iloc[day]["close"])
    print_summary(portfolio, aktien_list, stocks)
        
def buy (portfolio, Aktie, prozent_kapital, value):
    Kapital=get_kapital(portfolio)
    kaufwert = prozent_kapital*Kapital
    if kaufwert > value:
        anzahl = math.floor(kaufwert/value)
    else:
        anzahl = math.floor(Kapital/value)
        if anzahl == 0:
            return
    buy_stock(portfolio, Aktie, value, anzahl)

def sell(portfolio, Aktie, prozent_aktie, value):
    Kapital=get_kapital(portfolio)
    anzahl=get_anzahl(portfolio,Aktie)
    einstandskurs = get_einstandskurs(portfolio, Aktie)
    if anzahl <= 0 or (einstandskurs != 0 and einstandskurs > value):
        return
    aktien_to_sell = round(prozent_aktie*anzahl)
    if aktien_to_sell < 0:
        aktien_to_sell = 1
    sell_stock(portfolio, Aktie, value, anzahl)
        
def contains(signal_aktien, signal):
    count_list = []
    count = 0
    for signal_aktie in signal_aktien:
        if signal_aktie[1] == signal:
            count_list.extend([count])
        count += 1
    return count_list
    
def create_signal_array(list):
    signal_aktien_list=[]
    for aktie in list:
        signal_aktien_list.append([aktie,""])
    return signal_aktien_list

def print_summary(portfolio, aktien_list, stocks):
    Kapital=float(get_kapital(portfolio))
    geld=0.0
    for counter in range(len(aktien_list)):
        print(aktien_list[counter])
        anzahl=get_anzahl(portfolio,aktien_list[counter])
        value=stocks[counter].iloc[-1]["close"]
        geld += anzahl*value
    print("Aktien Wert: " + str(geld))
    print("Gesamt: " + str(Kapital+geld))

def get_names(list):
    helper_list=[]
    for x in list:
        helper_list.append(x[0])
    return helper_list


# In[2]:


import pandas as pd
import numpy as np
import math
from Database import *

# init the trading values
def evaluate_model_weighted(portfolio, stocks, names):
    Startkapital = get_startkapital(portfolio)
    aktien_list = get_stocks_from_portfolio(portfolio)
    aktien_list= get_names(aktien_list)
    length=len(stocks[0]["close"])
    for day in range(length):
        print("---------------")
        print("Day " + str(day+1))
        signal_aktien=create_signal_array(aktien_list)
        count_aktie = 0
        for stock in stocks:
            stock=stock[["close","buy_weak","buy_middle","buy_strong","sell_weak","sell_middle","sell_strong","hold","weighted_signal"]]
            if day > len(stock["close"]):
                print("continue")
                continue
            signal_aktien[count_aktie][1] = stock.iloc[day]["weighted_signal"]
            count_aktie += 1      
        # 10 is not included    
        for weight in reversed(range(-9, 10)):
            aktie_numbers = contains(signal_aktien, weight)
            if weight > 1:
                for aktie_number in aktie_numbers:
                    buy(portfolio, aktien_list[aktie_number], weight/9, stocks[aktie_number].iloc[day]["close"])   
            elif weight < -1:
                for aktie_number in aktie_numbers:
                    sell(portfolio, aktien_list[aktie_number], weight/9, stocks[aktie_number].iloc[day]["close"])
    print_summary(portfolio, aktien_list, stocks)
        
def buy (portfolio, Aktie, prozent_kapital, value):
    Kapital=get_kapital(portfolio)
    kaufwert = prozent_kapital*Kapital
    if kaufwert > value:
        anzahl = math.floor(kaufwert/value)
    else:
        anzahl = math.floor(Kapital/value)
        if anzahl == 0:
            return
    buy_stock(portfolio, Aktie, value, anzahl)

def sell(portfolio, Aktie, prozent_aktie, value):
    Kapital=get_kapital(portfolio)
    anzahl=get_anzahl(portfolio,Aktie)
    einstandskurs = get_einstandskurs(portfolio, Aktie)
    if anzahl <= 0 or (einstandskurs != 0 and einstandskurs > value):
        return
    aktien_to_sell = round(prozent_aktie*anzahl)
    if aktien_to_sell < 0:
        aktien_to_sell = 1
    sell_stock(portfolio, Aktie, value, anzahl)
        
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

def print_summary(portfolio, aktien_list, stocks):
    Kapital=float(get_kapital(portfolio))
    geld=0.0
    for counter in range(len(aktien_list)):
        print(aktien_list[counter])
        anzahl=get_anzahl(portfolio,aktien_list[counter])
        value=stocks[counter].iloc[-1]["close"]
        geld += anzahl*value
    print("Aktien Wert: " + str(geld))
    print("Gesamt: " + str(Kapital+geld))

def get_names(list):
    helper_list=[]
    for x in list:
        helper_list.append(x[0])
    return helper_list


# In[3]:


def analyze_day(portfolio, stocks, names):
    Startkapital = get_startkapital(portfolio)
    aktien_list = get_stocks_from_portfolio(portfolio)
    aktien_list= get_names(aktien_list)
    signal_aktien=create_signal_array(aktien_list)
    # signal aktien is an array that holds share name and signal
    print(aktien_list)
    count_aktie = 0
    for stock in stocks:
            stock=stock[["close","buy_weak","buy_middle","buy_strong","sell_weak","sell_middle","sell_strong","hold"]]
            if not (math.isnan(stock.iloc[-1]["sell_weak"])):
                signal_aktien[count_aktie][1] = "sell_weak"
            elif not (math.isnan(stock.iloc[-1]["sell_middle"])):
                signal_aktien[count_aktie][1] = "sell_middle"
            elif not (math.isnan(stock.iloc[-1]["sell_strong"])):
                signal_aktien[count_aktie][1] = "sell_strong"
            elif not (math.isnan(stock.iloc[-1]["buy_weak"])):
                signal_aktien[count_aktie][1] = "buy_weak"
            elif not (math.isnan(stock.iloc[-1]["buy_middle"])):
                signal_aktien[count_aktie][1] = "buy_middle"
            elif not (math.isnan(stock.iloc[-1]["buy_strong"])):
                signal_aktien[count_aktie][1] = "buy_strong"
            else:
                signal_aktien[count_aktie][1] = "hold"
            count_aktie += 1        
        
    aktie_numbers = contains(signal_aktien, "sell_strong")
    for aktie_number in aktie_numbers:
        sell(portfolio, aktien_list[aktie_number], 0.6, stocks[aktie_number].iloc[-1]["close"])
            
    aktie_numbers = contains(signal_aktien, "sell_middle")
    for aktie_number in aktie_numbers:
        sell(portfolio, aktien_list[aktie_number], 0.4, stocks[aktie_number].iloc[-1]["close"])
        
    aktie_numbers = contains(signal_aktien, "sell_weak")
    for aktie_number in aktie_numbers:
        sell(portfolio, aktien_list[aktie_number], 0.25, stocks[aktie_number].iloc[-1]["close"])
            
    aktie_numbers = contains(signal_aktien, "buy_strong")
    for aktie_number in aktie_numbers:
        buy(portfolio, aktien_list[aktie_number], 0.3, stocks[aktie_number].iloc[-1]["close"])
        
    aktie_numbers = contains(signal_aktien, "buy_middle")
    for aktie_number in aktie_numbers:
        buy(portfolio, aktien_list[aktie_number], 0.25, stocks[aktie_number].iloc[-1]["close"])
            
    aktie_numbers = contains(signal_aktien, "buy_weak")
    for aktie_number in aktie_numbers:
        buy(portfolio, aktien_list[aktie_number], 0.1, stocks[aktie_number].iloc[-1]["close"])
        
def buy (portfolio, Aktie, prozent_kapital, value):
    Kapital=get_kapital(portfolio)
    kaufwert = prozent_kapital*Kapital
    if kaufwert > value:
        anzahl = math.floor(kaufwert/value)
    else:
        anzahl = math.floor(Kapital/value)
        if anzahl == 0:
            return
    decision = input("Wollen Sie "+str(anzahl)+" Aktien von "+str(Aktie)+" fuer "+str(value)+" kaufen? [Ja/Nein]")
    if decision == "Ja":
        buy_stock(portfolio, Aktie, value, anzahl)
    else: 
        decision = input("Wie viele Aktien wollen Sie kaufen? [0-"+str(math.floor(Kapital/value))+"]")
        if int(decision) == 0:
            print("keine Aktien ausgewählt")
            return
        elif int(decision) > math.floor(Kapital/value):
            print("Zu viele Aktien ausgewählt")
            return
        else:
            anzahl = int(decision)
            decision = input("Wollen Sie "+str(anzahl)+" Aktien von "+str(Aktie)+" fuer "+str(value)+" kaufen? [Ja/Nein]")
            if decision == "Ja":
                buy_stock(portfolio, Aktie, value, anzahl)
            else:
                return

        buy_stock(portfolio, Aktie, value, anzahl)
def sell(portfolio, Aktie, prozent_aktie, value):
    Kapital=get_kapital(portfolio)
    anzahl=get_anzahl(portfolio,Aktie)
    einstandskurs = get_einstandskurs(portfolio, Aktie)
    if anzahl <= 0 or (einstandskurs != 0 and einstandskurs > value):
        return
    aktien_to_sell = round(prozent_aktie*anzahl)
    if aktien_to_sell < 0:
        aktien_to_sell = 1
    decision = input("Wollen Sie "+str(anzahl)+" Aktien von "+str(Aktie)+" fuer "+str(value)+" verkaufen? [Ja/Nein]")
    if decision == "Ja":
        sell_stock(portfolio, Aktie, value, anzahl)
    else: 
        decision = input("Wie viele Aktien wollen Sie verkaufen? [0-"+str(anzahl)+"]")
        if int(decision) == 0:
            print("keine Aktien ausgewählt")
            return
        elif int(decision) > anzahl:
            print("Zu viele Aktien ausgewählt")
            return
        else:
            anzahl = int(decision)
            decision = input("Wollen Sie "+str(anzahl)+" Aktien von "+str(Aktie)+" fuer "+str(value)+" verkaufen? [Ja/Nein]")
            if decision == "Ja":
                sell_stock(portfolio, Aktie, value, anzahl)
            else:
                return
        
def contains(signal_aktien, signal):
    count_list = []
    count = 0
    for signal_aktie in signal_aktien:
        if signal_aktie[1] == signal:
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


# In[ ]:


import pandas as pd
import numpy as np
import math
import time
from Database import *


# init the trading values
def evaluate_model_weighted_perm(summe, portfolio, stocks, names):
    Startkapital = get_startkapital(portfolio)
    aktien_list = get_stocks_from_portfolio(portfolio)
    aktien_list= get_names(aktien_list)
    length=len(stocks[0]["close"])
    for day in range(length):
        #print("---------------")
        #print("Day " + str(day+1))
        signal_aktien=create_signal_array(aktien_list)
        count_aktie = 0
        for stock in stocks:
            stock=stock[["close","buy_weak","buy_middle","buy_strong","sell_weak","sell_middle","sell_strong","hold","weighted_signal"]]
            if day >= len(stock["close"]):
                count_aktie += 1      
                continue
            signal_aktien[count_aktie][1] = stock.iloc[day]["weighted_signal"]
            count_aktie += 1      
        # 10 is not included    
        for weight in reversed(range(-summe, summe+1)):
            aktie_numbers = contains(signal_aktien, weight)
            if weight > 1:
                for aktie_number in aktie_numbers:
                    buy(portfolio, aktien_list[aktie_number], weight/((1/3)*summe+summe), stocks[aktie_number].iloc[day]["close"])   
            elif weight < -1:
                for aktie_number in aktie_numbers:
                    sell(portfolio, aktien_list[aktie_number], weight/summe, stocks[aktie_number].iloc[day]["close"])
            
    gesamt= print_summary(portfolio, aktien_list, stocks)
    return(gesamt)
        
def buy (portfolio, Aktie, prozent_kapital, value):
    Kapital=get_kapital(portfolio)
    kaufwert = prozent_kapital*Kapital
    if kaufwert > value:
        anzahl = math.floor(kaufwert/value)
    else:
        anzahl = math.floor(Kapital/value)
        if anzahl == 0:
            return
    buy_stock(portfolio, Aktie, value, anzahl)
    time.sleep(0.1)

def sell(portfolio, Aktie, prozent_aktie, value):
    Kapital=get_kapital(portfolio)
    anzahl=get_anzahl(portfolio,Aktie)
    einstandskurs = get_einstandskurs(portfolio, Aktie)
    if anzahl <= 0 or (einstandskurs != 0 and einstandskurs > value):
        return
    aktien_to_sell = round(prozent_aktie*anzahl)
    if aktien_to_sell < 0:
        aktien_to_sell = 1
    sell_stock(portfolio, Aktie, value, aktien_to_sell)
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

