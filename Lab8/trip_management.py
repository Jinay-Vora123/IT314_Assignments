from pricing import PricingEngine

class Trip:
    def __init__(self, trip_id: int, passenger, pickup_location: str, destination: str):
        self.trip_id = trip_id
        self.passenger = passenger
        self.pickup_location = pickup_location
        self.destination = destination
        self.taxi = None
        self.price = PricingEngine.calculate_fare(self.pickup_location, self.destination)
        self.status = "Pending"
        self.distance = self.calculate_distance()

    def assign_taxi(self, taxi):
        self.taxi = taxi
        self.status = "In Progress"

    def mark_completed(self):
        self.status = "Completed"

    def mark_failed(self):
        self.status = "Failed"
        print(f"Trip {self.trip_id} failed to find a taxi.")

    def calculate_distance(self):
        # Simulating distance calculation
        distances = {
            ('North', 'South'): 12.0,
            ('East', 'West'): 15.5,
            ('South', 'North'): 10.0,
            ('West', 'East'): 18.2,
        }
        return distances.get((self.pickup_location, self.destination), random.uniform(5.0, 20.0))

class TripManager:
    def __init__(self):
        self.trips = []
        self.failed_trips = []

    def start_trip(self, trip, dispatcher):
        taxi = dispatcher.dispatch_taxi(trip)
        if taxi:
            self.trips.append(trip)
        else:
            self.failed_trips.append(trip)
