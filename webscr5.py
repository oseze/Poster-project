#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 16:07:03 2020

@author: osezeiyore
"""
#pip install lxml OR html5lib

from bs4 import BeautifulSoup
from requests import get
import numpy as np
import requests 
import lxml
import html5lib
import numpy
import pandas as pd
import re
import urllib.request
import random

#%%

#def main():
url ='https://www.artistsposters.com/advanced_search_result.php?keywords=&page='

'''
picture
shipping
shipping cost
'''

# preallocate lists
InfoText=[]
pricee=[]
suppe=[]
link=[]

# loop across pages on website selecting price, infotext(artist name + title) 
# and image link
for page in range(1,530): #531 #532
    pp = get(url+str(page))
    html = pp.text
    soup = BeautifulSoup(pp.content,'html.parser')  #,'lxml')    
        
    l=soup.select('h2 a')
    lik=[l[i].get('href') for i in range(len(l))]
    link.extend(lik)
    
    priceee = soup.select('p.price')
    pricee.extend(priceee)
    AA=list(soup.select('div.productPreviewContent h2 a'))
    InfoText.extend(AA)
InfoText=[str(i) for i in InfoText]

#%%
n=len(InfoText)

# preallocate lists
artist=[0]*n
year=[0]*n
title=[0]*n
price=[0]*n

#%%

# loop across all data points arranging infotext information in seperate lists
# and, converting price to float format
for i in range(n):
    res=InfoText[i]
    ress=re.search('">(.*)</a>', res)    
    result =ress.group(1)
    dat=result.split(" - ")
    pri=re.search('"price"> (.*)\xa0<span class="dn-s">EUR', str(pricee[i]))
    prii=pri.group(1).replace('.','')
    price[i]=float(prii.replace(',','.'))
    if len(dat)>2:
        artist[i]=dat[0]
        year[i]=dat[1]
        title[i]=dat[2]
    elif len(dat)==2:
        artist[i]=dat[0]
        year[i]=0
        title[i]=dat[1]

#%%

# creae dataframe with appropriate column names
df=pd.DataFrame(columns=['Price','Artist','Title','src','link'])

# place lists as colomns in dataframe
df.Price=price
df.Artist=artist
df.Title=title
# df.src=suppe
df.link=link

#%%

# filter dataframe based on the price column in the (all posters below 40 euro)
df2=df[df['Price'] <= 40]

# reset index in new dataframe
df2.reset_index(drop=True,inplace=True)


#%%

#use link to get source to download image to folder and name it after price,
# title and artist 

for i in range(len(df2)):  #range(len(df2)):
    urll = df2['link'][i]
    pp = get(urll)
    html = pp.text
    soup = BeautifulSoup(pp.content,'html.parser') 
           
    images=soup.find_all("img",attrs={"class":"productimage"})
    image_src=images[0]["src"] 
    image_src_full='https://www.artistsposters.com/'+ image_src
    df2['Artist'][i]= df2['Artist'][i].replace('/','')
    df2['Title'][i]= df2['Title'][i].replace('/','')
    urllib.request.urlretrieve(image_src_full,str(df2['Price'][i])+'euro'+df2['Artist'][i]+df2['Title'][i])
    
    soup.select("h3")
    
    # images
    # image_src=images[0]["src"] 
    # image_src_full='https://www.artistsposters.com/'+ image_src
    # urllib.request.urlretrieve(image_src_full,str(df2['Price'][i])+'euro'+df2['Artist'][i]+df2['Title'][i]+1)
                               
                                 
    



#%%

# - få fat i mål
# - klik og kom direkte ind på billedet
# - lav gui 
                                                
