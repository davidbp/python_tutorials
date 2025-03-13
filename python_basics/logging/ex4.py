import logging
import os
from datetime import datetime

# Create 'logged_messages' directory if it doesn't exist
log_dir = 'logged_messages'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Create log file path with timestamp
timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
log_file = os.path.join(log_dir, f'ex4__all_messages__{timestamp}.log')

# Create and configure handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)  # Console shows only WARNING and above

file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)      # File stores INFO and above (changed from DEBUG)

# Configure the root logger
logging.basicConfig(
    level=logging.DEBUG,  # Keep DEBUG as lowest level to allow all messages to be processed
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[console_handler, file_handler]
)

# Test all logging levels
logging.debug("Debug message - won't be stored anywhere")
logging.info("Info message - in file only")
logging.warning("Warning message - in both file and console")
logging.error("Error message - in both file and console")
