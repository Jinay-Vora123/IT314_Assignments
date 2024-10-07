import random
import datetime
import logging

# Assuming Logger is defined elsewhere in logging_module
# import from logging_module import Logger

class FeedbackManager:
    @staticmethod
    def collect_feedback(taxi):
        # Simulate feedback collection
        feedback = random.randint(1, 5)
        print(f"Passenger gave a feedback of {feedback} to Taxi {taxi.taxi_id}")
        taxi.receive_feedback(feedback)

class UserProfile:
    def __init__(self, user: User):
        self.user = user
        self.rating = None
        self.feedback_history = []

    def add_feedback(self, feedback: int):
        self.feedback_history.append(feedback)
        if self.rating is None:
            self.rating = feedback
        else:
            self.rating = (self.rating + feedback) / 2  # Average rating
        Logger.log_info(f"{self.user.name}'s new average rating is: {self.rating}")

    def get_feedback_history(self):
        return self.feedback_history

class TripHistory:
    def __init__(self):
        self.completed_trips = []

    def add_trip(self, trip: Trip):
        self.completed_trips.append(trip)
        Logger.log_info(f"Trip from {trip.passenger.pickup_location} to {trip.passenger.destination} added to history.")

    def display_history(self):
        for trip in self.completed_trips:
            Logger.log_info(f"Trip: {trip.passenger.name} - Fare: {trip.fare}, Status: {trip.status}")

class EnhancedDriver(Driver):
    def __init__(self, name: str, driver_id: int):
        super().__init__(name, driver_id)
        self.profile = UserProfile(self)
        self.trip_history = TripHistory()

    def complete_trip(self, trip: Trip):
        super().complete_trip(trip)
        self.trip_history.add_trip(trip)

    def receive_feedback(self, feedback: int):
        self.profile.add_feedback(feedback)

class EnhancedPassenger(Passenger):
    def __init__(self, name: str, pickup_location: str, destination: str):
        super().__init__(name, pickup_location, destination)
        self.profile = UserProfile(self)
        self.trip_history = TripHistory()

    def complete_trip(self, trip: Trip):
        super().complete_trip(trip)
        self.trip_history.add_trip(trip)

    def receive_feedback(self, feedback: int):
        self.profile.add_feedback(feedback)

class NotificationService:
    @staticmethod
    def send_notification(user: User, message: str):
        Logger.log_info(f"Sending notification to {user.name}: {message}")

class Trip:
    def __init__(self, passenger: EnhancedPassenger, driver: EnhancedDriver):
        self.passenger = passenger
        self.driver = driver
        self.status = 'pending'
        self.distance = 0.0  # Distance in kilometers
        self.fare = 0.0
        self.start_time = None
        self.end_time = None

    def start_trip(self):
        Logger.log_info(f"Trip started from {self.passenger.pickup_location} to {self.passenger.destination}.")
        self.start_time = datetime.datetime.now()
        self.status = 'in_progress'
        self.distance = self.calculate_distance()

    def complete_trip(self):
        self.end_time = datetime.datetime.now()
        Logger.log_info(f"Trip completed for {self.passenger.name}. Duration: {self.end_time - self.start_time}")
        self.status = 'completed'
        self.fare = self.calculate_fare()
        Logger.log_info(f"Total fare for the trip: {self.fare}")

        # Collect feedback after the trip
        FeedbackManager.collect_feedback(self.driver)

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

    def add_driver(self, driver: EnhancedDriver):
        self.drivers.append(driver)
        self.available_taxis.append(driver)  # Initially, all drivers are available
        Logger.log_info(f"Driver {driver.name} added to the dispatcher.")

    def dispatch_taxi(self, passenger: EnhancedPassenger):
        Logger.log_info(f"Dispatching taxi for {passenger.name}.")
        available_driver = self.find_available_driver()
        if available_driver:
            trip = Trip(passenger, available_driver)
            available_driver.current_trip = trip
            trip.start_trip()
            passenger.current_trip = trip
            self.available_taxis.remove(available_driver)
            NotificationService.send_notification(passenger, "Taxi has been dispatched to your location.")
        else:
            Logger.log_error("No taxis available.")
            raise TaxiNotAvailableException()

    def find_available_driver(self):
        for driver in self.drivers:
            if driver.current_trip is None:
                return driver
        return None

    def complete_trip(self, taxi: EnhancedDriver):
        if taxi.current_trip:
            taxi.complete_trip(taxi.current_trip)
            taxi.current_trip = None
            self.available_taxis.append(taxi)
        else:
            Logger.log_warning(f"Taxi {taxi.name} has no current trip to complete.")

class MainApp:
    def __init__(self):
        self.dispatcher = Dispatcher()

    def run(self):
        Logger.log_info("Starting Taxi App...")

        # Create and add drivers
        self.dispatcher.add_driver(EnhancedDriver("Alice", 1))
        self.dispatcher.add_driver(EnhancedDriver("Bob", 2))
        self.dispatcher.add_driver(EnhancedDriver("Charlie", 3))

        # Create and add passengers
        passengers = [
            EnhancedPassenger("Eve", "North", "East"),
            EnhancedPassenger("Frank", "South", "West"),
            EnhancedPassenger("Grace", "East", "South"),
            EnhancedPassenger("Hank", "West", "North"),
        ]

        # Validate locations and request taxis
        for passenger in passengers:
            try:
                LocationService.validate_location(passenger.pickup_location)
                LocationService.validate_location(passenger.destination)
                passenger.request_taxi(self.dispatcher)
            except InvalidLocationException as e:
                Logger.log_error(e.message)

        # Complete trips
        for driver in self.dispatcher.drivers:
            self.dispatcher.complete_trip(driver)

        # Process payments for completed trips
        for passenger in passengers:
            if passenger.current_trip and passenger.current_trip.status == 'completed':
                try:
                    PaymentService.process_payment(passenger.current_trip.fare)
                except ValueError as e:
                    Logger.log_error(e)

        # Display trip histories
        for passenger in passengers:
            Logger.log_info(f"{passenger.name}'s Trip History:")
            passenger.trip_history.display_history()

        for driver in self.dispatcher.drivers:
            Logger.log_info(f"{driver.name}'s Trip History:")
            driver.trip_history.display_history()

if __name__ == "__main__":
    app = MainApp()
    app.run()
