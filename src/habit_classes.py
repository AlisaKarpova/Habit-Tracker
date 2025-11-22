from uuid import uuid4
from datetime import datetime


class User:
    def __init__(self, name: str, id=None):
        self.user_name = name
        self.user_id = id or str(uuid4())
        self.user_habits = set()

    def add_habit(self, habit: str):
        self.user_habits.add(habit)

    def remove_habit(self, habit_to_remove: str):
        if habit_to_remove in self.user_habits:
            self.user_habits.remove(habit_to_remove)

    def habits(self):
        return self.user_habits


class Habit:
    def __init__(self, name: str, frequency: str,
                 start_day: str, end_day: str):
        self.habit_name = name
        self.frequency = frequency
        self.start_day = datetime.strptime(start_day, "%d-%m-%Y").date()
        self.end_day = datetime.strptime(end_day, "%d-%m-%Y").date()
        self.completed_days = []

    def is_complited(self, day: str):
        target_day = datetime.strptime(day, "%d-%m-%Y").date()
        return target_day in self.completed_days

    def completion_mark(self, day: str):
        target_day = datetime.strptime(day, "%d-%m-%Y").date()
        if self.end_day >= target_day >= self.start_day:
            self.completed_days.append(target_day)

    def total_period(self):
        return (self.end_day - self.start_day).days + 1

    def completion_rate(self):
        total_days = self.total_period()
        completed_count = len(self.completed_days)
        return round((completed_count / total_days) * 100, 2) if total_days > 0 else 0


class Record:
    def __init__(self, habit: str, day: str, mood="", notes=""):
        self.record_id = str(uuid4())
        self.habit = habit
        self.day = datetime.strptime(day, "%d-%m-%Y").date()
        self.mood = mood
        self.notes = notes

    def update_mood(self, users_mood: str):
        self.mood = users_mood

    def update_notes(self, users_notes: str):
        self.notes = users_notes

    def __str__(self):
        return (
            f"ID: {self.record_id}\n"
            f"Habit Name: {self.habit.habit_name}\n"
            f"Date: {self.day}\n"
            f"Mood: {self.mood}\n"
            f"Notes: {self.notes}"
        )
