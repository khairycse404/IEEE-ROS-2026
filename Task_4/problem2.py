import json
def save_inventory(data):
    with open(file = "inventory.json", mode = "w") as file:
        json.dump(data, file)

def load_inventory():
    try:
        with open(file = "inventory.json", mode = "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

inventory = {
    "Apple": 10,
    "Banana": 5,
    "Milk": 2
}

save_inventory(inventory)
print(load_inventory())