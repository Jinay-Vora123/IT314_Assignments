import random
import time
from trip_management import TripManager
from pricing import PricingEngine
from feedback import FeedbackManager
from passengers import Passenger

class Taxi:
    def __init__(self, taxi_id: int, location: str, available: bool = True, driver_name: str = "Unknown"):
        self.taxi_id = taxi_id
        self.location = location
        self.available = available
        self.driver_name = driver_name
        self.current_trip = None
        self.total_earnings = 0.0
        self.rating = 0.0
        self.feedback_received = 0

    def assign_trip(self, trip):
        if self.available:
            print(f"Taxi {self.taxi_id} assigned to trip {trip.trip_id}")
            self.available = False
            self.current_trip = trip
            trip.assign_taxi(self)
        else:
            print(f"Taxi {self.taxi_id} is not available!")

    def complete_trip(self):
        print(f"Taxi {self.taxi_id} completed the trip for {self.current_trip.passenger.name}")
        self.total_earnings += self.current_trip.price
        FeedbackManager.collect_feedback(self)
        self.available = True
        self.current_trip = None

    def update_location(self, new_location: str):
        print(f"Taxi {self.taxi_id} is moving from {self.location} to {new_location}")
        self.location = new_location

    def receive_feedback(self, feedback: int):
        self.feedback_received += 1
        self.rating = (self.rating * (self.feedback_received - 1) + feedback) / self.feedback_received
        print(f"Taxi {self.taxi_id} now has an average rating of {self.rating:.2f} after {self.feedback_received} feedbacks")

class Dispatcher:
    def __init__(self):
        self.taxis = [Taxi(i, random.choice(['North', 'South', 'East', 'West']), True, f"Driver {i}") for i in range(1, 51)]
        self.trip_manager = TripManager()
        self.pricing_engine = PricingEngine()

    def find_nearest_taxi(self, location: str):
        available_taxis = [taxi for taxi in self.taxis if taxi.available and taxi.location == location]
        if available_taxis:
            return random.choice(available_taxis)
        else:
            print(f"No available taxis in {location}")
            return None

    def dispatch_taxi(self, trip):
        taxi = self.find_nearest_taxi(trip.passenger.pickup_location)
        if taxi:
            taxi.assign_trip(trip)
        else:
            print(f"No taxis available for trip {trip.trip_id}")
            trip.mark_failed()
        return taxi

    def complete_trip(self, taxi: Taxi):
        taxi.complete_trip()

def main():
    dispatcher = Dispatcher()
    passengers = [
        Passenger("Alice", "North", "South"),
        Passenger("Bob", "East", "West"),
        Passenger("Charlie", "South", "North"),
        Passenger("Diana", "West", "East")
    ]

    # Passengers request taxis
    for passenger in passengers:
        trip = passenger.request_taxi()
        dispatcher.trip_manager.start_trip(trip, dispatcher)
    
    # Simulate trips being completed
    for taxi in dispatcher.taxis:
        if taxi.current_trip:
            time.sleep(1)
            dispatcher.complete_trip(taxi)

if __name__ == "__main__":
    main()
