# -----------------------------------------------------------
# demonstrates how to send emails with GMails API
#
# -----------------------------------------------------------

from __future__ import print_function

import os.path
import base64
from email.mime.text import MIMEText

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import mimetypes
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def create_mail_message(from_email, to_email, subject, message_text, attachment_path=None):
    """
	Create the email message from passed params.
	
	Parameters
    ----------
    from_email : str
        Sender's email address
    to_email : str
        Receiver's email address  
    subject : str
        Subject of email
	message_text : str
        Text of email
	attachment_path : str (optional)
        Path of attachment for email
		
	Returns
    ----------
	dict
        Encoded email message.
    """
    try:
        message = MIMEMultipart()
        message['To'] = to_email
        message['From'] = from_email
        message['Subject'] = subject
        message.attach(MIMEText(message_text))
        # encoded message
        create_message = {}

        if(attachment_path):
            print(F'Attachment path: {attachment_path}')
            attachment = build_file_part(file = attachment_path)
            message.attach(attachment)
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {
            'message': { 'raw': encoded_message }
                }

        else:
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {
                'raw': encoded_message
            }
        return create_message

    except Exception as e:
        print("Error in creating mail", e)
        return None




def gmail_auth():
    """
	Authorize GMail service.
		
	Returns
    ----------
	variable
        A Resource object with methods for interacting with the service.
    """
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)

    return service


def gmail_send_message(service, user_id, encoded_message):
    """
	Send email message.
	
	Parameters
    ----------
    service : variable
        Resource object with methods for interacting with the GMail service.
    user_id : str
        Sender's id  
    encoded_message : dict
        Encoded email message
		
	Returns
    ----------
	var
        Message which was sent
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=encoded_message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except HttpError as e:
        print('An error occurred: %s' % e)




if __name__ == '__main__':

    email = create_mail_message(from_email = 'numbr3la.services@gmail.com',
        to_email = 'arek99.10@gmail.com',
        subject = 'Hi',
        message_text = 'Python is great!')

    service = gmail_auth()

    gmail_send_message(service, 'numbr3la.services@gmail.com', email)