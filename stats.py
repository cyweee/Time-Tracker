import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Translation dictionary for the chart
translations = {
    "ru": {
        "title": "Распределение времени по категориям",
        "x_label": "День недели",
        "y_label": "Часы",
        "categories": ["Учеба", "Дз", "Отдых", "Другое"],
        "days": ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
    },
    "en": {
        "title": "Time Distribution by Categories",
        "x_label": "Day of the Week",
        "y_label": "Hours",
        "categories": ["Study", "Homework", "Relax", "Other"],
        "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    }
}

def read_and_process_json(file_path):
    """Считывание JSON и обработка данных."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Creating a dictionary to store time by weekdays and categories
    categories = ["Учеба", "Дз", "Отдых", "Другое"]
    time_data = {cat: [0] * 7 for cat in categories}  # 7 дней недели

    for activity in data["activities"]:
        name = activity["name"]
        start = activity.get("start")
        end = activity.get("end")

        if name in categories and start and end:
            # Duration calculation
            start_time = datetime.fromisoformat(start)
            end_time = datetime.fromisoformat(end)
            duration = end_time - start_time

            # Convert duration to hours
            duration_hours = duration.total_seconds() / 3600

            # Definition of the day of the week (0 = Mon, 6 = Sun)
            day_of_week = start_time.weekday()

            # Adding time to the appropriate category and day
            time_data[name][day_of_week] += duration_hours

    return time_data

def plot_statistics(time_data, language="ru"):
    """Построение графика на основе данных и языка."""
    lang_data = translations[language]
    title = lang_data["title"]
    x_label = lang_data["x_label"]
    y_label = lang_data["y_label"]
    categories = lang_data["categories"]
    days = lang_data["days"]

    # Plotting a graph
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.2  # Ширина столбцов
    x_indexes = range(len(days))

    # Drawing columns for each category
    for i, category in enumerate(categories):
        ax.bar(
            [x + i * bar_width for x in x_indexes],  # Смещение столбцов
            time_data.get(category, [0] * 7),
            width=bar_width,
            label=category
        )

    # Customizing the chart
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xticks([x + bar_width * (len(categories) / 2 - 0.5) for x in x_indexes])
    ax.set_xticklabels(days)
    ax.legend()

    plt.show()

if __name__ == "__main__":
    # Example of usage
    file_path = "activities.json"
    current_language = "ru"  # Current interface language (“ru” or “en”)

    time_data = read_and_process_json(file_path)
    plot_statistics(time_data, language=current_language)
