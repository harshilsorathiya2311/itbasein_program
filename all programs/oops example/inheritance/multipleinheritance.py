class father:
    def skills(self):
        print("father has business skills")
        
class mother:
    def cook(self):
        print("mother has making best cooking")
        
class child(father,mother):
    def hobbies(self):
        print("child likes cricket")
        
family = child()

family.skills()
family.cook()
family.hobbies()