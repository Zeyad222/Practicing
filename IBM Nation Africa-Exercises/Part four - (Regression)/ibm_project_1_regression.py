# -*- coding: utf-8 -*-
"""IBM-Project-1-Regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jYbGZOmwnYpZif7Bs77_TxW2xm8lhKEd
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

path = "/content/drive/MyDrive/IBM - Data Science/Analysis project(IBM-Nation)/Project-1-Analysis/Files/Product Data Set - Student 2 of 3.csv"
product_data = pd.read_csv(path, sep = '|')
product_data.head(2)

path = "/content/drive/MyDrive/IBM - Data Science/Analysis project(IBM-Nation)/Project-1-Analysis/Files/Transaction Data Set - Student 3 of 3.csv"
transactions_data = pd.read_csv(path, sep = '|')
transactions_data.head(2)

path = "/content/drive/MyDrive/IBM - Data Science/Analysis project(IBM-Nation)/Project-1-Analysis/Files/Customer Data Set - Student 1 of 3.csv"
customer_data = pd.read_csv(path, sep = ',')
customer_data.head(2)

customer_data['INCOME'] = customer_data['INCOME'].map(lambda x: x.replace('$','')) 
customer_data['INCOME'] = customer_data['INCOME'].map(lambda x: int(x.replace(',','')))

product_data['UNIT LIST PRICE'] = product_data['UNIT LIST PRICE'].map(lambda x: float(x.replace('$','')))

trans_products = transactions_data.merge(product_data, how= 'inner', left_on ='PRODUCT NUM', right_on = 'PRODUCT CODE')
trans_products.head()

trans_products['Total_Price'] = trans_products['QUANTITY PURCHASED'] * trans_products['UNIT LIST PRICE'] * (1-trans_products['DISCOUNT TAKEN'])
trans_products.head()

customer_prod_categ = trans_products.groupby(['CUSTOMER NUM','PRODUCT CATEGORY']).agg({'Total_Price': 'sum'})
customer_prod_categ.head()

customer_prod_categ.reset_index()

customer_pivot = customer_prod_categ.pivot_table(index='CUSTOMER NUM', columns='PRODUCT CATEGORY', values='Total_Price')
customer_pivot.head()

trans_total_spend = trans_products.groupby('CUSTOMER NUM').agg({'Total_Price': 'sum'}).\
rename(columns = {'Total_Price':'Total Spent'})
trans_total_spend.head()

customer_KPIS = customer_pivot.merge(trans_total_spend, how = 'inner', left_index= True , right_index = True)
customer_KPIS.head()

customer_all_view = customer_data.merge(customer_KPIS, how ='inner', left_on='CUSTOMERID', right_index=True)
customer_all_view=customer_all_view.fillna(0)
customer_all_view.head()

"""# Regression"""

DF_input=customer_all_view[['GENDER','AGE','INCOME','EXPERIENCE SCORE','LOYALTY GROUP','HOUSEHOLD SIZE','MARITAL STATUS']]
DF_input.head()

# Loyalty group and Marital status are strings
DF_input["MARITAL STATUS"].unique()

DF_input["LOYALTY GROUP"].unique()

#  pd.get_dummies(DF_input["MARITAL STATUS"]).head()

#  pd.get_dummies(DF_input["LOYALTY GROUP"]).head()

def encode_loyalty(value):
  if value =='enrolled':
    return 1
  else:
   return 0

DF_input["LOYALTY GROUP"] = DF_input["LOYALTY GROUP"].apply(encode_loyalty)

# DF_input.head()

"""If we run line 24 firstly it will divide LOYALTY GROUP column into two cols, and we don't need that. So, we make a function for this col separately"""

DF_input = pd.get_dummies(DF_input)
DF_input.head()

from sklearn import preprocessing

DF_input_column_names = DF_input.columns.values

DF_input_np=preprocessing.minmax_scale(DF_input)

Reg_input_scaled=pd.DataFrame(DF_input_np, columns=DF_input_column_names)
Reg_input_scaled.head()

from sklearn.model_selection import train_test_split

X_train,X_test,Y_train,Y_test = train_test_split(Reg_input_scaled,customer_all_view['Total Spent']  ,test_size=0.2, random_state=42)

from sklearn.linear_model import LinearRegression

regr = LinearRegression()
regr.fit(X_train,Y_train)
Y_pred = regr.predict(X_test)
print('Coefficients: \n', regr.coef_)

import numpy as np
np.positive(regr.coef_)

Reg_input_scaled.columns

coeficient_ = pd.DataFrame( regr.coef_ ,columns=['Coefficient'])
coeficient_.head()

coef_list = []

for num in regr.coef_:
  if num > 0:
    print("Positive")
  else:
    print("Negative")
  coef_list.append(num)
print(coef_list)

import pandas as pd
DF_input_column_names = DF_input.columns

predictor_varibale_table = pd.DataFrame(data = DF_input_column_names)
predictor_varibale_table.columns = ['predictor varibale']
# predictor_varibale_table.head(10)

table = pd.concat([predictor_varibale_table,coeficient_],axis=1)
table.head(10)

Relation_Total_Spend = pd.DataFrame( coef_list,columns= ['Relationship with Total Spend'])
Relation_Total_Spend.head()

table_last = pd.concat([table,Relation_Total_Spend],axis=1)
table_last.head(10)