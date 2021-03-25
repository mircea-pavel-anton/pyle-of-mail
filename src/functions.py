import email
from config import filters
from sys import exit

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
def extract_sender(imap, message_uid):
    sender = ""
    
    try:
        # Fetch the given message based on the number
        rc, msg = imap.fetch(message_uid, '(RFC822)')

        # If the operation was successful, extract the data
        if (rc == 'OK'):
            # Parse the data bytes
            mail = email.message_from_bytes(msg[0][1])
            sender = mail["from"]
        else:
            log("Failed to fetch mail: " + str(message_uid))

    except:
        log("Failed to fetch mail: " + str(message_uid))

    # Return the sender field
    return sender

# Analyzes the emails in the given mailbox.
# It returns a dictionary containing the address of the sender
# as the key, and the number of emails received from them as the
# value.
def analyze_mailbox(imap, mailbox):
    # A dictionary that will contain pairs in this format:
    # { "sender_address@provider.whatever": number_of_emails_received_from_them }
    senders_dict = {}

    try:
        # Select the given mailbox as to only analyze it
        imap.select(mailbox)

        # Fetch all message numbers in the given mailbox
        rc, data = imap.search(None, 'ALL')

        # If the operation was succesful, analyze the data
        # otherwise, log an error
        if (rc == 'OK'):
            index = 1
            # Loop through all available emails
            for message_uid in data[0].split():
                print(str(index) + "/" + str(len(data[0].split())))
                # Extract the email sender
                sender = extract_sender(imap, message_uid)

                # If the doesn't exist in the dictionary, add it with a value of 1
                # Otherwise, increment the associated number
                if sender not in senders_dict:
                    senders_dict[sender] = 1
                else:
                    senders_dict[sender] += 1
                index += 1
        else:
            log("Failed to fetch all messages in mailbox:" + mailbox)
    except:
        log("Failed to fetch all messages in mailbox:" + mailbox)

    finally:
        imap.close() # Close the opened mailbox

    return senders_dict

# Logger function. Should print to some log file, or stdout or something
# this is plenty for now, but i should really not forget to change this later :)
def log(message):
    print(message)

# Loop through all the filters defined in the config, and ensure
# the appropriate mailboxes are present for the filtering to take
# place
def create_folder_structure(imap):
    log("Creating mailboxes...")
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

            # Remove the trailing backslash
            formatted = target[0 : len(target) - 1]

            # Check if target already exists. If it does not, create it and log it
            if (formatted not in mailboxes):
                try:
                    imap.create(formatted)  # Create mailbox
                    mailboxes.append(formatted) # Add it to the cached list
                    log("Created mailbox: " + formatted)
                except:
                    log("Failed to create mailbox: " + formatted)
                    log("That is a critical error. Exiting...")
                    sys.exit()
            else:
                log("Mailbox " + formatted + " already exists")
    log("Done")
