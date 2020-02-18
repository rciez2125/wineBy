import pandas as pd 
from datetime import datetime
now = datetime.now()

d = pd.DataFrame({'firstName': 'Rebecca', 'lastName': 'Ciez', 'email': 'rebecca.ciez@gmail.com'}, index=[0])
s = pd.DataFrame({'date': now, 'storerec': 'looks good'}, index=[0])

d.to_csv('customerlist.csv')
s.to_csv('storerecnotes.csv')

d2 = pd.read_csv('customerlist.csv', index_col = 'Unnamed: 0')
print(d2.index[-1])
