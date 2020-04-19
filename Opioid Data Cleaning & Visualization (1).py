#!/usr/bin/env python
# coding: utf-8

# In[252]:


import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#from matplotlib import pyplot

import geopandas as gpd

import descartes


pd.set_option('display.max_columns', None)


# In[49]:


df_opioids = pd.read_csv("opioids.csv")
df = pd.read_csv("prescriber-info.csv")
df2 = pd.read_csv("overdoses.csv")


# In[253]:


df2.head()


# In[254]:


df_overdoses = df2.drop(columns = ['State'])
df_overdoses


# In[255]:


df_o1 = df_overdoses.rename(columns={"Abbrev": "State"})
df_o1.sort_values('State')


# In[272]:


df_o_new = df_o1.replace(',','', regex=True)
df_o_new


# In[277]:


df_o_new['Deaths'] = df_o_new['Deaths'].astype(str).astype(int)
df_o_new['Population'] = df_o_new['Population'].astype(str).astype(int)
df_o_new


# In[284]:


df_o_new['Deaths Per 100,000 People'] = df_o_new.Deaths / df_o_new.Population *100000
decimals = 1    
df_o_new['Deaths Per 100,000 People'] = df_o_new['Deaths Per 100,000 People'].apply(lambda x: round(x, decimals))
df_o_new
df_o_new.sort_values('Deaths Per 100,000 People', ascending = False)


# In[270]:


usa = gpd.read_file("states.shp")
# check the GeoDataframe
usa.head()


# In[282]:


usa.plot()


# In[280]:


# join the geodataframe with the csv dataframe
merged = usa.merge(df_o_new, how='left', left_on="STATE_ABBR", right_on="State")
merged = merged[['STATE_ABBR', 'geometry', 'Population', 'Deaths', 'State',
                'Deaths Per 100,000 People']]
merged.head()


# In[352]:


# set the value column that will be visualised
variable = 'Deaths Per 100,000 People'
# set the range for the choropleth values
vmin, vmax = 0, 35
# create figure and axes for Matplotlib
fig, ax = plt.subplots(1, figsize=(50, 20))
# remove the axis
ax.axis('off')
# add a title and annotation
ax.set_title('Opioid Overdoses Per 100,000 People in 2014', fontdict={'fontsize': '50', 'fontweight' : '3'})
ax.annotate('Source: Kaggle - https://www.kaggle.com/apryor6/us-opiate-prescriptions', xy=(0.5, .05), xycoords='figure fraction', fontsize=20, color='#555555')
# Create colorbar legend
sm = plt.cm.ScalarMappable(cmap='Oranges', norm=plt.Normalize(vmin=vmin, vmax=vmax))
# empty array for the data range
sm.set_array([]) # or alternatively sm._A = []. Not sure why this step is necessary, but many recommends it
# add the colorbar to the figure
fig.colorbar(sm)
# create map
merged.plot(column=variable, cmap='Oranges', linewidth=0.8, ax=ax, edgecolor='0.8')

#Add Labels
#merged['coords'] = merged['geometry'].apply(lambda x: x.representative_point().coords[:])
#merged['coords'] = [coords[0] for coords in merged['coords']]
#for idx, row in merged.iterrows():
#    plt.annotate(s=row['Deaths Per 100,000 People'], xy=row['coords'],horizontalalignment='center')


# In[72]:


df.head()


# In[8]:


df.tail()


# In[285]:


df_prescriber = df[['Gender', 'State', 'Credentials', 'Specialty', 'Opioid.Prescriber']]
df_prescriber.head()


# In[74]:


df_prescriber.count()


# In[75]:


df = df_prescriber.sort_values('State')
df


# In[106]:


df_new = df.drop(df[df.State.isin(["AA", "ZZ", "AE", "GU", "PR", "VI"])].index)
df_new


# In[77]:


state_group = df_new.groupby('State')
state_group


# In[336]:


state_sum_df = state_group.sum().reset_index()
state_sum_df


# In[337]:


new = state_sum_df.merge(df_o_new, on='State')
new


# In[338]:


new['Opioid.Prescriber'] = new['Opioid.Prescriber'].astype(str).astype(int)
new = new.rename(columns={"Opioid.Prescriber": "Prescriber"})


# In[339]:


new['Opioid Prescribers Per 100,000 People'] = new.Prescriber / new.Population *100000
new


# In[353]:


sns.set(rc={'figure.figsize':(25,8.27)})


# In[354]:


prescriber_states = sns.barplot(x="State", y="Opioid Prescribers Per 100,000 People", data=new, color = 'orange')

prescriber_states.axes.set_title("Opioid Prescribers Per 100,000 People by State",fontsize=30)
prescriber_states.set_xlabel("State",fontsize=20)
prescriber_states.set_ylabel("Opioid Prescribers",fontsize=20)

sns.set_context("poster")


# In[113]:


special_group = df_new.groupby('Specialty')
special_group


# In[132]:


special_sum_df = special_group.sum().reset_index()
special_sum_df = special_sum_df.sort_values('Opioid.Prescriber', ascending = False)
special_sum_df


# In[355]:


top_ten_special = special_sum_df.head(10)
top_ten_special


# In[356]:


top_ten_special = top_ten_special.rename(columns={"Opioid.Prescriber": "Opioid Prescribers"})


# In[357]:


sns.set(rc={'figure.figsize':(8,8)})


# In[358]:


plt.rcParams["axes.labelsize"] = 15
plt.xticks(rotation = 90)
prescriber_of_opioids_specialty = sns.barplot(x="Specialty", y="Opioid Prescribers", 
                                              data=top_ten_special, palette=("Oranges_d"))
sns.set_context("poster")

