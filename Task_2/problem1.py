#!/usr/bin/env python3

# numbers = []

# while True:
#     num = int(input("Enter a number (-1 to stop): "))
    
#     if num == -1:
#         break
    
#     numbers.append(num)

# if len(numbers) > 0:
#     print("Largest number: ", max(numbers))
#     print("Smallest number: ", min(numbers))
# else:
#     print("No numbers entered.")

numbers = []

while True:
    num = int(input("Enter a number (-1 to stop): "))
    
    if num == -1:
        break
    
    numbers.append(num)

if len(numbers) > 0:
    largest = numbers[0]
    smallest = numbers[0]

    for i in range(len(numbers)):
        if numbers[i] > largest:
            largest = numbers[i]
        
        if numbers[i] < smallest:
            smallest = numbers[i]

    print("Largest number:", largest)
    print("Smallest number:", smallest)
else:
    print("No numbers entered.")