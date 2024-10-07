import logging
import os
import sys
from logging.handlers import RotatingFileHandler, SMTPHandler

# Define constants for log file configuration
LOG_DIR = "logs"
LOG_FILE = "app.log"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3

# Ensure the log directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

class CustomFormatter(logging.Formatter):
    """Custom logging formatter to enhance log output."""
    
    def format(self, record):
        log_fmt = f'%(asctime)s - %(levelname)s - [%(name)s] - %(message)s'
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class Logger:
    """Logger class to encapsulate logging functionality."""
    
    @staticmethod
    def setup_logging():
        """Set up logging configuration."""
        # Create a logger
        logger = logging.getLogger("TaxiAppLogger")
        logger.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(CustomFormatter())
        logger.addHandler(console_handler)

        # File handler with rotation
        file_handler = RotatingFileHandler(os.path.join(LOG_DIR, LOG_FILE), 
                                           maxBytes=MAX_LOG_SIZE, 
                                           backupCount=BACKUP_COUNT)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(CustomFormatter())
        logger.addHandler(file_handler)

        # SMTP handler for critical errors
        smtp_handler = SMTPHandler(
            mailhost=('smtp.gmail.com', 587),
            fromaddr='your_email@gmail.com',  # Update with your email
            toaddrs=['admin@example.com'],  # Update with the recipient email
            subject='Critical Error in Taxi App',
            credentials=('your_email@gmail.com', 'your_password'),  # Update with your email credentials
            secure=()
        )
        smtp_handler.setLevel(logging.CRITICAL)
        smtp_handler.setFormatter(CustomFormatter())
        logger.addHandler(smtp_handler)

        Logger.logger = logger  # Store the logger as a static variable

    @staticmethod
    def log_info(message: str):
        Logger.logger.info(message)

    @staticmethod
    def log_debug(message: str):
        Logger.logger.debug(message)

    @staticmethod
    def log_error(message: str):
        Logger.logger.error(message)

    @staticmethod
    def log_critical(message: str):
        Logger.logger.critical(message)

class Application:
    """Main application class to demonstrate logging functionality."""

    def __init__(self):
        self.setup_logging()

    def setup_logging(self):
        """Set up logging for the application."""
        Logger.setup_logging()
        Logger.log_info("Logging setup complete.")

    def run(self):
        """Run the main application logic."""
        Logger.log_info("Starting the application...")

        try:
            self.perform_operations()
        except Exception as e:
            Logger.log_error(f"An error occurred: {e}")
            self.handle_critical_error(e)

    def perform_operations(self):
        """Simulate some application operations."""
        Logger.log_info("Performing some operations...")

        for i in range(10):
            if i == 5:
                Logger.log_debug("This is a debug message.")
            elif i == 8:
                Logger.log_critical("A critical operation has failed!")
            else:
                Logger.log_info(f"Operation {i} completed successfully.")

    def handle_critical_error(self, error):
        """Handle a critical error."""
        Logger.log_critical(f"Handling critical error: {error}")
        # Here you could add more recovery logic or notifications

    def generate_report(self):
        """Generate a report of application activities."""
        Logger.log_info("Generating report...")
        # Simulate report generation logic
        for i in range(3):
            Logger.log_info(f"Report section {i + 1}: Data processed.")

        Logger.log_info("Report generation complete.")

class TaxiApplication(Application):
    """Extended application for the Taxi system."""
    
    def perform_operations(self):
        """Override to include taxi-specific operations."""
        Logger.log_info("Performing taxi operations...")

        for i in range(10):
            if i == 3:
                Logger.log_debug("This is a debug message related to taxi operations.")
            elif i == 7:
                Logger.log_critical("A taxi has reported a critical failure!")
            else:
                Logger.log_info(f"Taxi operation {i} completed successfully.")
        
        self.generate_report()  # Generate report at the end of operations

if __name__ == "__main__":
    app = TaxiApplication()
    app.run()
