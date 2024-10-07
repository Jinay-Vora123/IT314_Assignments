from trip_management import Trip
import random

class Passenger:
    def __init__(self, name: str, pickup_location: str, destination: str):
        self.name = name
        self.pickup_location = pickup_location
        self.destination = destination

    def request_taxi(self):
        print(f"{self.name} is requesting a taxi from {self.pickup_location} to {self.destination}")
        return Trip(random.randint(1000, 9999), self, self.pickup_location, self.destination)
