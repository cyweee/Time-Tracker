import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# func for loading data from JSON
def load_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("activities", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка загрузки данных: {e}")
        return []

# func for calculating activity duration in hours
def calculate_durations(activities):
    durations_by_day = {"ПН": {}, "ВТ": {}, "СР": {}, "ЧТ": {}, "ПТ": {}, "СБ": {}, "ВС": {}}

    for entry in activities:
        name = entry["name"]
        start_str = entry["start"]
        end_str = entry["end"]

        if start_str and end_str:
            # convert strings to datetime objects
            start = datetime.fromisoformat(start_str)
            end = datetime.fromisoformat(end_str)
            duration_hours = (end - start).total_seconds() / 3600

            # define day of week
            day_of_week = start.strftime("%a").upper()
            if day_of_week in durations_by_day:
                if name not in durations_by_day[day_of_week]:
                    durations_by_day[day_of_week][name] = 0
                durations_by_day[day_of_week][name] += duration_hours

    return durations_by_day

# loading data and calculating durations
data = load_data('activities.json')
durations_by_day = calculate_durations(data)

# parameters for drawing a graph
days = list(durations_by_day.keys())
activities = ["Учеба", "Дз", "Отдых", "Другое"]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#8c564b']  # Цвета для категорий

# convert data into arrays
values = []
for day in days:
    values.append([durations_by_day[day].get(activity, 0) for activity in activities])

values = np.array(values)

# building a chart
fig, ax = plt.subplots(figsize=(10, 6))

# sum the values for each category to create stacks
bottom = np.zeros(len(days))
for i, activity in enumerate(activities):
    ax.bar(days, values[:, i], label=activity, color=colors[i], bottom=bottom)
    bottom += values[:, i]

# chart settings
ax.set_xlabel('День недели')
ax.set_ylabel('Часы')
ax.set_title('Распределение времени по категориям')
ax.legend(activities, bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()