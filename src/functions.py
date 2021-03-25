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
