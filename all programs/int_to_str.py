user_input = input("Enter your name: ")

# String
print("String value:", user_input)
print(type(user_input))

# Integer (using length of string)
int_value = len(user_input)
print("Integer value:", int_value)
print(type(int_value))

# Float
float_value = float(int_value)
print("Float value:", float_value)
print(type(float_value))

# Complex
complex_value = complex(int_value)
print("Complex value:", complex_value)
print(type(complex_value))

# Boolean
bool_value = bool(user_input)
print("Boolean value:", bool_value)
print(type(bool_value))

# Range
range_value = range(int_value)
print("Range value:", range_value)
print(type(range_value))
