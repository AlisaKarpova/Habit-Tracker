import matplotlib.pyplot as plt

from src.habit_tracker.trackers_main_classes import Habit


class GraphicsAnalytics:
    """Plot the completion rate."""

    def __init__(self, habit: Habit):
        """
        Initialize of the GraphicsAnalytics.

        Args:
            habit (Habit): the instance of the Habit class

        Returns:
            None
        """
        self.habit = habit

    def plot_completion_rate(self):
        """
        Plot the pie chart.

        Returns:
            None
        """
        completion_percentage = self.habit.completion_rate()

        labels = ['Выполненные дни', 'Невыполненные дни']
        sizes = [completion_percentage, 100 - completion_percentage]
        colors = ['lightblue', 'lightcoral']

        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title(f'Процент выполнения привычки ({self.habit.habit_name})')
        plt.show()
