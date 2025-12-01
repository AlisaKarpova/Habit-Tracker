from datetime import date, datetime
from typing import List, Optional, Set
from uuid import uuid4


class User:
    """Represent the user."""

    def __init__(self, name: str, user_id: Optional[str] = None):
        """
        Initialize the User.

        Args:
            name (str): name of the user
            user_id (Optional[str], optional): the user's ID. If not specified, it is generated automatically

        Returns:
            None
        """
        self.user_name = name
        self.user_id = user_id or str(uuid4())
        self.user_habits: Set[str] = set()

    def add_habit(self, habit: str) -> None:
        """
        Add a new habit.

        Args:
            habit (str): name of the added habit

        Returns:
            None
        """
        self.user_habits.add(habit)

    def remove_habit(self, habit_to_remove: str) -> None:
        """
        Remove the specified habit.

        Args:
            habit_to_remove (str): name of the habit that is needed to be removed

        Returns:
            None
        """
        if habit_to_remove in self.user_habits:
            self.user_habits.remove(habit_to_remove)

    def habits(self) -> Set[str]:
        """
        Return a set of the user's current habits.

         Returns:
             Set[str]: set of active user habits
        """
        return self.user_habits


class Habit:
    """Describe user's habit."""

    def __init__(self, name: str, freq: str, start_day: str, end_day: str):
        """
        Initialize the Habit.

        Args:
            name (str): name of the habit
            freq (str): frequency of habit fulfillment ("daily", "every Tuesday")
            start_day (str): starting date in the 'dd-mm-yyyy' format
            end_day (str): final date in the 'dd-mm-yyyy' format

        Returns:
            None
        """
        self.habit_name = name
        self.frequency = freq
        self.start_day = datetime.strptime(start_day, '%d-%m-%Y').date()
        self.end_day = datetime.strptime(end_day, '%d-%m-%Y').date()
        self.completed_days: List[date] = []

    def is_complited(self, day: str) -> bool:
        """
        Determine whether a given habit is marked as completed on the specified day.

        Args:
            day (str): day of the checking in the 'dd-mm-yyyy' format

        Returns:
            bool: True if the habit is completed on that day, otherwise False
        """
        target_day = datetime.strptime(day, '%d-%m-%Y').date()
        return target_day in self.completed_days

    def completion_mark(self, day: str) -> None:
        """
        Mark the fact that the habit was completed on the specified day.

        Args:
            day (str): day the habit was completed, in the 'dd-mm-yyyy' format

        Returns:
            None
        """
        target_day = datetime.strptime(day, '%d-%m-%Y').date()
        if self.end_day >= target_day >= self.start_day:
            self.completed_days.append(target_day)

    def total_period(self) -> int:
        """
        Calculate the total habit period in days.

        Returns:
            int: number of days of habit fulfillment
        """
        return (self.end_day - self.start_day).days + 1

    def completion_rate(self) -> float:
        """
        Calculate the percentage of completed days relative to the total number of days.

        Returns:
            float: percentage of completed days rounded to two decimal places
        """
        total_days = self.total_period()
        completed_count = len(self.completed_days)
        if total_days > 0:
            return round((completed_count / total_days) * 100, 2)
        return 0


class Record:
    """Record of habit fulfillment."""

    def __init__(self, habit: str, day: str, mood: str = '', notes: str = ''):
        """
        Initialize the Record.

        Args:
            habit (str): name of the habit
            day (str): date of completion in the 'dd-mm-yyyy' format
            mood (str, optional): user's mood. The default value is empty
            notes (str, optional): additional notes. They are empty by default

        Returns:
            None
        """
        self.record_id = str(uuid4())
        self.habit = habit
        self.day = datetime.strptime(day, '%d-%m-%Y').date()
        self.mood = mood
        self.notes = notes

    def update_mood(self, users_mood: str) -> None:
        """
        Update the user's mood in a specific record.

        Args:
            users_mood (str): some text information about user's state and mood

        Returns:
            None
        """
        self.mood = users_mood

    def update_notes(self, users_notes: str) -> None:
        """
        Provide with an opportunity to write some notes after the fulfillment of the habit.

        Args:
            users_notes (str): some extra information that the user want to share

        Returns:
            None
        """
        self.notes = users_notes

    def __str__(self) -> str:
        """
        Convert an instance of the Record class to a string.

        Returns:
            str: formatted string containing all the existing information
        """
        return (
            f'ID: {self.record_id}\nHabit Name: {self.habit}\nDate: {self.day}\nMood: {self.mood}\nNotes: {self.notes}'
        )
