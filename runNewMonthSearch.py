from datetime import datetime
import pandas as pd

# run the things to scrape the data
#import scrapeAllProducts.py
#import testingSearch.py
#import searchStores.py

# get current date & time
now = datetime.now()
# save archive files
n = (str(now)[:10])

df = pd.read_csv('wineList.csv')
df.to_csv('wineList'+n+'.csv')

df = pd.read_csv('wineListwithStores.csv')
df.to_csv('wineListwithStores'+n+'.csv')

df = pd.read_csv('wineListFullAvailability.csv')
df.to_csv('wineListFullAvailability'+n+'.csv')


# keep only the stuff that's in stores:
df = pd.read_csv('wineListFullAvailability.csv', index_col = 'Unnamed: 0')
stores = ['6526', '0247', '9213', '0220', '0224', '0214']

keepInfo = ['OnlineStock', 'PartNumber', 'Price', 'StoreURL','link', 'product']

allkeepers = stores + keepInfo

print(allkeepers)

df1 = df[allkeepers]
df2 = df1.dropna(subset=stores, how='all')
df2.reset_index(drop = True, inplace = True)
#df2 = df1[df1['6526'] == 'nan']

#print(df1['6526'].iloc[2])

df2 = df2.rename(columns={"6526": "Murrysville-Blue Spruce", "0247": "Shadyside-Whole Foods", "9213": "Plum-Holiday Park", "0220": "Oakmont", "0224":"Squirrel Hill - Murray Ave", "0214": "Fox Chapel - Waterworks"})
df2.to_csv('RelatedData.csv')


