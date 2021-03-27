# Append log messages to the success log file
def logok(message):
    file = open(oklog, "a")
    file.write(message)
    file.close()

# Append log messages to the errlog files
# Default behaviour is to log the message and continue the
# execution of the program.
# One can force exit the script by passing `exit=True`
def logerr(message, exit = False):
    file = open(errlog, "a")
    file.write(message)
    
    if (exit):
        file.write('This is a critical failure. Exiting...')
        file.close()
        exit()
    else:
        file.close()

