import logging
import os
from datetime import datetime

# Create 'logged_messages' directory if it doesn't exist
log_dir = 'logged_messages'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Create log file path
log_file = os.path.join(log_dir, 'ex3__all_messages.log')

# Create and configure handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)  # Console shows only WARNING and above

file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)      # File stores everything

# Configure the root logger
logging.basicConfig(
    level=logging.DEBUG,  # Allow processing of all messages
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[console_handler, file_handler]
)

# Now test all levels
logging.debug("Debug message - in file only")
logging.info("Info message - in file only")
logging.warning("Warning message - in both file and console")
logging.error("Error message - in both file and console")
