
# The `logging` module

Logging is means of tracking events that happen during software execution.

The `logging` module provides a set of convenience functions that are meant to be used in differnet scenarios



- **`logging.info()`**: Report events that occur during normal/expected operation of a program.

- **`logging.debug()`**: Report detailed otuput for diagnostic purposes.

- **`logging.warn()`**: Issue a warning due to a runtime event, use this if the situation is avoidable by the user to eliminate the warning.

- **`logging.warning()`**: Issue a warning due to a runtime event, use this if the user cannnot do anything about the situation, the the event should be notted.

- **`logging.error()`**: Report error without raising a python exception.


By default, messages that are not printed (due to the logging level threshold) are simply discarded and are not stored anywhere. The logging module only processes messages that meet or exceed the configured logging level.



### Example 1:

In `ex1.py` one can find the following code

```python
import logging
logging.warning('Warning: check this!')  # will print a message to the console
logging.info('Information logged')  # will not print anything
```

When running `ex1.py` the user will see:

```python
WARNING:root:Warning: check this!
```

Note: Nothing about the `logging.info()` message is displayed..

Without configuration, only messages at WARNING level or higher will be displayed. The logging levels in order of increasing severity are:
    
```python
DEBUG (10) < INFO (20) < WARNING (30) < ERROR (40) < CRITICAL (50)
```

Now in example 2 we will simply add `logging.basicConfig(level=logging.INFO)` to the code so that `INFO` messages are shown.



### Example 2: Chaning logging displayed information

One can change what is printed in the terminal when running a script updating the level of `logging` using `logging.basicConfig(level=logging.LEVEL)`
where `LEVEL` can be a string from `[]`.

For example, if we add `LEVEL=INFO`, as one can see in `ex2.py`


```python
import logging

logging.basicConfig(level=logging.INFO)

logging.warning('Warning: check this!')  # will be printed because `logging.basicConfig(level=logging.INFO)`
logging.info('Information logged')  # will be printed
```

When running `python ex2.py` the user will see:

```
WARNING:root:Warning: check this!
INFO:root:Information logged
```

Which includes the `INFO` details that did not appear in `ex1.py`.



### Example 3: Storing some logged information with a file handler with **`logging.FileHandler`**


The code in  `ex3.py` shows how to add a handler that stores to disk the logged messages.

- To print in the console `console_handler = logging.StreamHandler()` is used. 

- To print in a file `file_handler = logging.FileHandler(log_file)` is used.


```python
import logging

# Create and configure handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)  # Console shows only WARNING and above

file_handler = logging.FileHandler('all_messages.log')
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
```


After running this:

- Console output will show only WARNING and ERROR messages

- The file `ex3__all_messages.log` will contain ALL messages (DEBUG, INFO, WARNING, and ERROR)




### Example 4: Storing some logged information with a file handler with **`logging.FileHandler`** and adding time into the logged filename


Example `ex4.py` shows how to create a logger that stores the logged items to disk with **`logging.FileHandler`**. The example also has a logger that takes care of printing to the console (we can use more than one logger!).

- To print in the console `console_handler = logging.StreamHandler()` is used. 

- To print in a file `file_handler = logging.FileHandler(log_file)` is used.

 
```python
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
```


After running this:

- Console output will show only WARNING and ERROR messages

- The file `ex4__all_messages__2025_02_25_11_20_04.log` will contain messages INFO, WARNING, and ERROR.

