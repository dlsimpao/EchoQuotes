import json
import hashlib

class QuoteHandler():
    def __init__(self, quote_file_path, meta_file_path):
        print("Initializing quotes...")
        self.file_path = quote_file_path
        self._meta_file_path = meta_file_path

        with open(self.file_path, 'r') as json_file:
            quotes_data = json.load(json_file)

        with open(self._meta_file_path, 'r') as meta:
            meta_data = json.load(meta)
        
        self.quotes_db = quotes_data
        self._id_validation = meta_data

    # Function that generates a unique hash based on quote
    def generate_quote_id(self, quote_text):
        hash_obj = hashlib.sha256(str(quote_text).encode())
        return hash_obj.hexdigest()

    # Function to read quotes from JSON file
    def read_quotes_from_json(self):
        return self.quotes_db
    
    # Function to clean characters
    def attempt_clean_unicode(self, sentence):
        translate_dict = {
            "\u2019":"'",
            "\u2014":"---",
            "\u2013":"--",
            "\u00e9":"e"
        }
        for uni, ascii in translate_dict.items():
            sentence = sentence.replace(uni, ascii)
        return sentence
    
    # Function to add quotes to JSON file
    def add_quotes_to_json(self, new_quote_item):
        # add identifier
        qid = self.generate_quote_id(new_quote_item.get("quote"))
        new_quote_item["id"] = qid
        new_quote_item["quote"] = self.attempt_clean_unicode(new_quote_item.get("quote"))

        try:
            # if ID is unique, add to quotes database
            if qid not in self._id_validation:
                self.quotes_db.append(new_quote_item)
                self._id_validation.append(new_quote_item.get("id"))
                print("added data to quotes database")
            else:
                print(f"ID {qid} already exists! Data not added.")

            with open(self.file_path, 'w') as json_file, open(self._meta_file_path, 'w') as audit:               
                json.dump(self._id_validation, audit, indent = 2)
                json.dump(self.quotes_db, json_file, indent=2)

        except Exception as e:
            print("unable to add quote")
            print(f"error: {e}")

    # Function to update quotes in JSON file
    def update_quotes_in_json(self, update_quote_item):
        id_to_update = update_quote_item.get("id")
        if id_to_update not in self._id_validation:
            raise ValueError(f"Not in database! {id_to_update}")            
        else:
            for quote in self.quotes_db:
                if quote.get("id") == id_to_update:
                    quote["quote"] = update_quote_item.get("quote")
                    quote["author"] = update_quote_item.get("author")
                    quote["source"] = update_quote_item.get("source")
                    print(f"updated quote with data {quote}")
                    break
            with open(self.file_path, 'w') as json_file:          
                json.dump(self.quotes_db, json_file, indent=2)


    # Function to delete quotes based on id
    def delete_quote_in_json(self, msg):
        id_to_delete = msg.get("id")
        if id_to_delete not in self._id_validation:
            raise ValueError(f"Not in database! {id_to_delete}")            
        else:
            self._id_validation.remove(id_to_delete)
            for quote in self.quotes_db:
                if quote.get("id") == id_to_delete:
                    self.quotes_db.remove(quote)
                    print(f"removed quote with data {quote}")
                    break

            with open(self.file_path, 'w') as json_file, open(self._meta_file_path, 'w') as audit:               
                json.dump(self._id_validation, audit, indent = 2)
                json.dump(self.quotes_db, json_file, indent=2)
