#!/usr/bin/env python
# coding: utf-8

# In[88]:


import smtplib, ssl, email, mimetypes
from datetime import date
from email.message import EmailMessage
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import decode_header
import csv
import imaplib
import os
import re


# In[35]:


sender_email = "fama.shares@gmail.com"
#receiver_email = "maxludwig23@t-online.de"
port = 465
password = "www.pornhub.com"


# In[36]:


#Kapital = 10300.54
#receiver_email = "brandmueller.fabian@gmail.com"
#receiver_email = "maxludwig3@t-online.de"
#aktien_preis_anzahl_empfehlung_list = [["aktie1", 8.1, 3], ["aktie2", 7.8, 5], ["aktie3", 5.9, 13]]
#aktien_anzahl_list = [["aktie1", 3], ["aktie2", 1], ["aktie3", 5]]


#send_email_sell(receiver_email, Kapital, aktien_anzahl_list, aktien_preis_anzahl_empfehlung_list)


# In[54]:


def send_email_sell(receiver_email, Kapital, aktien_anzahl_list, aktien_preis_anzahl_empfehlung_list, Startkapital, portfolio_wert):
    message = build_email_sell(Kapital, aktien_anzahl_list, aktien_preis_anzahl_empfehlung_list, Startkapital, portfolio_wert)
    write_csv(aktien_preis_anzahl_empfehlung_list)
    
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "FAMA.SHARES - Neue Verkaufsempfehlung"
    msg.attach(MIMEText(message, "plain"))
    msg = attach_csv(msg)
    msg = msg.as_string()
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg)


# In[55]:


def send_email_buy(receiver_email, Kapital, aktien_anzahl_list, aktien_preis_anzahl_empfehlung_list, Startkapital, portfolio_wert):
    message = build_email_buy(Kapital, aktien_anzahl_list, aktien_preis_anzahl_empfehlung_list, Startkapital, portfolio_wert)
    write_csv(aktien_preis_anzahl_empfehlung_list)
    
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "FAMA.SHARES - Neue Kaufempfehlung"
    msg.attach(MIMEText(message, "plain"))
    msg = attach_csv(msg)
    msg = msg.as_string()
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg)


# In[117]:


def receive_emails():
    email_suggestion_list = []
    
    today = date.today()
    
    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate
    imap.login(sender_email, password)
    
    imap.select("INBOX")
    status, messages = imap.search(None, 'SINCE "{}"'.format(str(today.strftime("%d-%b-%Y"))))
    messages = messages[0].split(b' ')
    print(messages)
    if messages == [b'']:
        # return empty list if no mail received
        return []
    for mail in messages:
        received_csv = {"buy": [], "sell": []} 
        res, msg = imap.fetch(mail, "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding)
                
                if "Verkauf" in subject or "Kauf" in subject:
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = From.decode(encoding)
                    if not msg.is_multipart():
                        raise Exception("Email is not a multipart! From: {}, Subject: {}".format(From, subject))
                        
                    for part in msg.walk():
                        content_disposition = str(part.get("Content-Disposition"))
                        if "attachment" in content_disposition:
                            folder_name = clean(From)
                            if not os.path.isdir(folder_name):
                                # make a folder for this email (named after the subject)
                                os.mkdir(folder_name)
                            if "Verkauf" in subject:
                                filename = str(date.today()) + "_sell.csv"
                                filepath = os.path.join(folder_name, filename)
                                open(filepath, "wb").write(part.get_payload(decode=True))
                                sell = read_csv(filepath)
                                received_csv["sell"] += sell
                            elif "Kauf" in subject:
                                filename = str(date.today()) + "_buy.csv"
                                filepath = os.path.join(folder_name, filename)
                                open(filepath, "wb").write(part.get_payload(decode=True))
                                buy = read_csv(filepath)
                                received_csv["buy"] += buy
                    mail_address=re.findall(r'"(.*?)"', From)[0]
                    email_suggestion_list.append([mail_address, received_csv])
    status, messages = imap.search(None, "ALL")
    return email_suggestion_list


# In[118]:


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)


# In[120]:


#print(receive_emails())


# In[42]:


def attach_csv(msg):
    fileToSend = "aktien.csv"
    
    ctype, encoding = mimetypes.guess_type(fileToSend)
 
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    if maintype == "text":
        fp = open(fileToSend)
        # Note: we should handle calculating the charset
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "image":
        fp = open(fileToSend, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "audio":
        fp = open(fileToSend, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(fileToSend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
    msg.attach(attachment)
    return msg


# In[43]:


def build_email_buy(Kapital, aktien_anzahl_list, aktien_preis_anzahl_empfehlung_list, Startkapital, portfolio_wert):
    aktien_bestand_string = ""
    for aktie in aktien_anzahl_list:
        aktien_bestand_string += aktie[0] + ": " + str(aktie[1]) + "Stück, Einstandskurs: "+str(aktie[2])+"\r\n"
        
    aktien_buy_string = ""
    for aktie in aktien_preis_anzahl_empfehlung_list:
        aktien_buy_string += "-----\n"
        aktien_buy_string += aktie[0] + "\n"
        aktien_buy_string += "Aktueller Wert: " + str(aktie[2]) + " Euro\r\n"
        aktien_buy_string += "Empfohlene Anzahl: " + str(aktie[1]) + "\r\n"
        aktien_buy_string += "Stärke des Kaufsignals: " + str(aktie[3]) + "\r\n"
        aktien_buy_string += "-----\r\n"
        
    message = """Guten Tag,
    
Es wird empfohlen folgende Aktie(n) zu kaufen:
{aktien_buy_string}
    
Falls Sie sich fuer einen Kauf entscheiden, schicken Sie uns bitte die beigefuegt CSV-Datei ausgefuellt zurueck.
    
PS:
Ihr aktuelles Kapital liegt bei {Kapital} Euro, ihr Startkapital lag bei. Der tagesaktuelle Wert ihres Portfolios beläuft sich auf Euro
    
Hier ihre aktuellen Aktienbestaende:
{aktien_bestand_string}""".format(aktien_buy_string=aktien_buy_string, Kapital=Kapital, aktien_bestand_string=aktien_bestand_string)
    
    return message


# In[44]:


def build_email_sell(Kapital, aktien_anzahl_list, aktien_preis_anzahl_empfehlung_list, Startkapital, portfolio_wert):
    print(Startkapital)
    aktien_bestand_string = ""
    for aktie in aktien_anzahl_list:
        aktien_bestand_string += aktie[0] + ": " + str(aktie[1]) + "Stück, Einstandskurs: "+str(aktie[2])+ "\r\n"
        
    aktien_buy_string = ""
    for aktie in aktien_preis_anzahl_empfehlung_list:
        aktien_buy_string += "-----\n"
        aktien_buy_string += aktie[0] + "\n"
        aktien_buy_string += "Aktueller Wert: " + str(aktie[2]) + " Euro\r\n"
        aktien_buy_string += "Empfohlene Anzahl: " + str(aktie[1]) + " Euro\r\n"
        aktien_buy_string += "Stärke des Verkaufsignals: " + str(aktie[3]) + "\r\n"
        aktien_buy_string += "-----\r\n"
        
    message = """Guten Tag,
    
Es wird empfohlen folgende Aktie(n) zu verkaufen:
{aktien_buy_string}
    
Falls Sie sich fuer einen Verkauf entscheiden, schicken Sie uns bitte die beigefuegte CSV-Datei ausgefuellt zurueck.
    
PS:
Ihr aktuelles Kapital liegt bei {Kapital} Euro, ihr Startkapital lag bei. Der tagesaktuelle Wert ihres Portfolios beläuft sich auf Euro
    
Hier ihre aktuellen Aktienbestaende:
{aktien_bestand_string}""".format(aktien_buy_string=aktien_buy_string, Kapital=Kapital, aktien_bestand_string=aktien_bestand_string)
    
    return message


# In[45]:


def write_csv(aktien_preis_anzahl_empfehlung_list):
    with open('aktien.csv', mode='w') as csv_file:
        aktien_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        aktien_writer.writerow(['Aktie', 'Anzahl', 'Wert', 'Zusatzkosten'])
        for aktie in aktien_preis_anzahl_empfehlung_list:
            aktien_writer.writerow([aktie[0], aktie[1], aktie[2], '1.0'])
        


# In[1]:


def read_csv(filepath):
    aktien_anzahl_preis_zuatzkosten= []
    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0 and row != []:
                aktien_anzahl_preis_zuatzkosten.append(row)
            line_count += 1
    return aktien_anzahl_preis_zuatzkosten
    


# In[ ]:




