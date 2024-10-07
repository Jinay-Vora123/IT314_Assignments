import logging
from logging_module import Logger
from trip_management import TripManager
from passengers import Passenger
from dispatcher_module import Dispatcher
from error_handling import TaxiNotAvailableException

class AdditionalFeature:
    def __init__(self, feature_name: str):
        self.feature_name = feature_name

    def execute(self):
        Logger.log_info(f"Executing additional feature: {self.feature_name}")
        # Simulate additional functionality
        result = self.feature_name + " executed successfully."
        Logger.log_debug(result)
        return result

def test_dispatching_system():
    Logger.log_info("Testing dispatching system...")

    dispatcher = Dispatcher()
    test_passengers = [
        Passenger("Eve", "North", "East"),
        Passenger("Frank", "South", "West"),
        Passenger("Grace", "East", "South"),
        Passenger("Hank", "West", "North"),
    ]

    for passenger in test_passengers:
        trip = passenger.request_taxi()
        dispatcher.trip_manager.start_trip(trip, dispatcher)

    for taxi in dispatcher.taxis:
        if taxi.current_trip:
            dispatcher.complete_trip(taxi)

def simulated_workload():
    for i in range(100):
        Logger.log_info(f"Simulating workload iteration: {i}")
        feature = AdditionalFeature(f"Feature {i}")
        feature.execute()

def main():
    Logger.log_info("Starting main system...")

    # Testing dispatching system with extra simulated workload
    test_dispatching_system()
    simulated_workload()

if __name__ == "__main__":
    main()
