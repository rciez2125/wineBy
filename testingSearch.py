import urllib.request
import re
from bs4 import BeautifulSoup
import math
from selenium import webdriver
import time
import numpy as np 
import pandas as pd
import os 

import multiprocessing
from joblib import Parallel, delayed
num_cores = multiprocessing.cpu_count()
print(num_cores)

df = pd.read_csv('wineList.csv')

# filter out wine that's too expensive
priceCap = 25
df = df[df.Price<priceCap]
df = df.drop(columns = 'Unnamed: 0')
df = df.reset_index(drop=True)


def index_marks(nrows, chunk_size):
    return range(chunk_size, math.ceil(nrows / chunk_size) * chunk_size, chunk_size)

def split(df, chunk_size):
    indices = index_marks(df.shape[0], chunk_size)
    return np.split(df, indices)

def searchAvailability(df):
	driver = webdriver.Firefox()
	onlineAvail = []
	storeSearch = []
	for n in range(len(df)):
		#print(n, 'of', len(df))
		urlpage = df.link.iloc[n]
		driver.get(urlpage)
		onlineResults = driver.find_elements_by_xpath("//*[@class='inv_online_container']//*[@class='prodText_nob']//*[@id='onlineAvailability']")
		storeResults = driver.find_elements_by_xpath("//*[@class='inv_store_container']//*[@class='p_fLeft']")

		if len(onlineResults)>0:
			onlineAvail.append(onlineResults[0].text)
		else: 
			onlineAvail.append('None Available')

		if len(storeResults)>0:
			for s in storeResults:
				link = s.find_element_by_tag_name('a')
				product_link = link.get_attribute("href")
				#print(product_link)
				storeSearch.append(product_link)
		else:
			storeSearch.append('')
	df['OnlineStock'] = onlineAvail
	df['StoreURL'] = storeSearch
	driver.quit()

	df.to_csv('wineWithwebsites'+str(df.index[0])+str(df.index[-1])+'.csv')
	time.sleep(10)
	#return(df)

chunks = split(df, 100)
# this could probably be parallelized

#results = Parallel(n_jobs=2)(map(delayed(searchAvailability), chunks))

#for c in chunks:
#	searchAvailability(c)
#	print("Shape: {}; {}".format(c.shape, c.index))

# smush all of the smaller csv files back to one dataframe and save 
for c in chunks:
	s = 'wineWithwebsites'+str(c.index[0])+str(c.index[-1])+'.csv'
	if c.index[0] == 0:
		df_all = pd.read_csv(s, index_col=0)
		os.remove(s)
	else:
		df = pd.read_csv(s, index_col=0)
		df_all = df_all.append(df)
		os.remove(s)
df_all.to_csv('wineListwithStores.csv')