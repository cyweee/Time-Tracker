import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

# Translation dictionary for the chart
translations = {
    "ru": {
        "title": "Распределение времени по категориям",
        "x_label": "День недели",
        "y_label": "Часы",
        "categories": {
            "study": "Учеба",
            "homework": "Дз",
            "relax": "Отдых",
            "other": "Другое"
        },
        "days": ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
    },
    "en": {
        "title": "Time Distribution by Categories",
        "x_label": "Day of the Week",
        "y_label": "Hours",
        "categories": {
            "study": "Study",
            "homework": "Homework",
            "relax": "Relax",
            "other": "Other"
        },
        "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    }
}

def read_and_process_json(file_path, category_keys):
    """Считывание JSON и обработка данных."""
    if not os.path.exists(file_path):
        # Если файла нет, создаем пустую структуру
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({"activities": []}, f, ensure_ascii=False, indent=4)
        print(f"Created new file: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # create a dictionary to store time by day of the week and category
    time_data = {key: [0] * 7 for key in category_keys}  # 7 дней недели

    for activity in data["activities"]:
        name = activity["name"]
        start = activity.get("start")
        end = activity.get("end")

        if name in category_keys and start and end:
            # duration calculation
            start_time = datetime.fromisoformat(start)
            end_time = datetime.fromisoformat(end)
            duration = end_time - start_time

            # convert duration to hours
            duration_hours = duration.total_seconds() / 3600

            # define day of week (0 = Monday, 6 = Sunday)
            day_of_week = start_time.weekday()

            # add time to the appropriate category and day
            time_data[name][day_of_week] += duration_hours

    return time_data

def plot_statistics(time_data, language="ru", output_file=None):
    """Построение графика на основе данных и языка."""
    lang_data = translations[language]
    title = lang_data["title"]
    x_label = lang_data["x_label"]
    y_label = lang_data["y_label"]
    categories = lang_data["categories"]
    days = lang_data["days"]

    # preparing data for plotting
    category_keys = list(categories.keys())
    translated_categories = [categories[key] for key in category_keys]

    # plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.2  # Ширина столбцов
    x_indexes = range(len(days))

    # Построение столбцов для каждой категории
    for i, category in enumerate(category_keys):
        ax.bar(
            [x + i * bar_width for x in x_indexes],
            time_data.get(category, [0] * 7),
            width=bar_width,
            label=translated_categories[i]
        )

    # Настройка графика
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xticks([x + bar_width * (len(category_keys) / 2 - 0.5) for x in x_indexes])
    ax.set_xticklabels(days)
    ax.legend()

    # storing the graph if a file for output is specified
    if output_file:
        fig.savefig(output_file, dpi=300, bbox_inches='tight', transparent=True)
        print(f"Graph saved to {output_file}")
    else:
        plt.show()

def clear_old_data(file_path):
    """Очищает данные для новой недели."""
    if os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({"activities": []}, f, ensure_ascii=False, indent=4)
        print(f"Cleared data in {file_path}")
    else:
        print(f"File {file_path} does not exist. No data to clear.")

if __name__ == "__main__":
    # path to json
    file_path = "activities.json"

    # current language
    current_language = "ru"

    # category keys
    category_keys = ["study", "homework", "relax", "other"]

    # output file (None если не нужно сохранять)
    output_file = "doc/img/your_stats.png"

    # Получение текущего дня недели
    current_day = datetime.now().weekday()  # 0 = ПН, 6 = ВС

    # Чтение и обработка данных
    time_data = read_and_process_json(file_path, category_keys)

    # Построение графика на основе текущей недели
    plot_statistics(time_data, language=current_language, output_file=output_file)

    # Если сегодня воскресенье, очищаем данные
    if current_day == 6:  # 6 = Sunday
        clear_old_data(file_path)
    else:
        print("Данные за текущую неделю визуализированы. Очистка произойдёт в ближайшее воскресенье.")