class Student:
    surname = "harshil" 

    def __init__(self, name, age):
        self.name = name  
        self.age = age
        
        
student1 = Student("sorathiya", 21)

print(student1.name) 
print(student1.surname)
print(student1.age)