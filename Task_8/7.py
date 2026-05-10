# Tram
n = int(input())

current = 0
max_capacity = 0

for i in range(n):
    a, b = map(int, input().split())

    current = current - a  
    current = current + b   
    if current > max_capacity:
        max_capacity = current

print(max_capacity)