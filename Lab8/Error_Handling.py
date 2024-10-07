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
