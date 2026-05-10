iterations = int(input())

for i in range(iterations):
    n = int(input())
    name1, name2 = input().split()

    if sorted(name1) == sorted(name2):
        print("YES")
    else:
        print("NO")