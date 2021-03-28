from config import filters, logfile, username, password, imap_server

from imap_tools import MailBox, A
from collections import defaultdict
from datetime import datetime


# Connect to the imap server + logging
def imap_connect():
    log('Logging in to ' + imap_server + '...')
    imap = MailBox(imap_server).login(username, password)
    log('OK')
    return imap

# Disconnect from the imap server + logging
def imap_disconnect(imap):
    log('Disconnecting from ' + imap_server + '...')
    imap.logout()
    log('OK')

# Append log messages to the log file
def log(message):
    # Get the current time for the message timestamp
    time = datetime.now()

    # Extract the timestamp from the current time, and make sure it's 30 chars long
    timestamp = '[ ' + str(time.day) + '/' + str(time.month) + '/' + str(time.year) + " | " + str(time.hour) + ':' + str(time.minute) + ':' + str(time.second) + '.' + str(time.microsecond) + ' ]'
    while len(timestamp) < 30:
        timestamp += ' '

    # Timestamp the message and add a newline at the end
    message = f'{timestamp}\t{message}\n'

    # Open the log file, dump the message inside and then close it
    file = open(logfile, "a+")
    file.write(message)
    file.close()
    print(message)

# Analyzes the given mailbox.
# It goes through all emails inside a mailbox and returns a dictionary
# that holds each unique email address as the key, and the number of emails
# received from them as the value
def analyze_mailbox(imap, mailbox):
    imap.folder.set(mailbox)

    # Dictionary that holds the address of the sender as key
    # and the number of emails as the value
    senders = defaultdict(lambda: 0)

    # For each email, increment the dict value for the sender
    for msg in imap.fetch():
        senders[msg.from_] += 1

    # Return the dictionary
    return senders

# Applies all the filters from the config file on the given mailbox
# Returns the number of emails that got moved around
def filter_mailbox(imap, mailbox):
    # Select the required mailbox
    imap.folder.set(mailbox)

    count = 0 # number of emails that got moved around

    # Fetch all unseen emails from the given mailbox
    # NOTE: the returned value of ima.fetc() is a generator
    # we want to convert it to a list, so that we can loop
    # through it multiple times.
    mails_list = list(imap.fetch(A(seen=True)))

    # This dictionary acts as a 'to do list', in the sense that
    # it stores what emails should be moved and where.
    # The structure of the dictionary is as follows:
    # - the value element holds a list of email UIDs
    # - the key element stores the name of the mailbox in which
    #     the emails from the value should be moved
    dict = defaultdict(lambda: [])

    # For each retrieved mail, check it against each rule in the filters
    for mail in mails_list:
        for rule in filters:
            # Convert both strings to upper, since we do not want the filters to
            # be case-sensitive
            if rule.upper() in mail.from_.upper():
                dict[filters[rule]].append(mail.uid)
                log('Moving from ' + mailbox + ' to ' + filters[rule] + ' mail')
                log('\tfrom: ' + mail.from_)
                log('\tsubject: ' + mail.subject)
                count += 1

    # Parse the dictionary for each directory, and move the emails in bulk
    # This should be more efficient thatn moving each email at a time in terms
    # of requests/sec.
    for entry in dict:
        imap.move([m for m in dict[entry]], entry)

    return count

# Parses the filters from the config file and extracts the mailbox structure/hierarchy
def get_folders():
    list = []

    # Loop through all the folders defined in the filters and extract a list
    # of all unique folders.
    for entry in filters:
        # Get the folder path from the filter entry
        folder = filters[entry]

        # The folders defined in the filters contain a full path.
        # As such, we need to split that path and extract all the subfolders.
        target = ''

        for level in folder.split('/'):
            # Add one level to the path per iteration
            target += '{}/'.format(level)

            # Remove the trailing backslash
            formatted = target[0 : len(target) - 1]

            # Add it to the list if it's not in there already
            if (formatted not in list):
                list.append(formatted)

    return list

# Creates the required mailbox hierarchy based on the filters listed in the config file
def create_folders(imap):
    # Get a list of all the mailboxes required for the filter rules
    folders = get_folders()

    # For each required folder, check if it already exists or not,
    # and create it if required.
    log('Creating mailboxes...')
    for folder in folders:
        if imap.folder.exists(folder):
            log('\t- Mailbox already exists: ' + folder)
        else:
            try:
                imap.folder.create(folder)
                log('\t- Successfully created mailbox: ' + folder)
            except:
                log('Failed to create mailbox: ' + folder)
    log('Done')
