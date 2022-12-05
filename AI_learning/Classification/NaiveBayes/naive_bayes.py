# Import the neccessary modules
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB


df = pd.read_csv('titanic.csv',sep='\t')

# Drop some columns which is not relevant to the analysis (they are not numeric)
cols_to_drop = ['PassengerId','Name', 'Ticket', 'Cabin']
df = df.drop(cols_to_drop, axis=1)


# To replace missing values with interpolated values, for example Age
df['Age'] = df['Age'].interpolate()
# Drop all rows with missing data
df = df.dropna()


# First, create dummy columns from the Embarked and Sex columns
EmbarkedColumnDummy = pd.get_dummies(df['Embarked'])
SexColumnDummy = pd.get_dummies(df['Sex'])

#Second, we add these dummy columns to the original dataset
df = pd.concat((df, EmbarkedColumnDummy, SexColumnDummy), axis=1)

# Drop the redundant columns thus converted
df = df.drop(['Sex','Embarked'],axis=1)


# Separate the dataframe into X and y data
X = df.values
y = df['Survived'].values

# Delete the Survived column from X
X = np.delete(X,0,axis=1)


# Split the dataset into 70% Training and 30% Test
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=0)

# Using simple Naive Bayes classifier
nb_clf = GaussianNB()
nb_clf.fit(X_train, y_train)
print(nb_clf.score(X_test, y_test))


##  Pclass   Age      SibSp  Parch     Fare  C  Q  S  female  male
##  3         22.0      1      0     7.2500  0  0  1       0     1

y_pred = nb_clf.predict([[3,33,1,0,8,0,0,1,0,1]])
print(y_pred)