# Day 1
# Write a function called divide_or_square
# that takes an argument (number) and returns the square root if divisible by 5 or remainder if not.
# Written by ArvinJay Jumalon

def divide_or_square(number):
    return number ** 0.5 if (number % 5 == 0) == True else number % 5

print(divide_or_square(10))
print(divide_or_square(11))
print(divide_or_square(26))
print(divide_or_square(50))
print(divide_or_square(15))