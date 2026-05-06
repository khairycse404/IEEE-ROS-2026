import json
from models import Drone, Package


class Fleet:
    def __init__(self):
        self.drones = []
        self.packages = []

    def add_drone(self, drone):
        self.drones.append(drone)

    def add_package(self, package):
        self.packages.append(package)

    def save_to_json(self, path="fleet.json"):
        data = {
            "drones": [d.to_dict() for d in self.drones],
            "packages": [p.to_dict() for p in self.packages],
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def load_from_json(self, path="fleet.json"):
        with open(path, "r") as f:
            data = json.load(f)

        self.drones = [Drone.from_dict(d) for d in data["drones"]]
        self.packages = [Package.from_dict(p) for p in data["packages"]]

    def best_performance(self):
        if not self.drones:
            return None
        return max(self.drones, key=lambda d: d.battery)