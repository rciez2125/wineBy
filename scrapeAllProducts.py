import urllib.request
import re
from bs4 import BeautifulSoup
import math
from selenium import webdriver
import time
import numpy as np 
import pandas as pd
from joblib import Parallel, delayed
import multiprocessing


urlpage = 'https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/CatalogSearchResultView?storeId=10051&catalogId=10051&langId=-1&categoryId=1334028&pageView=&beginIndex=0&searchSource=E&sortBy=5#facet:&productBeginIndex:&orderBy:&pageView:&minPrice:&maxPrice:&pageSize:15&'
page = urllib.request.urlopen(urlpage)
soup = BeautifulSoup(page, 'html.parser')

stringSoup = str(soup)
s = stringSoup.find('Showing')
t = stringSoup[s:s+1000]
t2 = t.strip(' ')
t3 = t2.find('of')
t4 = t2[t3+3:]
t5 = t4.find(')')
t6 = t4[:t5]
totalProducts = float(re.sub(r"\W", "", t6))

data = []
priceData = []
base = 'https://www.finewineandgoodspirits.com'
driver = webdriver.Firefox()
pagestoSearch = math.ceil(totalProducts/15)

for n in range(pagestoSearch):
	urlpage = 'https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/CatalogSearchResultView?storeId=10051&catalogId=10051&langId=-1&categoryId=1334028&pageView=&beginIndex=0&searchSource=E&sortBy=5#facet:&productBeginIndex:'+str(n*15)+'&orderBy:&pageView:&minPrice:&maxPrice:&pageSize:15&'
	print(n)
	driver.get(urlpage)
	time.sleep(5)

	prodNames = driver.find_elements_by_xpath("//*[@class='grid_31 content-search']//*[@class='catalog_item']//*[@class='item']//*[@class = 'catalog_item_name']")
	prices = driver.find_elements_by_xpath("//*[@class='grid_31 content-search']//*[contains(@class, 'catalog_item_price')]")
	
	for result in prodNames:
		product_name = result.text
		product_link = result.get_attribute("href")
		data.append({"product" : product_name, "link" : product_link})

	for price in prices:
		prodPrice = price.text
		priceData.append(prodPrice)

#driver = webdriver.Firefox()
def scrapeProductList(n):
	driver = webdriver.Firefox()
	urlpage = 'https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/CatalogSearchResultView?storeId=10051&catalogId=10051&langId=-1&categoryId=1334028&pageView=&beginIndex=0&searchSource=E&sortBy=5#facet:&productBeginIndex:'+str(n*15)+'&orderBy:&pageView:&minPrice:&maxPrice:&pageSize:15&'
	driver.get(urlpage)

	prodNames = driver.find_elements_by_xpath("//*[@class='grid_31 content-search']//*[@class='catalog_item']//*[@class='item']//*[@class = 'catalog_item_name']")
	prices = driver.find_elements_by_xpath("//*[@class='grid_31 content-search']//*[contains(@class, 'catalog_item_price')]")
	
	for result in prodNames:
		product_name = result.text
		product_link = result.get_attribute("href")
		data.append({"product" : product_name, "link" : product_link})

	for price in prices:
		prodPrice = price.text
		priceData.append(prodPrice)
	driver.quit()
	return data, priceData

df = pd.DataFrame(data)
df['Price'] = priceData
df.Price = [x.strip('$') for x in df.Price]

partNums = []
for n in range(len(df)):
	a = df.link.iloc[n].find('partNumber')
	partNum = df.link.iloc[n][a+11:a+20]
	partNums.append(partNum)

df['PartNumber'] = partNums 
df.to_csv('wineList.csv')
