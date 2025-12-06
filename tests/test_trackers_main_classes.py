from datetime import date
from src.habit_tracker.trackers_main_classes import User, Habit, Record

def test_user_add_habit():
    user = User('Иван')
    habit = Habit('Плавание', 'каждый день', '01-11-2025', '30-11-2025', 'Иван')
    user.add_habit(habit)
    assert habit in user.user_habits

def test_user_remove_habit():
    user = User('Иван')
    habit = Habit('Плавание', 'каждый день', '01-11-2025', '30-11-2025','Иван')
    user.add_habit(habit)
    user.remove_habit(habit)
    assert habit not in user.user_habits

def test_habit_is_completed():
    habit = Habit('Чтение', 'каждый день', '01-11-2025', '30-11-2025','Иван')
    habit.completion_mark('01-11-2025')
    assert habit.is_complited('01-11-2025') is True
    assert habit.is_complited('01-10-2025') is False

def test_habit_completion_mark():
    habit = Habit('Чтение', 'каждый день', '01-11-2025', '30-11-2025','Иван')
    habit.completion_mark('01-11-2025')
    assert date(2025, 11, 1) in habit.completed_days

def test_habit_total_period():
    habit = Habit('Чтение', 'каждый день', '01-11-2025', '30-11-2025','Иван')
    assert habit.total_period() == 30

def test_habit_completion_rate():
    habit = Habit('Чтение', 'каждый день', '01-11-2025', '30-11-2025','Иван')
    habit.completion_mark('05-11-2025')
    assert habit.completion_rate() == 3.33

def test_record_update_mood():
    habit = Habit('Чтение', 'каждый день', '01-11-2025', '30-11-2025', 'Иван')
    record = Record(habit, '30-11-2025')
    record.update_mood('Все хорошо, читаю с удовольствием')
    assert record.mood == 'Все хорошо, читаю с удовольствием'

def test_record_update_notes():
    habit = Habit('Чтение', 'каждый день', '01-11-2025', '30-11-2025', 'Иван')
    record = Record(habit, '30-11-2025')
    record.update_notes('Книга интересная')
    assert record.notes == 'Книга интересная'