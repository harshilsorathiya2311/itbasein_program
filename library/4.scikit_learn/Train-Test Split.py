from sklearn.model_selection import train_test_split

x = [1, 2, 3, 4, 5]
y = [10, 20, 30, 40, 50]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

print("x_train:", x_train)
print("x_test:", x_test)