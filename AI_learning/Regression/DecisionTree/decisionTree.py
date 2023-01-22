import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

## Prepare data
file_handler = open("car_data.csv", "r")
data = pd.read_csv(file_handler, sep=",")
file_handler.close()

print (data)

data.buying[data.buying =='low'] = 1
data.buying[data.buying =='med'] = 2
data.buying[data.buying =='high'] = 3
data.buying[data.buying =='vhigh'] = 4

data.maint[data.maint =='low'] = 1
data.maint[data.maint =='med'] = 2
data.maint[data.maint =='high'] = 3
data.maint[data.maint =='vhigh'] = 4

data.doors[data.doors =='5more'] = 5

data.persons[data.persons =='more'] = 5

data.lug_boot[data.lug_boot =='small'] = 1
data.lug_boot[data.lug_boot =='med'] = 2
data.lug_boot[data.lug_boot =='big'] = 3

data.safety[data.safety =='low'] = 1
data.safety[data.safety =='med'] = 2
data.safety[data.safety =='high'] = 3

df = data

## Split data
X_train = df.loc[:,'buying':'safety']
Y_train = df.loc[:,'values']

#Create decision tree clasifier
tree = DecisionTreeClassifier(max_leaf_nodes=3,random_state=0)

#Train model
tree.fit(X_train,Y_train)

#Make prediction
prediction = tree.predict([[4,3,2,2,2,3]])
print (prediction)