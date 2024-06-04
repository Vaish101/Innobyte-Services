#!/usr/bin/env python
# coding: utf-8

# In[3]:


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

get_ipython().run_line_magic('matplotlib', 'inline')


# In[7]:


import pandas as pd


file_path = 'C:/Users/vheda/Downloads/AmazonSaleReport.csv'
df = pd.read_csv(file_path, encoding='latin1')


# In[8]:


df


# In[9]:


df = df.drop(columns=['index'])


# In[10]:


df.head()


# In[11]:


df.isnull().sum()


# In[12]:


df.duplicated()


# In[13]:


df.corr()


# In[18]:


df = df.drop(columns=['index'])


# In[19]:


numeric_df = df.select_dtypes(include=['float64', 'int64'])

# Calculate the correlation matrix
corr_matrix = numeric_df.corr()

# Display the correlation matrix
print(corr_matrix)


# In[20]:


df.info()


# In[22]:


sns.heatmap(numeric_df.corr(), annot=True, cmap="YlGnBu")


# In[23]:


df['Date'] = pd.to_datetime(df['Date'], format='%m-%d-%y', errors='coerce')


# In[25]:


sales_overview = df.groupby('Date').agg({'Amount': 'sum', 'Order ID': 'count'}).reset_index()
sales_overview.rename(columns={'Order ID': 'Number of Orders'}, inplace=True)


# In[29]:


fig, ax1 = plt.subplots(figsize=(8,6))
ax1.plot(sales_overview['Date'], sales_overview['Amount'], color='b',marker='o', label='Total Sales')
ax1.set_xlabel('Date')
ax1.set_ylabel('Total Sales', color='b')
ax1.tick_params('y', colors='b')
ax2 = ax1.twinx()
ax2.plot(sales_overview['Date'], sales_overview['Number of Orders'], color='g',marker='x', label='Number of Orders')
ax2.set_ylabel('Number of Orders', color='g')
ax2.tick_params('y', colors='g')
fig.tight_layout()
plt.title('Total Sales and Number of Orders Over Time')
plt.show()


# In[31]:


custom_palette = sns.color_palette("husl",9)
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='Category', order=df['Category'].value_counts().index,palette=custom_palette)
plt.title('Distribution of Product Categories')
plt.xlabel('Category')
plt.ylabel('Count')
plt.show()


# In[33]:


custom_palette = sns.color_palette("husl",9)
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='Size', order=df['Size'].value_counts().index,palette=custom_palette)
plt.title('Distribution of Product Sizes')
plt.xlabel('Size')
plt.ylabel('Count')
plt.show()


# In[34]:


color_palette = ['#a7c957', '#fb6f92']
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x='Fulfilment', order=df['Fulfilment'].value_counts().index, palette=color_palette)
plt.title('Distribution of Fulfillment Methods')
plt.xlabel('Fulfillment Method')
plt.ylabel('Count')
plt.show()


# In[35]:


custom_palette = sns.color_palette("pastel")
plt.figure(figsize=(6, 4))
fulfillment_effectiveness = df.groupby(['Fulfilment', 'Status']).size().unstack().fillna(0)

fulfillment_effectiveness.plot(kind='bar', stacked=True, figsize=(14, 7),color=custom_palette)
plt.title('Fulfillment Methods Effectiveness')
plt.xlabel('Fulfillment Method')
plt.ylabel('Number of Orders')
plt.legend(title='Order Status')
plt.show()


# In[36]:


state_segmentation = df['ship-state'].value_counts().reset_index()
state_segmentation.columns = ['State', 'Number of Orders']
custom_palette = sns.color_palette("rocket_r", len(state_segmentation))
plt.figure(figsize=(14, 7))
sns.barplot(data=state_segmentation, x='State', y='Number of Orders',palette=custom_palette)
plt.title('Customer Segmentation by State')
plt.xlabel('State')
plt.ylabel('Number of Orders')
plt.xticks(rotation=90)


# In[37]:


plt.show()


# In[38]:


geo_sales = df.groupby(['ship-state', 'ship-city']).agg({'Amount': 'sum'}).reset_index()


# In[39]:


state_sales = geo_sales.groupby('ship-state').agg({'Amount': 'sum'}).reset_index()
state_sales = state_sales.sort_values('Amount', ascending=False)
plt.figure(figsize=(14, 7))
sns.barplot(data=state_sales, x='ship-state', y='Amount', palette='pastel')
plt.title('Sales by State')
plt.xlabel('State')
plt.ylabel('Total Sales')
plt.xticks(rotation=90)
plt.show()


# In[40]:


city_sales = geo_sales.groupby('ship-city').agg({'Amount': 'sum'}).reset_index()
city_sales = city_sales.sort_values('Amount', ascending=False).head(10)
plt.figure(figsize=(14, 7))
sns.barplot(data=city_sales, x='ship-city', y='Amount', palette='pastel')
plt.title('Sales by City (Top 10)')
plt.xlabel('City')
plt.ylabel('Total Sales')
plt.xticks(rotation=90)
plt.show()

