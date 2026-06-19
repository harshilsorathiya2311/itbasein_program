from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

X = np.array([[0],[1],[2],[3],[4]])
y = np.array([0,2,4,6,8])

model = Sequential([
    Dense(1, input_shape=(1,))
])

model.compile(
    optimizer='adam',
    loss='mse'
)

model.fit(X, y, epochs=10)

print(model.predict(np.array([[5]])))