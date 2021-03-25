import email
from config import filters

# Returns an array containing the names of all available mailboxes on the
# selected imap server
def get_mailboxes(imap):
    # An array that will hold the names of all available mailboxes
    mailboxes = []

    # Fetch all folders from the imap server
    response_code, folders = imap.list()

    # Loop through all the folders, extract their names and dump them
    # into @mailboxes
    for folder_details_raw in folders:
        folder_details = folder_details_raw.decode().split()
        mailboxes.append(folder_details[-1].replace('"',''))

    # return the array of available mailboxes
    return mailboxes

# Returns the sender of the given message
def extract_sender(imap, message_number):
    # Fetch the given message based on the number
    _, msg = imap.fetch(message_number, '(RFC822)')

    # Parse the data bytes
    mail = email.message_from_bytes(msg[0][1])

    # Return the sender field
    return mail["from"]

# Analyzes the emails in the given mailbox.
# It returns a dictionary containing the address of the sender
# as the key, and the number of emails received from them as the
# value.
def analyze_mailbox(imap, mailbox):
    # Select the given mailbox as to only analyze it
    imap.select(mailbox)

    # A dictionary that will contain pairs in this format:
    # { "sender_address@provider.whatever": number_of_emails_received_from_them }
    senders = {}

    # Fetch all message numbers in the given mailbox
    _, message_numbers_raw = imap.search(None, 'ALL')

    # Loop through all available emails
    for message_number in message_numbers_raw[0].split():
        # Extract the email sender
        sender = extract_sender(imap, message_number)

        # If the doesn't exist in the dictionary, add it with a value of 1
        # Otherwise, increment the associated number
        if sender not in senders:
            senders[sender] = 1
        else:
            senders[sender] += 1

    return senders

# Logger function. Should print to some log file, or stdout or something
# this is plenty for now, but i should really not forget to change this later :)
def log(message):
    print(message)

# Loop through all the filters defined in the config, and ensure
# the appropriate mailboxes are present for the filtering to take
# place
def create_folder_structure(imap):
    # Get a list of all existing mailboxes
    mailboxes = get_mailboxes(imap)

    # For every folder defined in the filters, check if it already exists
    # and create it if it does not
    for entry in filters:
        # Get the folder path from the filter entry
        folder = filters[entry]

        # The folders defined in the filters contain a full path.
        # As such, we need to split that path and create all the required
        # subfolders, otherwise it will create a single folder with slashes
        # in the name
        # For example, for the structure "a/b/c", the target directory will
        # be "a", then "a/b", then "a/b/c" to ensure the proper hierarchy
        # is created.
        target = ""
        for level in folder.split('/'):
            # Add one level to the path per iteration
            target += "{}/".format(level)
            # Check if target already exists.
            # If it does not, create it and log it
            if (target not in mailboxes):
                imap.create(target)
                mailboxes.append(target)
                log("Created mailbox: " + target)
            else:
                log("Mailbox " + target + " already exists")

