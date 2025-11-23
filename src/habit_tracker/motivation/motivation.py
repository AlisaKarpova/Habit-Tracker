import random
import json

class Motivation:
    def __init__(self, file_path='motivation_quotes.json'):
        with open(file_path, encoding='utf-8') as file:
            self.quotes = json.load(file)

        self.used_quotes = set()

    def give_random_quote(self):
        while True:
            selected_quote = random.choice(self.quotes)

            if selected_quote not in self.used_quotes:
                self.used_quotes.add(selected_quote)

                if len(self.used_quotes) == len(self.quotes):
                    self.used_quotes.clear()
            return selected_quote
