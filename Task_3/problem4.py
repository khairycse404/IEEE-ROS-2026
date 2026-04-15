import random

def get_unique_lottery():
    nums = set()
    while len(nums) < 6:
        nums.add(random.randint(1, 50))
    return nums

print(get_unique_lottery())