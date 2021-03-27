from config import mailboxes, sleep_time
from functions import filter_mailbox, log, create_folders, imap_connect, imap_disconnect

from imap_tools import MailBox
from time import sleep


# Connect to the imap server, ensure the needed
# mailboxes are present and then disconnect
imap = imap_connect()
create_folders(imap)
imap_disconnect(imap)

# Loop indefinetly
while True:
    # Connect to the imap server using the credentials found in config.py
    imap = imap_connect()

    # Loop through all the required mailboxes and filter them
    for mailbox in mailboxes:
        log('Filtering started on ' + mailbox)
        filter_mailbox(imap, mailbox)

    # Disconnect from the imap server
    imap_disconnect(imap)

    # Sleep for as many seconds as indicated in the config.py file
    log('Napsiees!')
    sleep(sleep_time)
    log('Gluten morgan!')
