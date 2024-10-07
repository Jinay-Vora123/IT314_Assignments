import logging
from logging_module import Logger
from trip_management import TripManager
from passengers import Passenger
from dispatcher_module import Dispatcher
from error_handling import TaxiNotAvailableException
import random
import time

class AdditionalFeature:
    def __init__(self, feature_name: str):
        self.feature_name = feature_name

    def execute(self):
        Logger.log_info(f"Executing additional feature: {self.feature_name}")
        result = self.feature_name + " executed successfully."
        Logger.log_debug(result)
        return result

class Ride:
    def __init__(self, passenger: Passenger, start_location: str, destination: str, ride_type: str = "regular"):
        self.passenger = passenger
        self.start_location = start_location
        self.destination = destination
        self.ride_type = ride_type
        self.status = 'pending'

    def start_ride(self):
        Logger.log_info(f"Ride started for {self.passenger.name} from {self.start_location} to {self.destination}.")
        self.status = 'in_progress'

    def complete_ride(self):
        Logger.log_info(f"Ride completed for {self.passenger.name}.")
        self.status = 'completed'

class Taxi:
    def __init__(self, taxi_id: int):
        self.taxi_id = taxi_id
        self.current_trip = None

    def assign_trip(self, ride: Ride):
        self.current_trip = ride
        ride.start_ride()

    def complete_trip(self):
        if self.current_trip:
            self.current_trip.complete_ride()
            self.current_trip = None
        else:
            Logger.log_warning(f"Taxi {self.taxi_id} has no current trip to complete.")

class EnhancedDispatcher(Dispatcher):
    def __init__(self):
        super().__init__()
        self.available_taxis = [Taxi(i) for i in range(5)]  # Create 5 taxis for the dispatcher
        self.passenger_requests = []

    def find_available_taxi(self):
        for taxi in self.available_taxis:
            if not taxi.current_trip:
                return taxi
        return None

    def dispatch_taxi(self, passenger: Passenger):
        Logger.log_info(f"Dispatching taxi for {passenger.name}.")
        taxi = self.find_available_taxi()
        if taxi:
            ride = Ride(passenger, passenger.pickup_location, passenger.destination)
            taxi.assign_trip(ride)
            self.trip_manager.start_trip(ride, self)
        else:
            Logger.log_error("No taxis available.")
            self.passenger_requests.append(passenger)

    def handle_passenger_requests(self):
        for passenger in self.passenger_requests:
            self.dispatch_taxi(passenger)

class RideShare(Ride):
    def __init__(self, passenger: Passenger, start_location: str, destination: str, shared_passengers: list):
        super().__init__(passenger, start_location, destination, ride_type="shared")
        self.shared_passengers = shared_passengers

    def start_ride(self):
        Logger.log_info(f"Ride share started for {self.passenger.name} with passengers {', '.join([p.name for p in self.shared_passengers])}.")
        super().start_ride()

class EnhancedPassenger(Passenger):
    def request_ride(self, dispatcher: EnhancedDispatcher):
        dispatcher.dispatch_taxi(self)

    def request_shared_ride(self, dispatcher: EnhancedDispatcher, other_passengers: list):
        Logger.log_info(f"{self.name} is requesting a shared ride with {', '.join([p.name for p in other_passengers])}.")
        ride = RideShare(self, self.pickup_location, self.destination, other_passengers)
        dispatcher.dispatch_taxi(self)

def test_dispatching_system():
    Logger.log_info("Testing dispatching system...")

    dispatcher = EnhancedDispatcher()
    test_passengers = [
        EnhancedPassenger("Eve", "North", "East"),
        EnhancedPassenger("Frank", "South", "West"),
        EnhancedPassenger("Grace", "East", "South"),
        EnhancedPassenger("Hank", "West", "North"),
        EnhancedPassenger("Ivy", "South", "East"),
    ]

    # Requesting rides
    for passenger in test_passengers:
        if random.choice([True, False]):
            passenger.request_ride(dispatcher)
        else:
            # Randomly choose another passenger for shared rides
            other_passengers = random.sample([p for p in test_passengers if p != passenger], 2)
            passenger.request_shared_ride(dispatcher, other_passengers)

    # Complete all trips
    for taxi in dispatcher.available_taxis:
        if taxi.current_trip:
            taxi.complete_trip()

    # Handle any remaining requests
    dispatcher.handle_passenger_requests()

def simulated_workload():
    for i in range(100):
        Logger.log_info(f"Simulating workload iteration: {i}")
        feature = AdditionalFeature(f"Feature {i}")
        feature.execute()
        time.sleep(random.uniform(0.1, 0.5))  # Simulate processing time

def main():
    Logger.log_info("Starting main system...")

    # Testing dispatching system with extra simulated workload
    test_dispatching_system()
    simulated_workload()

if __name__ == "__main__":
    main()
