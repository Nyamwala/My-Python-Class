import math
hours = float(input("Enter the number of hours worked: "))
print("Hours worked:", hours)
print(type(hours))
hours_worked = int(hours)

rate = input("Enter the hourly rate: ")
print("Hourly rate:", rate)
hourly_rate =int(rate)
gross_pay = hours_worked * hourly_rate
print("Gross pay:", gross_pay)