class animal:
    def speak(self):
        print("animal speak")
        
class eat(animal):
    def eat_animal(self):
        print("eat food")
        
class bird (animal):
    def bird_name(self):
        print("parrot")
        
class allanimal(eat, bird):
    pass

animals = allanimal()

animals.speak()
animals.eat_animal()
animals.bird_name()


