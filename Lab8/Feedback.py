import random

class FeedbackManager:
    @staticmethod
    def collect_feedback(taxi):
        # Simulate feedback collection
        feedback = random.randint(1, 5)
        print(f"Passenger gave a feedback of {feedback} to Taxi {taxi.taxi_id}")
        taxi.receive_feedback(feedback)
