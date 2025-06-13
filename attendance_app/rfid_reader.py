import time
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class RFIDReader:
    def __init__(self):
        self.reader = None
        self.initialize_reader()
    
    def initialize_reader(self):
        """Initialize the RFID reader based on the environment"""
        try:
            if not settings.DEBUG:
                # Real hardware implementation for Raspberry Pi
                import RPi.GPIO as GPIO
                from mfrc522 import SimpleMFRC522
                
                self.reader = SimpleMFRC522()
                logger.info("RFID hardware reader initialized")
            else:
                # Simulation mode for development
                self.reader = None
                logger.info("RFID reader in simulation mode")
        except ImportError as e:
            logger.error(f"Failed to initialize RFID reader: {e}")
            self.reader = None
    
    def read_tag(self):
        """Read an RFID tag"""
        try:
            if self.reader is not None:
                # Real hardware reading
                id, text = self.reader.read()
                return str(id)
            else:
                # Simulation mode - return a test ID after 2 seconds
                time.sleep(2)
                return "123456789"
        except Exception as e:
            logger.error(f"Error reading RFID tag: {e}")
            return None
    
    def write_tag(self, text):
        """Write to an RFID tag"""
        try:
            if self.reader is not None:
                # Real hardware writing
                id = self.reader.write(text)
                return id
            else:
                # Simulation mode
                time.sleep(2)
                return "123456789"
        except Exception as e:
            logger.error(f"Error writing to RFID tag: {e}")
            return None
    
    def cleanup(self):
        """Clean up GPIO resources"""
        if self.reader is not None and hasattr(self.reader, 'cleanup'):
            self.reader.cleanup()
            logger.info("RFID reader GPIO cleaned up")

class RFIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rfid_reader = RFIDReader()
    
    def __call__(self, request):
        # Add RFID reader to request if needed
        if 'rfid' in request.path:
            request.rfid_reader = self.rfid_reader
        
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        self.rfid_reader.cleanup()
    
    def __del__(self):
        self.rfid_reader.cleanup()