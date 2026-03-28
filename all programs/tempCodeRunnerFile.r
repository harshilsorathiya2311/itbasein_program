def manipulation_func():
    text = input("enter a string:")

    print("start with h:", text.startswith("h"))
    print("ends with a:", text.endswith("a"))

    print("First of 'l':", text.find("a"))
    print("last of 'l':", text.rfind("a"))

    print("count of 'l' in text:", text.count("h"))
    
manipulation_func()


# def search_func():
#     text = input("enter a string:")

#     print("start with h:", text.startswith("h"))
#     print("ends with a:", text.endswith("a"))

#     print("First of 'l':", text.find("a"))
#     print("last of 'l':", text.rfind("a"))

#     print("count of 'l' in text:", text.count("h"))
    
# search_func()
