import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import policy
from email.parser import BytesParser
import re

class EmailHandler():
    def __init__(self, auth_user, auth_pass):
        self.user = auth_user
        self.password = auth_pass

        self._smtp_server = "smtp.gmail.com"
        self._smtp_port = 465

    def parse_raw_email(self, raw_message):
        msg = BytesParser(policy=policy.default).parsebytes(raw_message)
        
        # Extract the message body
        if msg.is_multipart():
            print("Parsing multipart...")
            for part in msg.iter_parts():
                if part.get_content_type() == 'text/plain':
                    message_body = part.get_payload(decode=True).decode(part.get_content_charset())
                    break
        else:
            message_body = msg.get_payload(decode=True).decode(msg.get_content_charset())

        print(f"Retrieving message: {message_body}")
        return message_body

    def read_emails(self, from_email):
        messages_list = []

        with imaplib.IMAP4_SSL(self._smtp_server) as server:
            server.login(self.user, self.password)
            server.select('inbox')

            status, messages = server.search(None, f'(UNSEEN FROM "{from_email}")')

            if status == "OK":
                messages = messages[0].split()
                print(f"Number of matching emails from {from_email}: {len(messages)}")

                # iterate through the matching emails
                for message_id in messages:
                    # Fetch the email
                    status, msg_data = server.fetch(message_id, '(RFC822)')
                    # print(msg_data)
                    raw_email = msg_data[0][1]
                    message = self.parse_raw_email(raw_email)
                    messages_list.append(message)

        return messages_list
    
    def parse_email_messages(self, messages):
        print("parsing email messsages...")
        message_list = []
        for message in messages:

            # Parses each message and retrieves records
            lines = message.strip().split("\r\n|")
            message_dict = {}

            for line in lines:
                line = re.sub(r'\r\n', ' ', line)
                key, value = line.split(" = ",1)
                message_dict[key] = value.encode('ascii', 'ignore').decode('ascii')

            message_list.append(message_dict)
        return message_list

    # Function to send an email
    def send_email(self, subject, body, to_email):
        # Replace these values with your own email configuration
        smtp_username = self.user
        smtp_password = self.password
        
        from_email = smtp_username
        
        # Create the MIMEText object for the email body
        message = MIMEText(body)
        
        # Setup the email headers
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = subject
        
        # Connect to the SMTP server
        with smtplib.SMTP_SSL(self._smtp_server, self._smtp_port) as server:
            server.login(smtp_username, smtp_password)
            
            # Send the email
            server.sendmail(from_email, to_email, message.as_string())