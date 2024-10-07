import logging
from logging_module import Logger
import random

# Exception Definitions
class TaxiAppException(Exception):
    pass

class TaxiNotAvailableException(TaxiAppException):
    def __init__(self, message="Taxi not available at the moment"):
        self.message = message
        super().__init__(self.message)

class TripFailedException(TaxiAppException):
    def __init__(self, message="Trip failed due to lack of availability"):
        self.message = message
        super().__init__(self.message)

class InvalidLocationException(TaxiAppException):
    def __init__(self, location):
        self.message = f"Invalid location provided: {location}"
        super().__init__(self.message)

class User:
    def __init__(self, name: str, user_type: str):
        self.name = name
        self.user_type = user_type  # Either 'passenger' or 'driver'

    def __str__(self):
        return f"{self.user_type.capitalize()}: {self.name}"

class Driver(User):
    def __init__(self, name: str, driver_id: int):
        super().__init__(name, 'driver')
        self.driver_id = driver_id
        self.current_trip = None
        self.location = None

    def update_location(self, location: str):
        Logger.log_info(f"{self.name} has updated location to {location}.")
        self.location = location

class Passenger(User):
    def __init__(self, name: str, pickup_location: str, destination: str):
        super().__init__(name, 'passenger')
        self.pickup_location = pickup_location
        self.destination = destination
        self.current_trip = None

    def request_taxi(self, dispatcher):
        Logger.log_info(f"{self.name} is requesting a taxi from {self.pickup_location} to {self.destination}.")
        dispatcher.dispatch_taxi(self)

class Trip:
    def __init__(self, passenger: Passenger, driver: Driver):
        self.passenger = passenger
        self.driver = driver
        self.status = 'pending'
        self.distance = 0.0  # Distance in kilometers
        self.fare = 0.0

    def start_trip(self):
        Logger.log_info(f"Trip started from {self.passenger.pickup_location} to {self.passenger.destination}.")
        self.status = 'in_progress'
        self.distance = self.calculate_distance()

    def complete_trip(self):
        Logger.log_info(f"Trip completed for {self.passenger.name}.")
        self.status = 'completed'
        self.fare = self.calculate_fare()
        Logger.log_info(f"Total fare for the trip: {self.fare}")

    def calculate_distance(self):
        # Simulate distance calculation
        distance = random.uniform(1, 20)  # Random distance between 1 km and 20 km
        Logger.log_info(f"Calculated distance for trip: {distance} km")
        return distance

    def calculate_fare(self):
        # Simple fare calculation: $1 per km
        fare = self.distance * 1.0
        return fare

class Dispatcher:
    def __init__(self):
        self.available_taxis = []
        self.passenger_requests = []
        self.drivers = []

    def add_driver(self, driver: Driver):
        self.drivers.append(driver)
        Logger.log_info(f"Driver {driver.name} added to the dispatcher.")

    def dispatch_taxi(self, passenger: Passenger):
        Logger.log_info(f"Dispatching taxi for {passenger.name}.")
        available_driver = self.find_available_driver()
        if available_driver:
            trip = Trip(passenger, available_driver)
            available_driver.current_trip = trip
            trip.start_trip()
            passenger.current_trip = trip
            self.available_taxis.remove(available_driver)
        else:
            Logger.log_error("No taxis available.")
            raise TaxiNotAvailableException()

    def find_available_driver(self):
        for driver in self.drivers:
            if driver.current_trip is None:
                return driver
        return None

    def complete_trip(self, taxi: Driver):
        if taxi.current_trip:
            taxi.current_trip.complete_trip()
            taxi.current_trip = None
            self.available_taxis.append(taxi)
        else:
            Logger.log_warning(f"Taxi {taxi.name} has no current trip to complete.")

class LocationService:
    @staticmethod
    def validate_location(location: str):
        # Simulated location validation
        valid_locations = ["North", "South", "East", "West", "Central"]
        if location not in valid_locations:
            Logger.log_error(f"Invalid location: {location}")
            raise InvalidLocationException(location)
        Logger.log_info(f"Location {location} is valid.")

class PaymentService:
    @staticmethod
    def process_payment(fare: float):
        Logger.log_info(f"Processing payment for amount: ${fare}")
        if fare < 0:
            Logger.log_error("Payment amount cannot be negative.")
            raise ValueError("Invalid payment amount")
        # Simulate payment processing
        Logger.log_info("Payment processed successfully.")

def main():
    Logger.log_info("Starting Taxi App...")

    # Create dispatcher and add drivers
    dispatcher = Dispatcher()
    dispatcher.add_driver(Driver("Alice", 1))
    dispatcher.add_driver(Driver("Bob", 2))
    dispatcher.add_driver(Driver("Charlie", 3))

    # Create passengers
    passengers = [
        Passenger("Eve", "North", "East"),
        Passenger("Frank", "South", "West"),
        Passenger("Grace", "East", "South"),
        Passenger("Hank", "West", "North"),
    ]

    # Validate locations
    for passenger in passengers:
        try:
            LocationService.validate_location(passenger.pickup_location)
            LocationService.validate_location(passenger.destination)
            passenger.request_taxi(dispatcher)
        except InvalidLocationException as e:
            Logger.log_error(e.message)

    # Complete trips
    for driver in dispatcher.drivers:
        dispatcher.complete_trip(driver)

    # Process payments for completed trips
    for passenger in passengers:
        if passenger.current_trip and passenger.current_trip.status == 'completed':
            try:
                PaymentService.process_payment(passenger.current_trip.fare)
            except ValueError as e:
                Logger.log_error(e)

if __name__ == "__main__":
    main()
