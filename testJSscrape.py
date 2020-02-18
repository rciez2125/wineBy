import urllib.request
import re
from bs4 import BeautifulSoup
import math
from selenium import webdriver
import time
import numpy as np 
import pandas as pd 

# import libraries
# specify the url
urlpage = 'https://groceries.asda.com/search/yogurt' 
print(urlpage)
# run firefox webdriver from executable path of your choice
driver = webdriver.Firefox()#(executable_path = 'your/directory/of/choice')

# run firefox webdriver from executable path of your choice
#driver = webdriver.Firefox()

driver.get(urlpage)
# execute script to scroll down the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
# sleep for 30s
time.sleep(30)
# driver.quit()

# find elements by xpath
# at time of publication, Nov 2018:
# results = driver.find_elements_by_xpath("//*[@id='componentsContainer']//*[contains(@id,'listingsContainer')]//*[@class='product active']//*[@class='title productTitle']")

# updated Nov 2019:
results = driver.find_elements_by_xpath("//*[@class=' co-product-list__main-cntr']//*[@class=' co-item ']//*[@class='co-product']//*[@class='co-item__title-container']//*[@class='co-product__title']")
print('Number of results', len(results))


# create empty array to store data
data = []
# loop over results
for result in results:
    product_name = result.text
    link = result.find_element_by_tag_name('a')
    product_link = link.get_attribute("href")
    # append dict to array
    data.append({"product" : product_name, "link" : product_link})

# close driver 
driver.quit()
# save to pandas dataframe
df = pd.DataFrame(data)
df.to_csv('wineList.csv')