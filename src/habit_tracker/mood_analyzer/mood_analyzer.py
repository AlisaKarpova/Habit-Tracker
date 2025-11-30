from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from src.habit_tracker.trackers_main_classes import Record

POSITIVE_THRESHOLD = 0.5
NEGATIVE_THRESHOLD = -0.05


class UsersMood:
    """Determine the mood by text."""

    def __init__(self):
        """Initialize the UserMood."""
        self.analyzer = SentimentIntensityAnalyzer()
        self.analyzer.lexicon.update({'плохое': -2.0, 'хорошее': 4.0, 'нормальное': 2.5})

    def determine_mood(self, record: Record) -> None:
        """
        Determine the user's mood.

        Args:
            record (Record): an instance of the Record class containing the mood text
        """
        sentiment = self.analyzer.polarity_scores(record.mood)
        compound_score = sentiment['compound']

        if compound_score >= POSITIVE_THRESHOLD:
            record.mood = 'хорошее'
        elif compound_score <= NEGATIVE_THRESHOLD:
            record.mood = 'плохое'
        else:
            record.mood = 'нормальное'
