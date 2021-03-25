import imaplib
from config import imap_server, username, password

# Connect to the imap server
imap = imaplib.IMAP4_SSL(imap_server)
imap.login(username, password)

def list_mailboxes():
    response_code, folders = imap.list()
    print('Available folders(mailboxes) to select:')
    for folder_details_raw in folders:
        folder_details = folder_details_raw.decode().split()
        print(f'- {folder_details[-1]}')

list_mailboxes()

# Disconnect from the imap server
imap.logout()