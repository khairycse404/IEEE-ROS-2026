t = int(input())

for i in range(t):
    n = int(input())
    arr = list(map(int, input().split()))

    if arr[0] == arr[1]:
        repeated = arr[0]
    else:
        repeated = arr[2]

    for i in range(n):
        if arr[i] != repeated:
            print(i + 1)
            break