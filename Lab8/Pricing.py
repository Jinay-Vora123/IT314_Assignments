import logging
from datetime import datetime
import random

# Setting up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class PricingEngine:
    BASE_FARE = 2.50
    COST_PER_MILE = 1.25
    PEAK_HOUR_MULTIPLIER = 1.5
    DISCOUNT_CODES = {
        "WELCOME10": 0.10,  # 10% discount
        "SUMMER20": 0.20,   # 20% discount
    }

    @staticmethod
    def calculate_fare(pickup_location: str, destination: str, discount_code: str = None):
        """Calculate the fare based on the pickup location and destination."""
        distance = PricingEngine.estimate_distance(pickup_location, destination)
        fare = PricingEngine.BASE_FARE + (distance * PricingEngine.COST_PER_MILE)
        
        # Apply surge pricing if applicable
        fare *= PricingEngine.apply_surge_pricing()

        # Apply discount if provided
        if discount_code:
            fare *= (1 - PricingEngine.get_discount(discount_code))
        
        logging.info(f"Calculated fare for trip from {pickup_location} to {destination}: ${fare:.2f}")
        return fare

    @staticmethod
    def estimate_distance(pickup_location: str, destination: str):
        """Estimate distance based on pickup and destination locations."""
        distances = {
            ('North', 'South'): 12.0,
            ('East', 'West'): 15.5,
            ('South', 'North'): 10.0,
            ('West', 'East'): 18.2,
        }
        return distances.get((pickup_location, destination), 10.0)

    @staticmethod
    def apply_surge_pricing():
        """Determine if surge pricing should be applied."""
        current_hour = datetime.now().hour
        if 17 <= current_hour <= 19:  # Example peak hours
            logging.info("Surge pricing is in effect.")
            return PricingEngine.PEAK_HOUR_MULTIPLIER
        logging.info("Normal pricing is in effect.")
        return 1.0

    @staticmethod
    def get_discount(code: str):
        """Get discount percentage based on the code provided."""
        return PricingEngine.DISCOUNT_CODES.get(code, 0.0)

class Trip:
    """Class representing a trip with fare calculations."""
    
    def __init__(self, trip_id: int, passenger: Passenger, pickup_location: str, destination: str, discount_code: str = None):
        self.trip_id = trip_id
        self.passenger = passenger
        self.pickup_location = pickup_location
        self.destination = destination
        self.discount_code = discount_code
        self.fare = 0.0

    def calculate_fare(self):
        """Calculate fare for the trip using the PricingEngine."""
        self.fare = PricingEngine.calculate_fare(self.pickup_location, self.destination, self.discount_code)
        logging.debug(f"Trip {self.trip_id} fare calculated: ${self.fare:.2f}")

    def start_trip(self):
        """Start the trip and calculate fare."""
        logging.info(f"Trip {self.trip_id} started for {self.passenger.name}.")
        self.calculate_fare()

class BookingSystem:
    """Class to manage taxi bookings and passenger requests."""

    def __init__(self):
        self.passengers = []
        self.trips = []
        self.taxis_available = 5  # Simulate 5 available taxis

    def add_passenger(self, passenger: Passenger):
        """Add a new passenger to the system."""
        self.passengers.append(passenger)
        logging.info(f"Passenger {passenger.name} added to the system.")

    def request_taxi_for_passenger(self, passenger: Passenger, discount_code: str = None):
        """Handle taxi requests for a passenger."""
        if self.taxis_available > 0:
            trip = Trip(random.randint(1000, 9999), passenger, passenger.pickup_location, passenger.destination, discount_code)
            self.trips.append(trip)
            self.taxis_available -= 1
            logging.info(f"Taxi assigned for {passenger.name}. Taxis available: {self.taxis_available}")
            trip.start_trip()
            logging.info(f"Trip {trip.trip_id} completed for {passenger.name}. Fare: ${trip.fare:.2f}")
            self.taxis_available += 1  # Free up taxi after trip
        else:
            logging.warning("No taxis available right now. Please wait.")

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

    # Request taxis for each passenger with some discount codes
    discount_codes = ["WELCOME10", None, "SUMMER20", None, None]
    for passenger, code in zip(passengers, discount_codes):
        booking_system.request_taxi_for_passenger(passenger, code)

if __name__ == "__main__":
    simulate_taxi_service()
