# Simple Calculator
print("Basic calculator")

num1 = float(input("Enter first number: "))
opr = input("Enter operator (+, -, *, /): ")
num2 = float(input("Enter second number: "))

if opr == "+":
    print(num1 + num2)

elif opr == "-":
    print(num1 - num2)

elif opr == "*":
    print(num1 * num2)

elif opr == "/":
    print(num1 / num2)

if num2 == 0:
    print("Error: Division by zero is not allowed.")
