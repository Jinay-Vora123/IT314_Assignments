import random
import time
from trip_management import Trip
from error_handling import TaxiNotAvailableException

class Passenger:
    """Class representing a passenger who requests taxis."""
    
    def __init__(self, name: str, pickup_location: str, destination: str):
        self.name = name
        self.pickup_location = pickup_location
        self.destination = destination
        self.current_trip = None
        self.feedback_given = False

    def request_taxi(self):
        """Request a taxi for the passenger."""
        print(f"{self.name} is requesting a taxi from {self.pickup_location} to {self.destination}")
        trip = Trip(random.randint(1000, 9999), self, self.pickup_location, self.destination)
        self.current_trip = trip
        return trip

    def provide_feedback(self, rating: int, comments: str = ""):
        """Allow the passenger to provide feedback on their trip."""
        if self.current_trip and not self.feedback_given:
            print(f"{self.name} provided feedback: {rating}/5 - {comments}")
            self.current_trip.record_feedback(rating, comments)
            self.feedback_given = True
        else:
            print(f"{self.name} cannot provide feedback at this time.")

class Trip:
    """Class representing a trip."""
    
    def __init__(self, trip_id: int, passenger: Passenger, pickup_location: str, destination: str):
        self.trip_id = trip_id
        self.passenger = passenger
        self.pickup_location = pickup_location
        self.destination = destination
        self.status = "Pending"  # Status can be "Pending", "In Progress", "Completed", "Cancelled"
        self.rating = None
        self.comments = ""

    def start_trip(self):
        """Start the trip."""
        print(f"Trip {self.trip_id} has started for {self.passenger.name}.")
        self.status = "In Progress"
        self.simulate_trip_duration()

    def complete_trip(self):
        """Complete the trip."""
        if self.status == "In Progress":
            print(f"Trip {self.trip_id} completed.")
            self.status = "Completed"
            self.passenger.provide_feedback(random.randint(1, 5), "Great service!")  # Random feedback for demo
        else:
            print(f"Trip {self.trip_id} cannot be completed because it is not in progress.")

    def cancel_trip(self):
        """Cancel the trip."""
        if self.status == "Pending":
            print(f"Trip {self.trip_id} has been cancelled.")
            self.status = "Cancelled"
        else:
            print(f"Trip {self.trip_id} cannot be cancelled because it has already started.")

    def record_feedback(self, rating: int, comments: str):
        """Record feedback provided by the passenger."""
        self.rating = rating
        self.comments = comments
        print(f"Feedback recorded for Trip {self.trip_id}: {rating}/5 - {comments}")

    def simulate_trip_duration(self):
        """Simulate the trip duration with a delay."""
        duration = random.randint(10, 30)  # Trip duration between 10 to 30 seconds
        time.sleep(duration)  # Simulating trip time
        print(f"Trip {self.trip_id} duration was {duration} seconds.")

class BookingSystem:
    """Class to manage taxi bookings and passenger requests."""

    def __init__(self):
        self.passengers = []
        self.trips = []
        self.taxis_available = 5  # Simulate 5 available taxis

    def add_passenger(self, passenger: Passenger):
        """Add a new passenger to the system."""
        self.passengers.append(passenger)
        print(f"Passenger {passenger.name} added to the system.")

    def request_taxi_for_passenger(self, passenger: Passenger):
        """Handle taxi requests for a passenger."""
        if self.taxis_available > 0:
            trip = passenger.request_taxi()
            self.trips.append(trip)
            self.taxis_available -= 1
            print(f"Taxi assigned for {passenger.name}. Taxis available: {self.taxis_available}")
            trip.start_trip()
            trip.complete_trip()
            self.taxis_available += 1  # Free up taxi after trip
        else:
            print("No taxis available right now. Please wait.")

    def handle_passenger_feedback(self, passenger: Passenger):
        """Handle feedback from a passenger."""
        if passenger.current_trip:
            feedback = random.randint(1, 5)
            comments = "Nice ride!" if feedback > 3 else "Could be better."
            passenger.provide_feedback(feedback, comments)
        else:
            print("No current trip for feedback.")

# Simulating the entire passenger and trip management system
def simulate_taxi_service():
    booking_system = BookingSystem()

    # Create some passengers
    passengers = [
        Passenger("Alice", "Downtown", "Airport"),
        Passenger("Bob", "Airport", "Uptown"),
        Passenger("Charlie", "Midtown", "Suburbs"),
        Passenger("Diana", "Uptown", "Downtown"),
        Passenger("Eve", "Suburbs", "Midtown"),
    ]

    # Add passengers to the booking system
    for passenger in passengers:
        booking_system.add_passenger(passenger)

    # Request taxis for each passenger
    for passenger in passengers:
        booking_system.request_taxi_for_passenger(passenger)

    # Handle feedback for passengers
    for passenger in passengers:
        booking_system.handle_passenger_feedback(passenger)

if __name__ == "__main__":
    simulate_taxi_service()
