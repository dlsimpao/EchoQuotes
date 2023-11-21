import re
import json

def test_parse_email_messages():
    sample = ['auth: randomauth\r\nquote: hello-quote\r\nsource: hello-source\r\nauthor: hello-author\r\n',
            'auth: randomauth\r\nquote: hello-quote2\r\nsource: hello-source2\r\nauthor: hello-author2\r\n',
            'auth: idk\r\nquote: hello-quote\r\nsource: hello-source\r\nauthor: hello-author\r\n']
    message_list = []

    for message in sample:
        lines = message.strip().split("\r\n")
        message_dict = {}

        for line in lines:
            key, value = line.split(": ",1)
            message_dict[key] = value

        message_list.append(message_dict)

    result_json = json.dumps(message_list, indent = 4)

    print(result_json)

def main():
    test_parse_email_messages()

if __name__ == "__main__":
    main()