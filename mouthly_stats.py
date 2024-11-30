import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Перевод текста
translations = {
    "ru": {
        "title": "Распределение времени по категориям за месяц",
        "x_label": "День месяца",
        "y_label": "Часы",
        "categories": {
            "study": "Учеба",
            "homework": "Дз",
            "relax": "Отдых",
            "other": "Другое"
        },
    },
    "en": {
        "title": "Time Distribution by Categories (Monthly)",
        "x_label": "Day of the Month",
        "y_label": "Hours",
        "categories": {
            "study": "Study",
            "homework": "Homework",
            "relax": "Relax",
            "other": "Other"
        },
    }
}

def read_activities(file_path):
    """Чтение данных из файла activities.json."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)["activities"]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def process_monthly_data(activities, category_keys):
    """Группировка данных за месяц по дням."""
    time_data = {key: [0] * 31 for key in category_keys}  # 31 день
    for activity in activities:
        name = activity["name"]
        start = activity.get("start")
        end = activity.get("end")

        if name in category_keys and start and end:
            start_time = datetime.fromisoformat(start)
            end_time = datetime.fromisoformat(end)
            duration_hours = (end_time - start_time).total_seconds() / 3600

            day_of_month = start_time.day - 1
            time_data[name][day_of_month] += duration_hours

    return time_data

def plot_monthly_statistics(time_data, language="ru"):
    """Построение графика за месяц."""
    lang_data = translations[language]
    title = lang_data["title"]
    categories = lang_data["categories"]
    days = [str(i + 1) for i in range(31)]

    category_keys = list(categories.keys())
    translated_categories = [categories[key] for key in category_keys]

    total_time_per_category = [sum(time_data[key]) for key in category_keys]
    total_time = sum(total_time_per_category)
    percentage_distribution = [
        (time / total_time) * 100 if total_time > 0 else 0 for time in total_time_per_category
    ]

    fig, ax = plt.subplots(2, 1, figsize=(14, 8), gridspec_kw={'height_ratios': [4, 1]})

    # Верхняя часть: по дням
    bottom_values = [0] * 31
    for i, category in enumerate(category_keys):
        ax[0].bar(
            days,
            time_data[category],
            bottom=bottom_values,
            label=f"{translated_categories[i]} ({round(percentage_distribution[i], 1)}%)"
        )
        bottom_values = [bottom_values[j] + time_data[category][j] for j in range(31)]

    ax[0].set_title(title)
    ax[0].set_xlabel(lang_data["x_label"])
    ax[0].set_ylabel(lang_data["y_label"])
    ax[0].legend()
    ax[0].grid(axis='y')

    # Нижняя часть: процентное распределение
    ax[1].bar(
        translated_categories,
        percentage_distribution,
        color=[plt.cm.tab10(i / len(category_keys)) for i in range(len(category_keys))]
    )
    ax[1].set_ylabel("%")
    ax[1].set_ylim(0, 100)
    ax[1].grid(axis='y')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    activities = read_activities("activities.json")
    category_keys = ["study", "homework", "relax", "other"]

    # Фильтрация данных за текущий месяц
    today = datetime.today()
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    monthly_activities = [
        activity for activity in activities
        if start_of_month <= datetime.fromisoformat(activity["start"]) <= end_of_month
    ]

    # Обработка данных
    time_data = process_monthly_data(monthly_activities, category_keys)

    # Построение графика
    plot_monthly_statistics(time_data, language="ru")