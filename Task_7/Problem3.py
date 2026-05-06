class Passenger:
    def __init__(self, name):
        self.name = name


class Flight:
    def __init__(self):
        self.passengers = []

    def add_passenger(self, passenger_obj):
        self.passengers.append(passenger_obj)


# Test
p1 = Passenger("Ahmed")
p2 = Passenger("Mona")

f = Flight()
f.add_passenger(p1)
f.add_passenger(p2)

print(len(f.passengers))