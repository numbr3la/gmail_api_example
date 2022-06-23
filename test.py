from gmail_api import *

if __name__ == '__main__':

    email = create_mail_message(from_email = 'example@gmail.com',
        to_email = 'user@example.com',
        subject = 'Hi',
        message_text = 'Python is great!')

    service = gmail_auth()

    gmail_send_message(service, 'example@gmail.com', email)