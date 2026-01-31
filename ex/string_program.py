print("testing function:")

# isalnum
date = "23jan2020" 
pincode = "382350a"
password = "Hars2322"

print("is alnum1:", date.isalnum())
print("is alnum2:", pincode.isalnum())
print("is alnum3:", password.isalnum())


#isdigit
price = "20000"
enter_age = "21"
Atm_pin = "2546"
credit_card_num = "594269327210125"

print("is digit1:", price.isdigit())
print("is digit2:", enter_age.isdigit())
print("is digit3:", Atm_pin.isdigit()) 
print("is digit4:", credit_card_num.isdigit()) 

#isalpha
name = "python" 
month = "march"
enter_city = "ahmedabad"

print("is alpha1:", name.isalpha())
print("is alpha2:", month.isalpha())
print("is alpha3:", enter_city.isalpha())

#islower
username = "harshil"
city = "Ahmedabad"
note = "python3rocks"

print("is lower1:", username.islower())
print("is lower2:", city.islower())
print("is lower3:", note.islower())

#isupper
enter_place = "SABARMATI"
name = "SORATHIYA" 

print("is upper1:", enter_place.isupper())
print("is upper2:", name.isupper())

#isspace
x = " "
comment = "   Great job!   "

print("is space1:", x.isspace())
print("is space5:", comment.isspace())


print("manipulation function:")

#capitalize
text = "welcome to python"
username = "harshil"
city = "aHmedabad" 
vehical_type = "bike"

print("capitalize1:", text.capitalize())
print("capitalize2:", username.capitalize()) 
print("capitalize3:", city.capitalize()) 
print("capitalize4:", vehical_type.capitalize()) 


#lower 
email = "SorathiyaHarshil9@gmail.com"
print("lower1:", email.lower())

#upper
coupon = "gqtc3rf"
country = "india"
product_code = "laptop5632"

 
print("upper1:", coupon.upper())
print("upper2:", country.upper())
print("upper3:", product_code.upper())

#title
main = "Introduction To Pyhton"
book = "ikagi"
city = "new nikol"

print("title1:", main.title())
print("title2:", book.title())
print("title3:", city.title())


#replace

place = "I like cars"
print("replace:", place.replace("cars", "bikes"))

message = "I eat vegitables"
new_message = message.replace("vegitables", "fruits")
print("replace1:", new_message)  

#rstrip
text = "Hello python   "
filename = "report...."
num_str = "1234000"
print("rstrip1:",text.rstrip())
print("rstrip2:", filename.rstrip("."))
print("rstrip3:", num_str.rstrip("0"))   



#strip
num = "   Hello World   "
text = "***Welcome***"
password = "  mypassword123  "


print("strip1:",num.strip())
print("strip2:", text.strip("*")) 
print("strip3:", password.strip()) 





print("searching  function:")

#endswith
filename = "document.pdf"
print("endswith:", filename.endswith(".pdf"))

#startwith
filename = "data2026"
print("startwith:", filename.startswith("data"))

#find
document = "Dear Alice, your order has been shipped."
print("find:", document.find("order"))

#count
text = "Hello World, Hello Python"
print("count:", text.count("Hello"))

print("formating  function:")

#format
name = "harshil"
age = 21
text = "My name is {} and my age is {}".format(name, age)
print(text)

#ljust
text = "python"
print("ljust:", text.ljust(10))

#rjust
text = "python"
print("rjust:", text.rjust(10))

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


























