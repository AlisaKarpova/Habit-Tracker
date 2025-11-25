from src.habit_tracker.motivation.motivation import Motivation


def test_give_random_quote():
    motivation = Motivation()
    quote = motivation.give_random_quote()
    assert quote is not None

def test_unique_quotes():
    motivation = Motivation()
    quotes = [motivation.give_random_quote() for _ in range(10)]
    assert len(set(quotes)) == len(quotes)