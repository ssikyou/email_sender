import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'dressmakercindy@gmail.com'
MAIL_PASSWORD = '903200xiao7'
MAIL_SENDER = 'cindy <dressmakercindy@gmail.com>'
enable_html = True

def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """
    
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
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
    if enable_html:
        message_html = read_template('message.html')

    # set up the SMTP server
    s = smtplib.SMTP(host=MAIL_SERVER, port=MAIL_PORT)
    s.starttls()
    s.login(MAIL_USERNAME, MAIL_PASSWORD)

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name)
        if enable_html:
            html = message_html.substitute(PERSON_NAME=name)
        # Prints out the message body for our sake
        print(message)
        if enable_html:
            print(html)

        # setup the parameters of the message
        msg['From']=MAIL_SENDER
        msg['To']=email
        msg['Subject']='Hi %s, Can I Make Custom Wedding Dresses And Special Occasion Dresses For You?' % name
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        if enable_html:
            msg.attach(MIMEText(html, 'html'))
        
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()
    
if __name__ == '__main__':
    main()