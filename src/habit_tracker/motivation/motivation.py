import json
import random
from typing import List, Set


class Motivation:
    """Give a motivational quote."""

    def __init__(self, file_path: str = 'src/habit_tracker/motivation/motivation_quotes.json'):
        """
        Initialize the Motivation.

        Args:
            file_path (str): path to the JSON file with quotes. By default —
         'src/habit_tracker/motivation/motivation_quotes.json'
        """
        with open(file_path, encoding='utf-8') as file:
            self.quotes: List[str] = json.load(file)

        self.used_quotes: Set[str] = set()

    def give_random_quote(self) -> str:
        """
        Provide user with a random motivational quote.

        Returns:
            str: random quote
            When all available quotes have been used at least once, the set of used quotes is cleared,
        allowing you to start a new cycle of issuing unique quotes
        """
        while True:
            selected_quote = random.choice(self.quotes)

            if selected_quote not in self.used_quotes:
                self.used_quotes.add(selected_quote)

                if len(self.used_quotes) == len(self.quotes):
                    self.used_quotes.clear()

                return selected_quote
