import sys
import os
import imaplib
import getpass
import email
import datetime
from pprint import pprint

M = imaplib.IMAP4_SSL('imap.gmail.com')

def process_mailbox(M):
    M.select()
    #rv, data = M.select("mailboxes/INBOX")
    rv, data = M.search(None, "ALL")
    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", num)
            return
        #print(data[0][1])
        msg = email.message_from_bytes(data[0][1])
        if msg.get_content_maintype() != 'multipart':
            continue

        print('Message %s: %s' % (num, msg['Subject']))
#         print('Raw Date:', msg['Date'])
#         date_tuple = email.utils.parsedate_tz(msg['Date'])
#         if date_tuple:
#             local_date = datetime.datetime.fromtimestamp(
#                 email.utils.mktime_tz(date_tuple))
#             print("Local Date:",local_date.strftime("%a, %d %b %Y %H:%M:%S"))
    for part in msg.walk():
        # multipart are just containers, so we skip them
        if part.get_content_maintype() == 'multipart':
            continue

        # is this part an attachment ?
        if part.get('Content-Disposition') is None:
            continue

        filename = part.get_filename()
        counter = 1

        # if there is no filename, we create one with a counter to avoid duplicates
        if not filename:
            filename = 'part-%03d%s' % (counter, 'bin')
            counter += 1
        
        detach_dir = '/home/shraddha/Downloads'
        att_path = os.path.join(detach_dir, filename)

        #Check if its already there
        if not os.path.isfile(att_path) :
            # finally write the stuff
            fp = open(att_path, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()
            
#M.login('testingpython7@gmail.com', getpass.getpass())
M.login('testingpython7@gmail.com', 'Synechron18@@')
process_mailbox(M)
