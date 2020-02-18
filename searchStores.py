import urllib.request
import re
from bs4 import BeautifulSoup
import math
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time
import numpy as np 
import pandas as pd
import os 

import multiprocessing
from joblib import Parallel, delayed
num_cores = multiprocessing.cpu_count()
print(num_cores)

# load csv file 
df = pd.read_csv('wineListwithStores.csv')

def index_marks(nrows, chunk_size):
    return range(chunk_size, math.ceil(nrows / chunk_size) * chunk_size, chunk_size)

def split(df, chunk_size):
    indices = index_marks(df.shape[0], chunk_size)
    return np.split(df, indices)

chunks = split(df, 100)

#stores = ['6526', '0247', '9213', '0220', '0224']
counties = ['Allegheny', 'Westmoreland']

print(df.columns)

def searchByStore(df, store):
	driver = webdriver.Firefox()
	data = []
	for n in df['Unnamed: 0']:
		if pd.isnull(df.loc[n, 'StoreURL']) == False:
			urlpage = df.loc[n, 'StoreURL']
			#try:
			driver.get(urlpage)
				#all_Links = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='columnDistance']")))



				#elem = driver.find_element_by_name('storeNO')
				#elem.clear()
				#elem.send_keys(store)
				#elem.submit()
			time.sleep(2)
				#results = driver.find_elements_by_xpath("//*[@class='columnDistance']")
			#except:
			#	results = ''
			
			if len(results)>1:
				results.pop(0)
				results.pop(-1)
				#print(len(results))
				for result in results:
					a = result.text
					#print(a)
					data.append(a)
			else:
				data.append('None available')
		else:
			data.append('None available')
	
	driver.quit()
	df[store] = data
	df.to_csv('wineInStores'+str(df.index[0])+str(df.index[-1])+store+'.csv')
	time.sleep(3)
	#return(df)

def searchByCounty(df, county):
	driver = webdriver.Firefox()
	dataSN = []
	dataAV = []
	for n in df['Unnamed: 0']:
		print(n)
		if pd.isnull(df.loc[n, 'StoreURL']) == False:
			urlpage = df.loc[n, 'StoreURL']
			try:
				driver.get(urlpage)
				# try and click throuhg 21 verification
				try:
					driver.find_element_by_xpath("//img[contains(@alt,'Yes')]").click()
				except:
					print('already old')
				elem = driver.find_element_by_name('storeNO')
				select = Select(driver.find_element_by_name('county'))
				select.select_by_visible_text(county)
				elem.submit()
				time.sleep(2)

				# find the results 
				results = driver.find_elements_by_xpath("//*[@class='tabContentRow']")
				if len(results)>1:
					storeNums = driver.find_elements_by_xpath("//*[@class='tabContentRow']//*[@class='columnAddress']//*[@class='boldMaroonText']")
					avail = driver.find_elements_by_xpath("//*[@class='tabContentRow']//*[@class='columnDistance']")
					for r in storeNums:
						sn = r.text
						dataSN.append(sn)
					
					for a in avail:
						av = a.text
						b = re.sub('[^0-9]','', av)
						dataAV.append(b)

					for r in range(len(results)):
						if dataSN[r] in df.columns:
							df[dataSN[r]][n] = dataAV[r]
						else:
							df[dataSN[r]]=""
							df[dataSN[r]][n] = dataAV[r]
			except:
				print('skipping because of timeout')

	driver.quit()
	df.to_csv('wineInStores'+str(df.index[0])+str(df.index[-1])+county+'.csv')
	time.sleep(10)

#searchByCounty(df, 'Allegheny')

#for c in chunks:
	# already have the data split into chunks, run each county search in parallel, put data back together
#	results = Parallel(n_jobs=2)(delayed(searchByCounty)(c,ct) for ct in counties)

for c in chunks:
	t1 = pd.read_csv('wineInStores'+str(c.index[0])+str(c.index[-1])+'Allegheny'+'.csv', index_col = 'Unnamed: 0')
	t2 = pd.read_csv('wineInStores'+str(c.index[0])+str(c.index[-1])+'Westmoreland'+'.csv', index_col = 'Unnamed: 0')

	df_both = pd.concat([t1,t2], axis = 1)
	df_both = df_both.loc[:,~df_both.columns.duplicated()]
	df_both.to_csv('wineInStores'+str(c.index[0])+str(c.index[-1])+'.csv')

	if c.index[0] == 0:
		df_all = df_both
	else:
		df_all = df_all.append(df_both)
	df_all.to_csv('wineListFullAvailability.csv')


# smush everything together
#a1 = pd.read_csv('wineInStores099Allegheny.csv', index_col = 'Unnamed: 0')
#a2 = pd.read_csv('wineInStores099Westmoreland.csv', index_col = 'Unnamed: 0')

#df_all = pd.concat([a1, a2], axis=1)
#df_all = df_all.loc[:,~df_all.columns.duplicated()]
#df_all = a1.append(a2)
#df_all.to_csv('wineListFullAvailabilityTEST.csv')
#for s in counties:
#	results = Parallel(n_jobs=1)(delayed(searchByCounty)(c, s) for c in chunks)
	
	# smush into one csv file
#	for c in chunks:
#		t = 'wineInStores'+str(c.index[0])+str(c.index[-1])+s+'.csv'
#		if c.index[0] == 0:
#			df_all = pd.read_csv(t, index_col=0)
#			os.remove(t)
#		else:
#			df = pd.read_csv(t, index_col=0)
#			df_all = df_all.append(df)
#			os.remove(t)
#	df_all.to_csv('wineInStores'+s+'.csv')

# smush everything back together from csv files 

#df_all.to_csv('wineListFullAvailability.csv')
