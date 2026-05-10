Number_Of_Lines = int(input())
for line in range(Number_Of_Lines):
    strOfInts = input()
    array = strOfInts.split(" ")
    intArr = [int(x) for x in array]

    biggestInt = 0
    sum = 0
    for number in intArr:
        sum += number
        if biggestInt < number:
            biggestInt = number

    sum -= biggestInt
    if sum == biggestInt:
        print("Output: YES")
    else:
        print("Output: NO")
