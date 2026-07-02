# Practice Program using NumPy, Matplotlib, and Scikit-learn

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# -----------------------------
# Step 1: Generate Sample Data
# -----------------------------
np.random.seed(42)

# Generate random X values
X = np.random.rand(100, 1) * 10

# Generate Y values with some noise
y = 3 * X.squeeze() + 5 + np.random.randn(100) * 2

# -----------------------------
# Step 2: Split the Dataset
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# Step 3: Train the Model
# -----------------------------
model = LinearRegression()
model.fit(X_train, y_train)

# -----------------------------
# Step 4: Make Predictions
# -----------------------------
y_pred = model.predict(X_test)

# -----------------------------
# Step 5: Evaluate the Model
# -----------------------------
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Model Performance")
print("-----------------")
print("Slope:", model.coef_[0])
print("Intercept:", model.intercept_)
print("Mean Squared Error:", mse)
print("R² Score:", r2)

# -----------------------------
# Step 6: Plot the Results
# -----------------------------
plt.figure(figsize=(8, 5))

# Scatter plot of test data
plt.scatter(X_test, y_test, color='blue', label='Actual Data')

# Regression line
plt.plot(X_test, y_pred, color='red', linewidth=2, label='Regression Line')

plt.title("Linear Regression Example")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.grid(True)

plt.show()