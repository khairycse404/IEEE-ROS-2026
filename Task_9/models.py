import math

class Package:
    def __init__(self, package_id, weight, destination):
        self.package_id = package_id
        self.weight = weight
        self.destination = destination

    def to_dict(self):
        return {
            "package_id": self.package_id,
            "weight": self.weight,
            "destination": list(self.destination),
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["package_id"], d["weight"], tuple(d["destination"]))


class Drone:
    BASE = (0, 0)

    def __init__(self, id, battery, position, capacity):
        self.id = id
        self.battery = battery
        self.position = position
        self.capacity = capacity

    def move(self, new_position):
        dx = new_position[0] - self.position[0]
        dy = new_position[1] - self.position[1]
        distance = math.sqrt(dx**2 + dy**2)

        self.consume_battery(distance * 0.1)
        self.position = new_position

    def consume_battery(self, amount):
        self.battery = max(0.0, self.battery - amount)

    def return_to_base(self):
        self.move(self.BASE)

    def is_low_battery(self):
        return self.battery < 20.0

    def to_dict(self):
        return {
            "id": self.id,
            "battery": self.battery,
            "position": list(self.position),
            "capacity": self.capacity,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["id"], d["battery"], tuple(d["position"]), d["capacity"])

    def __repr__(self):
        return f"Drone(id={self.id}, battery={self.battery:.1f}%, pos={self.position})"