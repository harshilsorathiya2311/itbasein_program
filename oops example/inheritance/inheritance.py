class animal:  
    def eat(self):
        print("animal eat food")
        

class dog(animal):
    def bark(self):
        print("dog barks")       
        
animals = dog()

animals.eat()
animals.bark()