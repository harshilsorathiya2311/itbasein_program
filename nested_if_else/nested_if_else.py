# Password
user_admin = True    
password_correct = False  

if user_admin:
    if password_correct:
        print("Login successful")
    else:
        print("Wrong password")
else:
    print("Invalid user")

# Bank
has_uniform = True
has_bag = True

if has_uniform:
    if has_bag:
        print("You can go to school")
    else:
        print("Get your bag first")
else:
    print("Wear your uniform first")

# Pass
passed_10th = True
science_stream = True

if passed_10th:
    if science_stream:
        print("You can join Science stream.")
    else:
        print("You can join Commerce stream.")
else:
    print("You cannot continue studies.")

# Ticket
age_20 = False  
ticket_purchased = True

if age_20:
    if ticket_purchased:
        print("You have purchased the ticket.")
    else:
        print("You have not purchased the ticket.")
else:
    print("You get a half ticket.")

# College
high_cgpa = True 
admit_only = True

if high_cgpa:
    if admit_only:
        print("Admitted with scholarship.")
    else:
        print("Need to pay all fees.")
else:
    print("Not admitted.")

# Lift
lift_full = True   
lift_capacity_ok = True  

if lift_capacity_ok:
    if lift_full:
        print("Lift is overloaded! Cannot move.")
    else:
        print("Lift can stop safely.")
else:
    print("Reduce the number of people in the lift.")

# Grade
grade_A = True
grade_B = False

if grade_A:
    print("Grade: A")
else:
    if grade_B:
        print("Grade: B")
    else:
        print("Grade: F")

# Traffic
light_red = True
light_yellow = False

if light_red:
    print("Stop!")
else:
    if light_yellow:
        print("Get ready to move.")
    else:
        print("Go!")

# Heavy Vehicle
has_heavy_license = True
driving_heavy = True

if has_heavy_license:
    if driving_heavy:
        print("You can drive a heavy vehicle.")
    else:
        print("You can drive a light vehicle.")
else:
    print("You cannot drive a heavy vehicle.")

# Internet Speed
fast = False
medium = True

if fast:
    print("fast download")
else:
    if medium:
        print("Internet is medium. Downloads are smooth.")
    else:
        print("Downloads may take time.")

# Laptop
have_laptop = True
can_code = False

if have_laptop:
    if can_code:
        print("you can code perfectly!")
    else:
        print("purchase a laptop")
else:
    print("use another option")

# Recharge
phone_recharged = True
can_watch_video = True

if phone_recharged:
    if can_watch_video:
        print("watch video")
    else:
        print("wannot watch video")
else:
    print("recharge your phone")

# Bike
have_bike = True
can_visit = True

if have_bike:
    if can_visit:
        print("You can visit the place")
    else:
        print("Not visiting")
else:
    print("Choose other option")

# Plug
plug_available = True
phone_plugged = False

if plug_available:
    if phone_plugged:
        print("Your phone is charging.")
    else:
        print("Your phone is not charging.")
else:
    print("Find a plug to charge phone")

# Camera
camera_installed = True
secured = False

if camera_installed:
    if secured:
        print("You are secure.")
    else:
        print("You are not secure.")
else:
    print("Install a camera to secure.")
