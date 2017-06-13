#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

K = []
L = []
KU = []
L1 = []

#pagrindinis link'as, naudojant scrapinimui einant per pasiūlymų puslapius
burl = "http://www.alio.lt/nekilnojamas-turtas/butai/parduoda.html?page="

#BeautifulSoup standartinis puslapio duomenų paruošimas
m = requests.get(burl+"1")
d = m.content
soup = BeautifulSoup(d, "html.parser")

#page = soup.find_all("div", {"class":"paging_b"}) - šitą, naudočiau, jei kada norėčiau visus pasiūlymus

#start = time.time() - jei reikia, galima paskaičiuoti laiką, kiek užtrunka
#int(page[0].find_all("a")[4].text) - šitą, naudočiau, jei kada norėčiau visus pasiūlymus, dabar tik pirmus 50 puslapių
for i in range(1,50):
	c = requests.get(burl+str(i))
	d = c.content
	soup = BeautifulSoup(d, "html.parser")
	a = soup.find_all("div", {"class":"price"}) # Kaina
	b = soup.find_all("div", {"class":"description"}) # Kamb.skaičius, Plotis ir Meai
	l = soup.find_all("a", {"class":"vertiselink cursor-pointer"}) #Url link'as

#atitinakamų duomenų suradimas ir pridėjimas prie atitinkamo list'o
	for oi in a:
	    K.append(int(oi.find("span", {"class":"main_price"}).text.replace(" ", "").replace("€","")))
	
	for op in b:
		if len(op.text.split("|")) == 3:
			ab = op.text.split("|")
			ab.insert(2, None)
			L.append(ab)
		elif len(op.text.split("|")) == 4:
			L.append(op.text.split("|"))
		else:
			pass

	for h1 in l:
		if h1["href"] not in L1:
			L1.append(h1['href'])
	
	#pridedama reikiamus list'ų duomenis į dict, kad būtų galima vėliau panaudoti pandas 
	for p,n,q in zip(K,L,L1):
	    dic = {}
	    dic["Kaina"] = p
	    #print(dic["Kaina"])
	    dic["Metai"] = n[2]
	    #print(dic["Metai"])
	    dic["Plotas"] = n[0]
	    #print(dic["Plotas"])
	    dic["Skaičius"] = n[1]
	    #print(dic["Skaičius"])
	    dic["Url"] = q
	    KU.append(dic)

	stop = time.time()
	duration = stop-start
	print(duration) 

#sukuriam pandas dataframe ir atrenkam reikiamus duomenis: pig. ir brang. kainą bei url link'ą, kad būtų galima iš kartą patikrinti
df = pd.DataFrame(KU)

#kad pandas rodytų pilną Url link'ą
pd.set_option('display.max_colwidth', -1)
print(df)
print("Pigiausias variantas "+str(df['Kaina'].min())+" "+str(list(df.loc[df['Kaina'].idxmin()])[-1]))
print("Brangusias variantas "+str(df["Kaina"].max())+" "+str(list(df.loc[df['Kaina'].idxmax()])[-1]))