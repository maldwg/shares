#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3


# In[1]:


############################################
#helper methods
def init_db_connection():
    # init db connection
    conn = sqlite3.connect("./shares.db")
    sql = conn.cursor()   
    return conn, sql

def close_db_connection(conn, sql):
    # close connection
    sql.close()
    conn.close()

def get_stocks_from_portfolio(portfolio):
    conn, sql = init_db_connection()
    portfolio_id=get_portfolio_id(portfolio)
    sql.execute("select shares.name, shares.identifier from portfolio_shares left join portfolio on portfolio_shares.portfolio = portfolio.id left join shares on portfolio_shares.share=shares.id where portfolio_shares.portfolio="+str(portfolio_id)+";")
    results=sql.fetchall()
    close_db_connection(conn, sql)
    return results    

    
    
def get_ammount_and_price(portfolio_id,stock_id):
    conn,sql = init_db_connection()
    sql.execute("Select anteile, einstandskurs from portfolio_shares where portfolio="+str(portfolio_id)+" and share ="+str(stock_id))
    ammount,price=sql.fetchone()
    close_db_connection(conn,sql)
    return ammount,price


def get_portfolio_share_id(portfolio, stock):
    conn,sql = init_db_connection()
    sql.execute("Select id from portfolio where name='"+portfolio+"'")    
    portfolio_id=sql.fetchone()[0]
    sql.execute("Select id from shares where name='"+stock+"'")    
    stock_id=sql.fetchone()[0]
    sql.execute("Select portfolio_shares.id from portfolio_shares where portfolio="+str(portfolio_id)+" and share ="+str(stock_id))    
    stock_portfolio_id=sql.fetchone()[0]
    close_db_connection(conn,sql)
    return stock_portfolio_id

def get_stock_id(stock):
    conn,sql = init_db_connection()
    sql.execute("Select id from shares where name='"+stock+"'")    
    stock_id=sql.fetchone()[0]
    close_db_connection(conn,sql)
    return stock_id   

def get_portfolio_id(portfolio):
    conn,sql = init_db_connection()
    sql.execute("Select id from portfolio where name='"+portfolio+"'")    
    portfolio_id=sql.fetchone()[0]
    close_db_connection(conn,sql)
    return portfolio_id

###############################################

# relevant methods to call

def buy_stock(portfolio, stock, price, ammount): # portfolio and stock = names, price = closing value, ammount = ammount
    conn,sql = init_db_connection()
    portfolio_id = get_portfolio_id(portfolio)
    stock_id = get_stock_id(stock)
    portfolio_stock_id=get_portfolio_share_id(portfolio,stock)
    old_stocks, old_price=get_ammount_and_price(portfolio_id,stock_id)
    new_stocks=old_stocks+ammount
    new_price=(old_price*old_stocks+price*ammount)/new_stocks # neuer einstandskurs anteilig errechnet
    sql.execute("update portfolio_shares set anteile="+str(new_stocks)+", einstandskurs="+str(new_price)+" where id ="+str(portfolio_stock_id))   
    conn.commit()
    kapital=get_kapital(portfolio)
    new_kapital=kapital-price*ammount
    sql.execute("update portfolio set aktuelles_kapital="+str(new_kapital)+" where id ="+str(portfolio_id))
    conn.commit()
    #print("Es wurden "+str(ammount)+" " + stock + " Aktien für "+str(price)+" € gekauft")
    close_db_connection(conn, sql)
    # ernidrige kapital!
    
def sell_stock(portfolio, stock, price, ammount): # portfolio and stock = names, price = closing value, ammount = ammount
    conn,sql = init_db_connection()
    portfolio_id = get_portfolio_id(portfolio)
    stock_id = get_stock_id(stock)
    portfolio_stock_id=get_portfolio_share_id(portfolio,stock)
    old_stocks, old_price=get_ammount_and_price(portfolio_id,stock_id)
    new_stocks=old_stocks-ammount
    sql.execute("update portfolio_shares set anteile="+str(new_stocks)+" where id ="+str(portfolio_stock_id))   
    conn.commit()
    gewinn = (price-old_price)*ammount
    #print("Es wurden "+str(ammount)+" " + stock + " Aktien verkauft")
    #print("Gewinn: "+str(gewinn)+" €")
    kapital=get_kapital(portfolio)
    sql.execute("update portfolio set aktuelles_kapital="+str(kapital+price*ammount)+" where id ="+str(portfolio_id))
    conn.commit()
    if new_stocks==0:
        sql.execute("update portfolio_shares set einstandskurs=0 where id ="+str(portfolio_stock_id))   
        conn.commit()
    # kapital erhöhen 
    close_db_connection(conn, sql)

def get_kapital(portfolio): # portfolio = name
    conn,sql = init_db_connection()
    portfolio_id = get_portfolio_id(portfolio)
    sql.execute("Select aktuelles_kapital from portfolio where id="+str(portfolio_id))
    kapital=sql.fetchone()[0]
    close_db_connection(conn,sql)
    return kapital     

def get_startkapital(portfolio): # portfolio = name
    conn,sql = init_db_connection()
    portfolio_id = get_portfolio_id(portfolio)
    sql.execute("Select startkapital from portfolio where id="+str(portfolio_id))
    kapital=sql.fetchone()[0]
    close_db_connection(conn,sql)
    return kapital 

def get_anzahl(portfolio,stock): # portfolio and stock = names,
    conn,sql = init_db_connection()
    portfolio_stock_id=get_portfolio_share_id(portfolio,stock)
    sql.execute("select anteile from portfolio_shares where id ="+str(portfolio_stock_id))
    kapital=sql.fetchone()[0]
    close_db_connection(conn,sql)
    return kapital    

def get_einstandskurs(portfolio,stock): # portfolio and stock = names,
    conn,sql = init_db_connection()
    portfolio_stock_id=get_portfolio_share_id(portfolio,stock)
    sql.execute("select einstandskurs from portfolio_shares where id ="+str(portfolio_stock_id))
    kapital=sql.fetchone()[0]
    close_db_connection(conn,sql)
    return kapital  

def create_portfolio(name, aktuelles_kapital, startkapital):
    conn,sql = init_db_connection()
    sql.execute("insert into portfolio (name, aktuelles_kapital, startkapital) values ('"+name+"',"+str(aktuelles_kapital)+","+str(startkapital)+");")
    conn.commit()
    close_db_connection(conn,sql)
    return True      

def delete_portfolio(portfolio):
    conn,sql = init_db_connection()
    portfolio_id = get_portfolio_id(portfolio)
    sql.execute("delete from table portfolio where id="+str(portfolio_id))
    conn.commit()
    close_db_connection(conn,sql)
    return True     

def add_stock_to_portfolio(portfolio, stock, anzahl, einstandskurs):
    conn,sql = init_db_connection()
    portfolio_id = get_portfolio_id(portfolio)
    stock_id = get_stock_id(stock)
    sql.execute("insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values ("+str(portfolio_id)+","+str(stock_id)+","+str(anzahl)+","+str(einstandskurs)+");")
    conn.commit()
    close_db_connection(conn,sql)
    return True    

def remove_stock_from_portfolio(portfolio, share):   
    conn,sql = init_db_connection()
    portfolio_id = get_portfolio_id(portfolio)
    stock_id = get_stock_id(stock)
    sql.execute("delete from table portfolio_shares where portfolio="+str(portfolio_id)+" and share="+str(stock_id))
    conn.commit()
    close_db_connection(conn,sql)
    return True 

def increase_kapital(portfolio, increase):
    conn,sql = init_db_connection()
    portfolio_id = get_portfolio_id(portfolio)
    new_kapital= get_kapital(portfolio)+increase
    new_startkapital= get_startkapital(portfolio)+increase
    sql.execute("update portfolio set kapital="+str(new_kapital)+",startkapital="+str(new_startkapital)+" where id ="+str(portfolio_id))
    conn.commit()
    close_db_connection(conn,sql)
    return True     
            
def get_user_id(firstname, lastname):
    conn,sql = init_db_connection()
    sql.execute("select id from user where firstname ="+firstname+" and lastname="+lastname)
    id=sql.fetchone()[0]
    close_db_connection(conn,sql)
    return id        
                
def add_user(firstname, lastname, mail):
    conn,sql = init_db_connection()
    sql.execute("insert into user (firstname, lastname, mail) values ("+firstname+","+lastname+","+mail+");")
    conn.commit()
    close_db_connection(conn,sql)
    return True     
                
def remove_user(firstname, lastname):
    conn,sql = init_db_connection()
    user_id = get_user_id(firstname, lastname)
    sql.execute("delete from table user where id="+str(user_id))
    conn.commit()
    close_db_connection(conn,sql)
    return True  
                
def add_share(name, identifier):
    conn,sql = init_db_connection()
    sql.execute("insert into shares (name, identifier) values ("+name+","+identifier+");")
    conn.commit()
    close_db_connection(conn,sql)
    return True       
                
def remove_share(share):
    conn,sql = init_db_connection()
    stock_id = get_stock_id(stock)
    sql.execute("delete from table shares where id="+str(stock_id))
    conn.commit()
    close_db_connection(conn,sql)
    return True 

def cleanup():
    conn,sql = init_db_connection()
    sql.execute("update portfolio_shares set einstandskurs=0.0, anteile=0 where portfolio=1")
    sql.execute("update portfolio set startkapital=2500.0, aktuelles_kapital=2500.0 where id=1")
    conn.commit()
    close_db_connection(conn,sql)
    return True


# In[ ]:




