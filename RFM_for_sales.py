import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt



data = pd.read_csv(r"D:\studying\Metholodgy\csv\bank_transactions.csv 2\bank_transactions.csv")
df=pd.DataFrame(data)
print(df.head())
print(df.tail())


print(data.isnull().sum())

data.info()


filtered_data=data[['CustLocation','TransactionID']].drop_duplicates()



filtered_data.CustLocation.value_counts()[:10].plot(kind='bar')


#insert the highest one
uk_data=data[data.CustLocation=='MUMBAI']
uk_data.info()

print(uk_data.describe())
print(uk_data.columns)


uk_data = uk_data[(uk_data['TransactionAmount (INR)']>0)]
uk_data.info()


# Assuming 'uk_data' is already defined and loaded with the correct data
uk_data = uk_data[['CustomerID', 'TransactionID', 'CustomerDOB', 'CustLocation', 
                   'CustAccountBalance', 'TransactionDate', 'TransactionAmount (INR)']]
print(uk_data['TransactionDate'].isnull().sum())
# Calculate the Total Price
uk_data['TotalPrice'] = uk_data['TransactionAmount (INR)'] * uk_data['CustAccountBalance']

# Convert TransactionDate to datetime
uk_data['TransactionDate'] = pd.to_datetime(uk_data['TransactionDate'], dayfirst=True, errors='coerce')


# Find the minimum and maximum TransactionDate
min_date, max_date = uk_data['TransactionDate'].min(), uk_data['TransactionDate'].max()
print(f"Transaction Date Range: {min_date} to {max_date}")  # Example: (2016/08/02 to 2016/09/16)

# Define a specific PRESENT date for analysis (after max date in the dataset)
PRESENT = dt.datetime(2016, 9, 18)

# Display the first few rows to verify the results
print(uk_data.head())



rfm= uk_data.groupby('CustomerID').agg({'TransactionDate': lambda date: (PRESENT - date.max()).days, 'TransactionID': lambda num: len(num), 'TotalPrice': lambda price: price.sum()})


print(rfm.head())


rfm.columns =['recency','frequency', 'monetary']



# Use pd.cut() to create equal-sized bins based on the range of values
rfm['f_quartile'] = pd.cut(rfm['frequency'], 4, labels=['1', '2', '3', '4'])

# Similarly, calculate Recency and Monetary quartiles
rfm['r_quartile'] = pd.cut(rfm['recency'], 4, labels=['4', '3', '2', '1'])
rfm['m_quartile'] = pd.cut(rfm['monetary'], 4, labels=['1', '2', '3', '4'])


print(rfm.head())



rfm['RFM_Score'] = rfm.r_quartile.astype(str)+rfm.f_quartile.astype(str) + rfm.m_quartile.astype(str)
print(rfm.head())


print(rfm[rfm['RFM_Score']=='111'].sort_values('monetary',ascending=False).head())
print(rfm.columns)





