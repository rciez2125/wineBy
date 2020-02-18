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


#num_cores = multiprocessing.cpu_count()
#print('numcores', num_cores)

#urlpage = 'https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/CatalogSearchResultView?storeId=10051&catalogId=10051&langId=-1&categoryId=1334029&sortBy=5&categoryType=&searchSource=E&pageView=&beginIndex=0#facet:&productBeginIndex:0&orderBy:&pageView:&minPrice:&maxPrice:&pageSize:&'
#urlpage = 'https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/CatalogSearchResultView?storeId=10051&catalogId=10051&langId=-1&categoryId=1334028&pageView=&beginIndex=0&searchSource=E&sortBy=5#facet:&productBeginIndex:0&orderBy:&pageView:&minPrice:&maxPrice:&pageSize:45&'
#urlpage = 'https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/CatalogSearchResultView?storeId=10051&catalogId=10051&langId=-1&categoryId=1334028&pageView=&beginIndex=0&searchSource=E&sortBy=5#facet:&productBeginIndex:0&orderBy:&pageView:&minPrice:&maxPrice:&pageSize:45&'
#'https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/CatalogSearchResultView?storeId=10051&catalogId=10051&langId=-1&categoryId=1334028&pageView=&beginIndex=0&searchSource=E&sortBy=5#facet:&productBeginIndex:15&orderBy:&pageView:&minPrice:&maxPrice:&pageSize:&'
urlpage = 'https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/CatalogSearchResultView?storeId=10051&catalogId=10051&langId=-1&categoryId=1334028&pageView=&beginIndex=0&searchSource=E&sortBy=5#facet:&productBeginIndex:&orderBy:&pageView:&minPrice:&maxPrice:&pageSize:15&'
#urlpage = 'https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/CatalogSearchResultView?storeId=10051&catalogId=10051&langId=-1&categoryId=1334032&variety=Online+Special+Wine&categoryType=&top_category=1334031&sortBy=5&searchSource=E&pageView=&beginIndex=0#facet:&productBeginIndex:0&orderBy:&pageView:&minPrice:&maxPrice:&pageSize:&'
page = urllib.request.urlopen(urlpage)
soup = BeautifulSoup(page, 'html.parser')

#print(soup.prettify())
#with open("output1.txt", "w") as file:
#    file.write(str(soup))
#mvill = 6526
stringSoup = str(soup)

s = stringSoup.find('Showing')
t = stringSoup[s:s+1000]
t2 = t.strip(' ')
t3 = t2.find('of')
t4 = t2[t3+3:]
t5 = t4.find(')')
t6 = t4[:t5]
totalProducts = float(re.sub(r"\W", "", t6))
print(totalProducts)

data = []
priceData = []
base = 'https://www.finewineandgoodspirits.com'
driver = webdriver.Firefox()
#print(math.ceil(totalProducts/15))
print(math.ceil(totalProducts/15))
pagestoSearch = math.ceil(totalProducts/15)

#driver.quit()
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
	#time.sleep(4)
	print(n)

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

#if __name__ == "__main__":
	#processed_list = Parallel(n_jobs=2)(delayed(for i in range(pagestoSearch)(scrapeProductList(i, data, priceData))))

#for i in range(pagestoSearch):(scrapeProductList(i))
#driver.quit()
#results = Parallel(n_jobs=1)(map(delayed(scrapeProductList), range(10)))
# from the url data, find the product number 


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
