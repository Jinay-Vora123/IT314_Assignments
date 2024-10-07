class PricingEngine:
    BASE_FARE = 2.50
    COST_PER_MILE = 1.25

    @staticmethod
    def calculate_fare(pickup_location: str, destination: str):
        distance = PricingEngine.estimate_distance(pickup_location, destination)
        fare = PricingEngine.BASE_FARE + (distance * PricingEngine.COST_PER_MILE)
        print(f"Calculated fare for trip from {pickup_location} to {destination}: ${fare:.2f}")
        return fare

    @staticmethod
    def estimate_distance(pickup_location: str, destination: str):
        distances = {
            ('North', 'South'): 12.0,
            ('East', 'West'): 15.5,
            ('South', 'North'): 10.0,
            ('West', 'East'): 18.2,
        }
        return distances.get((pickup_location, destination), 10.0)
