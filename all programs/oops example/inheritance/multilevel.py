class grandparent:
    def time1(self):
        print("birth year 1950")

class Parent(grandparent):
    def time2(self):
        print("birth year 1981")

class Child(Parent):
    def time3(self):
        print("birth year 2005")

obj = Child()
obj.time1()
obj.time2()
obj.time3()