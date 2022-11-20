import sklearn
import matplotlib.pyplot as plt
import numpy as np
import random
from sklearn import model_selection
from sklearn import linear_model

#y  = mx + c
#F = 1.8*C +32


x = list(range(0, 100)) #C
#y = [1.8*F + 32 for F in x] #F
y = [1.8*F + 32 +random.randint(-3,3) for F in x] #F

print(f'X: {x}')
print(F'Y: {y}')

plt.plot(x,y,'-*r')


x = np.array(x).reshape(-1,1)
y = np.array(y).reshape(-1,1)

xTrain, xTest, yTrain, yTest = model_selection.train_test_split(x,y,test_size=0.2)

model = linear_model.LinearRegression()
model.fit(xTrain, yTrain)
print(f'Coefficients: {model.coef_}')
print(f'Intercept: {model.intercept_}')

accuracy = model.score(xTest,yTest)
print(f'Accuracy: {round(accuracy*100,2)}')

x = x.reshape(1,-1)[0]
m = model.coef_[0][0]
c = model.intercept_[0]
y = [m*F + c for F in x]
plt.plot(x,y,'-*b')
plt.show()