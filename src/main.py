from config import imap_server, username, password
from functions import analyze_mailbox, filter_mailbox
from imap_tools import MailBox
from time import sleep

# Connect to the imap server
imap = MailBox(imap_server).login(username, password)

# Filtering is done here...
while True:
    for mailbox in mailboxes:
        filter_mailbox(imap, mailbox)
    sleep(sleep_time)

# Disconnect from the imap server
imap.logout()