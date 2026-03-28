class animal:
    def sound(self):
        return "diffrent sound"
class dog(animal):
    def sound(self):
        return "bark"
class cat(animal):
    def sound(self):
        return "meow"

animals = [dog(), cat(), animal()]
for animal in animals:
    print(animal.sound())
