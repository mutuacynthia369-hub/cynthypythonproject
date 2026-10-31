print("=====STUDENT GRRADDE CALCULATOR=====")
 #input
name = input("ENTER YOUR NAME:")
age = int(input(" ENTER YOUR AGE:"))

mark1 =float(input(" enter mark for Python:"))
mark2 =float(input("enter mark for Database:"))
mark3 = float(input("enter mark for web programming:"))

# variables
total = mark1 + mark2 + mark3
average = total/3

# condition
if average>=70:
 grade="A"
elif average>=60:
  grade="B"
elif average>=50:
   grade="C"
elif average >= 40:
   grade = "D"
else:
  grade ="F"

  #output
  print("\n =====STUDENT RESULTS=====")
  print("Name:", name)
  print("Age", age)
  print("Total", total)
  print("Average", average)
  print("Grade", grade)

if average >= 40:
    print("result:PASS")
    
else:
   print("result:FAILS")