from config import logfile
from datetime import datetime

# Append log messages to the log file
def log(message):
    # Get the current time for the message timestamp
    time = datetime.now()
    timestamp = dateTimeObj.year + '/', dateTimeObj.month, '/', dateTimeObj.day, dateTimeObj.hour, ':', dateTimeObj.minute, ':', dateTimeObj.second, '.', dateTimeObj.microsecond

    # Timestamp the message and add a newline at the end
    message = f'[{timestamp}] {message}\n'

    # Open the log file, dump the message inside and then close it
    file = open(logfile, "a")
    file.write(message)
    file.close()
