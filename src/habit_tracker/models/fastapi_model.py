import sqlite3
import uuid
from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.habit_tracker.motivation.motivation import Motivation
from src.habit_tracker.trackers_main_classes import Habit, Record, User

app = FastAPI()

users = {}
habits = []
records = set()


def db_connect():
    """
    Connect database with fastapi.

    Returns:
        str: connection
    """
    db_path = 'src/habit_tracker/models/habits.db'
    return sqlite3.connect(db_path)


@app.get('/')
async def root() -> dict[str, str]:
    """Send the greeting message.

    Returns:
        dict[str, str]: greeting message for the user
    """
    motivation = Motivation()
    quote = motivation.give_random_quote()

    return {'message': 'Привет! Расскажи о привычках, которые ты хочешь соблюдать', 'motivational_quote': quote}


@app.post('/users/')
async def register_user(name: str) -> dict[str, str]:
    """Register a new user.

    Args:
        name (str): name of the user

    Returns:
        dict[str, str]: message that the user was registered
    """
    user = User(name=name)
    users[user.user_id] = user

    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users VALUES (?, ?)', (user.user_id, user.user_name))
        conn.commit()

    return {
        'user_id': user.user_id,
        'message': f'Пользователь {user.user_name} зарегистрирован. Скопируй и сохрани id. Он еще пригодится',
    }


@app.post('/users/{user_id}/habits/')
async def add_habit(user_id: str, habits_name: str, freq: str, start_day: str, end_day: str) -> dict[str, str]:
    """Add a new habit to the user.

    Args:
        user_id (str): unique id of the user
        habits_name (str): name of the habit
        freq (str): the frequency of the habit fulfillment
        start_day (str): the first day of the habit
        end_day (str): the last day of the habit

    Returns:
        dict[str, str]: message that the habit was added to the user
    """
    try:
        user = users.get(user_id)
        if user is None:
            return JSONResponse(content={'message': 'Пользователь не найден'}, status_code=404)

        habit = Habit(name=habits_name, freq=freq, start_day=start_day, end_day=end_day, user_id=user_id)
        user.add_habit(habit)
        habits.append(habit)

        with db_connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?)',
                (habit.habit_id, habit.habit_name, habit.frequency, habit.start_day, habit.end_day, habit.user_id),
            )
            conn.commit()

        return {'message': f"Новая привычка '{habits_name}' создана для пользователя {user.user_name}"}

    except Exception as e:
        return JSONResponse(content={'message': f'Внутренняя ошибка сервера: {e!s}'}, status_code=500)


@app.delete('/users/{user_id}/habits/{habit_name}')
async def delete_habit(user_id: str, habit_name: str) -> dict[str, str]:
    """Remove the habit from the user.

    Args:
        user_id (str): unique identifier of the user
        habit_name (str): name of the habit to remove

    Returns:
        dict[str, str]: message that the habit is removed
    """
    user = users.get(user_id)
    if user is None:
        return JSONResponse(content={'message': 'Пользователь не найден'}, status_code=404)

    user.remove_habit(habit_name)

    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM habits WHERE title=? AND user_id=?', (habit_name, user_id))
        conn.commit()

    return {'message': f"Привычка '{habit_name}' удалена у пользователя {user.user_name}"}


@app.get('/habits/{habit_name}/check/{day}')
async def check_habit_completion(habit_name: str, day: str) -> bool:
    """
    Check whether the habit is marked as completed on the specified date.

    Args:
        habit_name (str): name of the habit
        day (str): the day of verification in the 'dd-mm-yyyy' format

    Returns:
        bool: True if the habit was completed on the specified date, otherwise False
    """
    habit = next((h for h in habits if h.habit_name == habit_name), None)
    if habit is None:
        return JSONResponse(content={'message': 'Привычка не найдена'}, status_code=404)
    return habit.is_complited(day)


@app.post('/habits/{habit_name}/mark/{day}')
async def mark_habit_completion(habit_name: str, day: str) -> dict[str, str]:
    """
    Record the fulfillment of a habit on a specified date.

    Args:
        habit_name (str): name of the habit
        day (str): the day of fulfillment in the 'dd-mm-yyyy' format

    Returns:
        dict[str, str]: message that the habit was fixed
    """
    habit = next((h for h in habits if h.habit_name == habit_name), None)
    if habit is None:
        return JSONResponse(content={'message': 'Привычка не найдена'}, status_code=404)
    habit.completion_mark(day)

    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO records VALUES (?, ?, NULL, NULL, ?)',
            (uuid.uuid4().hex[:8], day, habit.habit_id),
        )
        conn.commit()

    return {'message': f"Привычка '{habit_name}' зафиксирована как выполненная на {day}"}


@app.get('/habits/{habit_name}/rate')
async def get_habit_completion_rate(habit_name: str) -> dict[str, str]:
    """
    Count the habit fulfillment percentage.

    Args:
        habit_name (str): name of the habit

    Returns:
        dict[str, str]: message with the percentage of the fulfillment
    """
    habit = next((h for h in habits if h.habit_name == habit_name), None)
    if habit is None:
        return JSONResponse(content={'message': 'Привычка не найдена'}, status_code=404)
    rate_value = habit.completion_rate()
    return {'message': f"Процент выполнения привычки '{habit_name}' составляет {rate_value}%"}


@app.post('/habits/{habit_name}/records/')
async def create_record(habit_name: str, day: str, mood: str = '', notes: str = '') -> dict[str, str]:
    """
    Create a new record for a habit.

    Args:
        habit_name (str): the name of the habit
        day (str): date of completion in the 'dd-mm-yyyy' format
        mood (str, optional): user's mood. Default is empty.
        notes (str, optional): additional notes. Default is empty.

    Returns:
        dict[str, str]: JSON response with success or error message
    """
    habit = next((h for h in habits if h.habit_name == habit_name), None)
    if habit is None:
        return {'message': 'Привычка не найдена'}

    try:
        parsed_day = datetime.strptime(day, '%d-%m-%Y').date()
    except ValueError:
        return {'message': "Ошибка: Дата указана в неверном формате. Используйте формат 'DD-MM-YYYY'."}

    record = Record(habit=habit, day=parsed_day, mood=mood, notes=notes)

    if not hasattr(habit, 'records'):
        habit.records = []
    habit.records.append(record)

    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO records VALUES (?, ?, ?, ?, ?)',
            (record.record_id, parsed_day, mood, notes, habit.habit_id),
        )
        conn.commit()

    return {
        'message': f"Запись о выполнении привычки '{habit_name}' создана успешно. "
        f'Скопируй и сохрани id, он еще пригодится',
        'record_id': record.record_id,
        'date': parsed_day.strftime('%d-%m-%Y'),
    }


@app.post('/habits/{habit_name}/records/{record_id}/mood')
async def update_record_mood(habit_name: str, record_id: str, mood: str = '') -> dict[str, str]:
    """Update mood.

    Args:
        habit_name (str): the name of the habit
        record_id (str): id of the record
        mood (str, optional): user's mood. The default value is empty

    Returns:
        dict[str, str]: message that mood was updated
    """
    habit = next((h for h in habits if h.habit_name == habit_name), None)
    if habit is None:
        return {'message': 'Привычка не найдена'}

    record = next((r for r in habit.records if r.record_id == record_id), None)
    if record is None:
        return {'message': 'Запись не найдена'}

    record.update_mood(mood)

    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE records SET mood=? WHERE id=? AND habit_id=?',
            (mood, record_id, habit.habit_id),
        )
        conn.commit()

    return {'message': f"Настроение в записи '{record_id}' обновлено"}


@app.post('/habits/{habit_name}/records/{record_id}/notes')
async def update_record_notes(habit_name: str, record_id: str, notes: str = '') -> dict[str, str]:
    """Update notes.

    Args:
        habit_name (str): the name of the habit
        record_id (str): id of the record
        notes (str, optional): additional notes. They are empty by default

    Returns:
        dict[str, str]: message that notes were updated
    """
    habit = next((h for h in habits if h.habit_name == habit_name), None)
    if habit is None:
        return {'message': 'Привычка не найдена'}

    record = next((r for r in habit.records if r.record_id == record_id), None)
    if record is None:
        return {'message': 'Запись не найдена'}

    record.update_notes(notes)

    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE records SET notes=? WHERE id=? AND habit_id=?',
            (notes, record_id, habit.habit_id),
        )
        conn.commit()

    return {'message': f"Заметки в записи '{record_id}' обновлены"}


@app.get('/users/')
async def get_all_users() -> list:
    """Get all users from the database.

    Returns:
        list: list of all users
    """
    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        return cursor.fetchall()


@app.get('/habits/')
async def get_all_habits() -> list:
    """Get all habits from the database.

    Returns:
        list: list of all habits
    """
    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM habits')
        return cursor.fetchall()


@app.get('/records/')
async def get_all_records() -> list:
    """Get all records from the database.

    Returns:
        list: list of all records
    """
    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM records')
        return cursor.fetchall()
