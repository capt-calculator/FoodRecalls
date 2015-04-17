
# coding: utf-8

# In[2]:

import requests
import pandas as pd
import json
import plotly.plotly as py
from plotly.graph_objs import *


# In[3]:

api_key = 'XXX'

class_one = 'https://api.fda.gov/food/enforcement.json?&search=classification:"Class+I"&count=report_date'
class_two = 'https://api.fda.gov/food/enforcement.json?&search=classification:"Class+II"&count=report_date'
class_three = 'https://api.fda.gov/food/enforcement.json?&search=classification:"Class+III"&count=report_date'

class_total = 'https://api.fda.gov/food/enforcement.json?&count=report_date'


# In[4]:

responses = [
    json.loads(requests.get(class_one).text),
    json.loads(requests.get(class_two).text),
    json.loads(requests.get(class_three).text),
    json.loads(requests.get(class_total).text),
]



# In[5]:

columns = ['Class-I', 'Class-II', 'Class-III', 'Total']

data = []

for response in responses:
    data.append(pd.DataFrame(response['results']).set_index('time'))



# In[12]:

final = pd.concat([df for df in data],axis=1).fillna(0)
final.columns = [columns]
final.index = final.index.to_datetime()
final = final.tz_localize('UTC')


#### Make the Plotly Graph

# In[31]:

final = final.ix[-52:,:]
final.head()


# In[41]:

colors = ['#005869','#00856A','#8DB500']

trace1 = Bar(
    x=final.index,
    y=final['Class-III'],
    name='Class-III',
    marker=Marker(
        color=colors[0]
    )
)
            
trace2 = Bar(
    x=final.index,
    y=final['Class-II'],
    name='Class-II',
    marker=Marker(
        color=colors[1]
    )
)

trace3 = Bar(
    x=final.index,
    y=final['Class-I'],
    name='Class-I',
    marker=Marker(
        color=colors[2]
    )
)

data = Data([trace1,trace2,trace3])

layout = Layout(
    barmode='stack',
    title='Food Product Safety Recalls',

    xaxis=XAxis(
        tickangle=-45,
        title='Source: OpenFDA'
    ),

    yaxis=YAxis(
        title='Number of Recall Events')
)

figure = Figure(data=data, layout=layout)

py.iplot(figure, filename='FoodRecalls')

