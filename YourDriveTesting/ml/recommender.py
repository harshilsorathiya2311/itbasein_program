import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Sample dataset (replace with DB later)
data = pd.DataFrame({
    "price": [5, 10, 15, 20, 25, 30],
    "type_score": [1, 2, 3, 4, 5, 6],
    "car": ["A", "B", "C", "D", "E", "F"]
})

X = data[["price", "type_score"]]
y = data["car"]

model = RandomForestClassifier()
model.fit(X, y)

def recommend(price, type_score):
    return model.predict([[price, type_score]])[0]