print("===== MEDICAL CLINIC=====")
name = input("enter your name:")
age = input("enter your age:")

print("\n available DOCTORS:")
print("1. DR. John Mwangi - general medicine")
print("2. DR. Mary  Wanjiku - pediatrics")
print("3. DR.  David Otieno - dermatology")

doctor = input ("choose a doctor(1,2 or 3):")
day = input ("enter appointment day:")
if  doctor =="1":
    doctor_name = "DR. John Mwangi"
elif doctor == " 2":
  doctor_name =   "DR. Mary  Wanjiku"
elif doctor == " 3":
  doctor_name =   "DR. David Otieno"
else:
  doctor_name =   "Invalid doctor"

  print("\n ==== APPOINTMENT DETAILS ====")
  print("Patient:", name)
  print("age:" ,age)
  print("doctors:" ,doctor_name)
  print("day: " ,day)


  if doctor_name !="Invalid doctor":
     print("Appointment booked successfully!")
  else:
     print("please choose a valid  doctor.")