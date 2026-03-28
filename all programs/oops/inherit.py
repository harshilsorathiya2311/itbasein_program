class animal:
    def __init__(self,name):
        self.name = name
    def info(self):
        print("animal name :", self.name)

class dog(animal):
    def sound(self):
        print(self.name, "barks")   
        
d = dog("lebra")
d.info()
d.sound()  

#1.Single Inheritance
class Person:
    def __init__(self, name):
        self.name = name

class Employee(Person):  # Employee inherits from Person
    def show_role(self):
        print(self.name, "is an employee")

emp = Employee("harshil")
print("Name:", emp.name)
emp.show_role()  

#2. multiple Inheritance
class Person:
    def __init__(self, name):
        self.name = name

class Job:
    def __init__(self, salary):
        self.salary = salary

class Employee(Person, Job):  # Inherits from both Person and Job
    def __init__(self, name, salary):
        Person.__init__(self, name)
        Job.__init__(self, salary)

    def details(self):
        print(self.name, "earns", self.salary)

emp = Employee("harshil", 50000)
emp.details()

#3. Multilevel Inheritance
class Person:
    def __init__(self, name):
        self.name = name

class Employee(Person):  
    def show_role(self):
        print(self.name, "is an employee")

class Manager(Employee):  # Manager inherits from Employee
    def department(self, dept):
        print(self.name, "manages", dept, "department")

mgr = Manager("harshil")
mgr.show_role()
mgr.department("HR")

#4. Hierarchical Inheritance
class Person:
    def __init__(self, name):
        self.name = name

class Employee(Person):  
    def role(self):
        print(self.name, "works as an employee")

class Intern(Person):  
    def role(self):
        print(self.name, "is an intern")

emp = Employee("fenil ")
emp.role()

intern = Intern("om")
intern.role()