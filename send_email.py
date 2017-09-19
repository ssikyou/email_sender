import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            # print('{}:{}'.format(var[0], var[1]))
            os.environ[var[0]] = var[1]

import socks
socks.setdefaultproxy(socks.SOCKS5, '127.0.0.1', 1080)
socks.wrapmodule(smtplib)

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_SENDER = 'cindy <dressmakercindy@gmail.com>'

if os.environ.get('ENABLE_HTML') == 'False':
    ENABLE_HTML = False
else:
    ENABLE_HTML = True

if os.environ.get('DEBUG') == 'False':
    DEBUG = False
else:
    DEBUG = True


def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """
    
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            a_contact_s = a_contact.strip()
            if a_contact_s == '':
                break
            else:
                names.append(a_contact_s.split('@')[0])
                emails.append(a_contact_s)
    return names, emails

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def main():
    names, emails = get_contacts('contacts.txt') # read contacts
    message_template = read_template('message.txt')
    if ENABLE_HTML:
        message_html = read_template('message.html')

    # set up the SMTP server
    s = smtplib.SMTP(host=MAIL_SERVER, port=MAIL_PORT)
    s.starttls()
    s.login(MAIL_USERNAME, MAIL_PASSWORD)

    if DEBUG:
        print(names)
        print(emails)

    # For each contact, send the email:
    print('\nStart sending emails...')
    for name, email in zip(names, emails):
        print('name:%s email:%s' % (name, email))
        msg = MIMEMultipart('alternative')       # create a message

        if name == 'info':
            name = ''

        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name)
        if ENABLE_HTML:
            html = message_html.substitute(PERSON_NAME=name)
        # Prints out the message body for our sake
        if DEBUG:
            print(message)
            if ENABLE_HTML:
                print(html)

        # setup the parameters of the message
        msg['From']=MAIL_SENDER
        msg['To']=email
        msg['Subject']='Hi %s, Can I Make Custom Wedding Dresses And Special Occasion Dresses For You?' % name
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        if ENABLE_HTML:
            msg.attach(MIMEText(html, 'html'))
        
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg

    print('Done!')
    # Terminate the SMTP session and close the connection
    s.quit()
    
if __name__ == '__main__':
    main()