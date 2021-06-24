#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from technical_indicators_lib import *
import yfinance as yf
import math
import matplotlib.pyplot as plt
from williamsR import *
from Database import *
from analyzing_algorithms import *
from email_service import *
from Shares import *
from operator import itemgetter


# In[2]:


# receive mails and trade
# value like [mludwig3@...,{buy:[[]], sell[[]]}]
portfolio_trades=receive_emails()
print(portfolio_trades) 
if portfolio_trades:
    for trades in portfolio_trades:
        print(trades[0])
        portfolio=get_portfolio_by_mail(trades[0])
        for buy in trades[1]["buy"]:
            stock=buy[0]
            price=buy[1]
            ammount=buy[2]
            print(type(price))
            print(type(stock))
            print(type(ammount))
            buy_stock(portfolio, stock, price, ammount)
        for sell in trades[1]["sell"]:
            stock=sell[0]
            price=sell[1]
            ammount=sell[2]
            sell_stock(portfolio, stock, price, ammount)

# get all portfolios
all_portfolio_names = get_all_portfolios()
# analyze all shares
all_stocks, all_names = initialize_stocks("alles", "50d")
# first five numbers for trend inciators, last numbers for action indicators
permutation = [1, 1, 1, 1, 2, 1, 3, 2, 1]
summe = sum(permutation[5:])
combine_indicators(permutation, all_stocks, all_names)

# analyze every other portfolio
for portfolio in all_portfolio_names:
    print(portfolio)
    if portfolio == "alles" or  portfolio == "Test-Set" or  portfolio == "Test-Set2":
        continue
    else:
        # get wanted stocks 
        portfolio_stocks, portfolio_names = get_portfolio_data(portfolio, all_stocks, all_names)
        # get suggestions
        buy_suggestions, sell_suggestions, portfolio_value, Startkapital = evaluate_day(summe,portfolio, portfolio_stocks, portfolio_names)
        print(buy_suggestions)
        print(sell_suggestions)
        print(portfolio_value)
        print(Startkapital)
    
        # get email from portfolio
        mail=get_email(portfolio)
        kapital = get_kapital(portfolio)
        # get stocks_anzahl
        name_anzahl_preis = []
        for name in portfolio_names:
            anzahl, preis = get_ammount_and_price_by_name(portfolio, name)
            name_anzahl_preis.append((name, anzahl, preis))
        # call email service
        print("----------------------------------------------")
        print(mail)
        print(kapital)
        print(name_anzahl_preis)
        print(sell_suggestions)
        print(buy_suggestions)
        print(Startkapital)
        print(portfolio_value)
        send_email_sell(mail, kapital, name_anzahl_preis, sell_suggestions, Startkapital, portfolio_value)
        send_email_buy(mail, kapital, name_anzahl_preis, buy_suggestions, Startkapital, portfolio_value)
    
    

