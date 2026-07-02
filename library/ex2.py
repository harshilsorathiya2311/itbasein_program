import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

#1.generate sample data
np.random.seed(42)

#generate random x values
X = np.random.rand(100,1) * 10

#generate y values with some noise
y = 3 * X.squeeze() + 5 + np.random.randn(100) * 2

#2.split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#3.train the model
model = LinearRegression()
model.fit(X_train, y_train)

#4.make predictions
y_pred = model.predict(X_test)

#5. evalute the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("model performance:")
print("-----------------")
print("slope:", model.coef_[0])
print("intercept:", model.intercept_)
