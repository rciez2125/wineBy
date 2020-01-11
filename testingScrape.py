import urllib.request
import re
from bs4 import BeautifulSoup
import math
from selenium import webdriver
import time

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
mvill = 6526

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

urls = []
partNums = []
prodNames = []
prodNamesSearch = []

base = 'https://www.finewineandgoodspirits.com'
driver = webdriver.Firefox()
#print(math.ceil(totalProducts/15))
for n in range(4): #math.ceil(totalProducts/15)):
	urlpage = 'https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/CatalogSearchResultView?storeId=10051&catalogId=10051&langId=-1&categoryId=1334028&pageView=&beginIndex=0&searchSource=E&sortBy=5#facet:&productBeginIndex:'+str(n*15)+'&orderBy:&pageView:&minPrice:&maxPrice:&pageSize:15&'
	print(urlpage)
	#urlpage = 'https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/CatalogSearchResultView?storeId=10051&catalogId=10051&langId=-1&categoryId=1334032&variety=Online+Special+Wine&categoryType=&top_category=1334031&sortBy=5&searchSource=E&pageView=&beginIndex='+str(n*15)+'#facet:&productBeginIndex:0&orderBy:&pageView:&minPrice:&maxPrice:&pageSize:&'
	page = urllib.request.urlopen(urlpage)
	driver.get(urlpage)
	#browser = webdriver.PhantomJS()
	#browser.get(url)
	#html = browser.page_source
	#soup = BeautifulSoup(html, 'lxml')
	soup = BeautifulSoup(page, 'html.parser')
	stringSoup = str(soup)
	x = [m.start() for m in re.finditer('<div class="catalog_item">', stringSoup)]
	#print('x', len(x), x)
	for r in range(len(x)):
		sub = stringSoup[x[r]:]
		#print(substring[:10000])
		y = sub.find('<a href')
		z = sub.find('>', y)
		z2 = sub.find('href', z)
		z3 = sub.find('>', z2)
		z4 = sub.find('</a>', z3)
		#print(y,z)
		url3 = sub[y+9:z]
		#print(url3)
		fullurl3 = base+url3
		urls.append(fullurl3)
		a = url3.find('partNumber')
		partNum = url3[a+11:a+20]
		partNums.append(partNum)

		prodNames.append(sub[z3+1:z4])
		s = sub[z3+1:z4].replace(' ', '+')
		prodNamesSearch.append(s)

#print(len(urls), urls)
#print(len(partNums), partNums)
print(len(prodNames), prodNames)
#print(len(prodNamesSearch), prodNamesSearch)

# search through each for a given 
# search through each product for availability 

#availurl = 	'https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/ProductDetailInStore?storeId=10051&langId=-1&catalogId=10051&ItemCode=000001197&SearchNow=on&ProdName=Gentleman%27s+Collection+Forgo+Frills+Red+Blend+California&fromURL=%2Fwebapp%2Fwcs%2Fstores%2Fservlet%2FCatalogSearchResultView%3FstoreId%3D10051%26catalogId%3D10051%26langId%3D-1%26categoryId%3D1334028%26categoryType%3D%26top_category%3D%26parent_category_rn%3D%26sortBy%3D5%26searchSource%3DE%26pageView%3D%26beginIndex%3D0&countyName=&f=&storeName=&pageNum=&perPage=&storeType=&city=&zip_code=&county=&storeNO=6528'
#			'https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/ProductDetailInStore?storeId=10051&langId=-1&catalogId=10051&ItemCode=000001166&SearchNow=on&ProdName=Eppa+Suprafruta+White+Sangria+Organic+California			&fromURL=%2Fwebapp%2Fwcs%2Fstores%2Fservlet%2FCatalogSearchResultView%3FstoreId%3D10051%26catalogId%3D10051%26langId%3D-1%26categoryId%3D1334028%26categoryType%3D%26top_category%3D%26parent_category_rn%3D%26sortBy%3D5%26searchSource%3DE%26pageView%3D%26beginIndex%3D0&countyName=&f=&storeName=&pageNum=&perPage=&storeType=&city=&zip_code=&county=&storeNO=6528'