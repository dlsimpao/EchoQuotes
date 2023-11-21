import random
from dotenv import load_dotenv
import os

from quoteHandler import *
from emailHandler import *

def main():
    load_dotenv()
    
    # Load in environment variables
    EM_USR = os.getenv("EMAIL_USERNAME")
    EM_PAS = os.getenv("EMAIL_PASSWORD")
    RC_USR = os.getenv("RECPT_EMAIL")
    AD_USR = os.getenv("ADMIN_EMAIL")
    SC = os.getenv("SECRET")

    print(f"{EM_USR}, {EM_PAS} , {RC_USR}")

    quo = QuoteHandler(quote_file_path='data/quotes.json', meta_file_path='data/quotes_metadata.json')
    emh = EmailHandler(EM_USR, EM_PAS)

    # Read quotes from the JSON file
    quo.read_quotes_from_json()

    # Read emails from a given user
    messages = emh.read_emails(from_email=AD_USR)

    # Parse each email
    parsed_messages = emh.parse_email_messages(messages=messages)

    for msg in parsed_messages:
        if msg.pop("auth", None) == SC:
            match msg.pop("request", None):
                case "create":
                    print("creating...")
                    quo.add_quotes_to_json(msg)
                case "readAll":
                    print("reading...")
                    updated_quotes = f'{json.dumps(quo.read_quotes_from_json(), indent = 4)}'
                    emh.send_email("All QUOTES", updated_quotes, EM_USR)
                case "update":
                    print("updating...")
                    quo.update_quotes_in_json(msg)
                case "delete":
                    print("deleting...")
                    quo.delete_quote_in_json(msg)
                case _:
                    print("request is unindentified") 
        else:
            raise ValueError("Invalid auth code. Not authorized to proceed.")
        


    # # Select a random quote
    # random_quote = random.choice(quotes)
    
    # print(random_quote)
    # # Email configuration
    # email_subject = 'Random Quote of the Day'
    # email_body = f'"{random_quote}"'
    # recipient_email = RC_USR
    
    # # # Send the email
    # eh.send_email(email_subject, email_body, recipient_email)

if __name__ == "__main__":
    main()