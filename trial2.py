print("=====MEDICAL CLINIC=====")

name = input ("Enter your name:")
age = input("Enter your age:")

print("\n AVAILABLE DOCTORS:")
print("1. Dr. John Mwangi - general medicine")
print("2. Dr. Mary Wanjiku - pediatrics")
print("3. Dr. David Otieno - dermatology")

choice = input ("Choose a DOCTOR:")
if choice =="1":
  doctor ="Dr. John Mwangi"
elif choice =="2":
  doctor = " Dr. Mary Wanjiku"
elif choice =="3":
  doctor ="Dr. David Otieno"
else:
  doctor = " invalid doctor"

day = input(" enter appointment day:")

print("\n =====APPOINTMENT DETAILS=====")
print("Patient:", name)
print("Age:", age)
print("Doctor:" ,doctor)
print("Day:" ,day)

if doctor != " invalid doctor":
  print("Appointment booked successfully")
else:
  print("Please choose a valid doctor.")