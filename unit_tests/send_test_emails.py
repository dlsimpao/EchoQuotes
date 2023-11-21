import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

class EmailHandler():
    def __init__(self, auth_user, auth_pass):
        self.user = auth_user
        self.password = auth_pass

        self._smtp_server = "smtp.gmail.com"
        self._smtp_port = 465

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

def main():
    # Load in environment variables
    load_dotenv()
    EM_USR = os.getenv("EMAIL_USERNAME")
    EM_PAS = os.getenv("EMAIL_PASSWORD")
    SECRET = os.getenv("SECRET")

    email_subject = "hello-test"
    recipient_email = EM_USR
    eh = EmailHandler(EM_USR, EM_PAS)

    # testing email to self
    for i in range(1, 4):
        print(f"sending test emails --> {i}")
        email_body = f"auth: {SECRET}\r\nrequest: create\r\nquote: hello-quote{i}\r\nsource: hello-source{i}\r\nauthor: hello-author{i}"

        eh.send_email(email_subject, email_body, recipient_email)

if __name__ == "__main__":
    main()