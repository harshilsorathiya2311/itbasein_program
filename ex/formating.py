print("formating  function:")

#format
name = "harshil"
age = 21
text = "My name is {} and my age is {}".format(name, age)
print("format1:", text)

price = 50000
product = "Laptop"
info = "The price of {} is {}".format(product, price)
print("format2:", info)




#ljust
text = "python"
city = "Mumbai"


print("ljust1:", text.ljust(10))
print("ljust2:", city.ljust(15)) 


#rjust
text = "python"
employee_id = "23"
print("rjust1:", text.rjust(10))
print("rjust2:", employee_id.rjust(5)) 



#center
text = "python"
print("center:", text.center(11))

#encode
message = "Hello Server!"
print("encode:", message.encode())

#casefold
email = "HarshilSorathiya(7@gmail.com)"
print("casefold:", email.casefold())

#index
address = "sardar mall nikol ahmedabad"
print("index:", address.index("nikol"))

#isdecimal
price = "499"
print("isdecimal", price.isdecimal())

#identifier
username = "harshil"
print("isidentifier", username.isidentifier())

#isnumeric
mobile_num = "9409472381"
print("isnumeric", mobile_num.isnumeric())

#istitle
name = "harsHil"
print("istitle:", name.title())

#join
first = "harshil"
last = "sorathiya"
full_name = " ".join([first.title(), last.title()])
print("join:", full_name)

