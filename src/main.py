import imaplib
from config import imap_server, username, password
from functions import get_mailboxes, analyze_mailbox

# Connect to the imap server
imap = imaplib.IMAP4_SSL(imap_server)
imap.login(username, password)

mailboxes = get_mailboxes(imap)
print(mailboxes)
result = analyze_mailbox(imap, "Inbox")
print(result)

# Disconnect from the imap server
imap.logout()