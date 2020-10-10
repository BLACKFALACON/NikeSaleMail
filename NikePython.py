from bs4 import BeautifulSoup
import requests
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import time

finish=1
sure=0
while finish!=0:
    time.sleep(60)
    sure+=1  
    if sure ==60:
        try:
            pageLink="https://www.nike.com/tr/w/erkek-179-giysiler-3f27bz6ymx6znik1?sort=priceAsc"
            r = requests.get(pageLink)
            source = BeautifulSoup(r.content,"lxml")
            lists_money=source.find_all("div",attrs={"class":"product-price"}) 
            lists_model=source.find_all("div",attrs={"class":"product-card__subtitle"})
            print("Veriler başarılı bir şekilde çekildi.")
            model=pd.Series(lists_model)
            fiyat=pd.Series(lists_money)
            df=pd.DataFrame(data=model,columns=['Model'])
            df['Fiyat']=fiyat
            mailIcerik=str(df)
        except:
            print("Hata:", sys.exc_info()[0])
            sure=60
            
        try:
            mail = smtplib.SMTP("smtp.gmail.com",587)
            mail.ehlo()
            mail.starttls()
            mail.login("sahinbolukbasii@gmail.com", "**")

            mesaj = MIMEMultipart()
            mesaj["From"] = "sahinbolukbasii@gmail.com"           # Gönderen
            mesaj["Subject"] = "Nike İndirimli Ürünler"    # Konusu
            mesaj["To"] = "shnblkbssss@gmail.com"          # Alıcı
            body_text = MIMEText(mailIcerik, "plain")  
            mesaj.attach(body_text)

            mail.sendmail(mesaj["From"], mesaj["To"], mesaj.as_string())
            print("Mail başarılı bir şekilde gönderildi.")
            mail.close()
            sure=0      
        except:
            print("Hata:", sys.exc_info()[0])
            sure=60