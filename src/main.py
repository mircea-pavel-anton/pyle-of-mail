from config import imap_server, username, password, mailboxes, sleep_time
from functions import filter_mailbox, log

from imap_tools import MailBox
from time import sleep

# Connect to the imap server
log('Logging in to ' + imap_server + '...')
imap = MailBox(imap_server).login(username, password)
log('OK')

# Filtering is done here...
while True:
    for mailbox in mailboxes:
        log('Filtering started on' + mailbox)
        filter_mailbox(imap, mailbox)
    log('Napsiees!')
    sleep(sleep_time)
    log('Gluten morgan!')

# Disconnect from the imap server
imap.logout()