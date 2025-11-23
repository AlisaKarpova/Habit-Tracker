import random
import json
from typing import Set, List


class Motivation:
    def __init__(self, file_path: str = 'motivation_quotes.json'):
        with open(file_path, encoding='utf-8') as file:
            self.quotes: List[str] = json.load(file)

        self.used_quotes: Set[str] = set()

    def give_random_quote(self) -> str:
        while True:
            selected_quote = random.choice(self.quotes)

            if selected_quote not in self.used_quotes:
                self.used_quotes.add(selected_quote)

                if len(self.used_quotes) == len(self.quotes):
                    self.used_quotes.clear()
            return selected_quote
