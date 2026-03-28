user_input = input("enter your name:")

#string
print("string value", user_input)
print(type(user_input))

#integer
int_value = len(user_input)
print("integer value", int_value)
print(type(int_value))

#float
float_value = float(int_value)
print("float value", float_value)
print(type(float_value))

#complex
complex_value = complex(int_value)
print("complex value", complex_value)
print(type(complex_value))

#range
range_value = range(int_value)
print("range value", range_value)
print(type(range_value))

#boolean
boolean_value = bool(user_input)
print("complex value", boolean_value)
print(type(boolean_value))

