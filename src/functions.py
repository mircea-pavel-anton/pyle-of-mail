from log import logok, logerr
from collections import defaultdict
from config import filters
from imap_tools import A

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

def filter_mailbox(imap, mailbox):
    # Select the required mailbox
    imap.folder.set(mailbox)

    for rule in filters:
        mails = imap.fetch(A(from_=rule))
        imap.move(mails, filters[rule])

        for mail in mails:
            logok('Moving from ' + mailbox + ' to ' + filters[rule] + ' mail')
            logok('\tfrom: ' + mail.from_)
            logok('\tsubject: ' + mail.subject)


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

def create_folders(imap):
    # Get a list of all the mailboxes required for the filter rules
    folders = get_folders()

    # For each required folder, check if it already exists or not,
    # and create it if required.
    logok('Creating mailboxes...')
    for folder in folders:
        if imap.folder.exists(folder):
            logok('\t- Mailbox already exists: ' + folder)
        else:
            try:
                mailbox.folder.create(folder)
                logok('\t- Successfully created mailbox: ' + folder)
            except:
                logerr('Failed to create mailbox: ' + folder, True)
    logok('Done')
