a = (["harshil", "23", "R.B"], ["Fenil", "24", "R.B"])

students_dict = []

for student in a:
    students_dict.append({
        "name": student[0],
        "age": int(student[1]),  
        "collage": student[2]
    })


name = input("enter name: ")
age = int(input("enter age: "))
collage = input("enter collage name: ")

students_dict.append({
    "name": name,
    "age": age,
    "collage": collage
})

print(students_dict)