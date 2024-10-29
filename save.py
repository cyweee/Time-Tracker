import json
import os
import time
from datetime import datetime

# Путь к файлу для сохранения активностей
SAVE_FILE = 'activities.json'


# Функция для сохранения данных в JSON-файл
def save_data(activities, saved=True):
    data = {
        "saved": saved,
        "timestamp": time.time(),  # Текущее время
        "activities": activities
    }

    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# Функция для загрузки данных из JSON-файла
def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            return json.load(f)
    # Возвращаем пустой список активностей, если файл не существует
    return {
        "saved": False,
        "timestamp": time.time(),  # Устанавливаем текущее время для нового файла
        "activities": []
    }


# Функция для добавления новой активности
def add_activity(name, note=""):
    activity = {
        "name": name,
        "start": None,
        "start_readable": None,
        "note": note
    }
    data = load_data()
    data["activities"].append(activity)
    save_data(data["activities"])


# Функция для обновления активности по индексу
def update_activity(index, new_data):
    data = load_data()
    if index < len(data["activities"]):
        data["activities"][index].update(new_data)
        save_data(data["activities"])


# Пример использования
if __name__ == "__main__":
    activities = load_data()["activities"]

    # Добавление новой активности
    add_activity("Работа", "Задачи на день")

    # Установка времени начала активности
    start_time = time.time()
    start_readable = datetime.fromtimestamp(start_time).strftime("%d.%m.%Y %H:%M:%S")

    update_activity(0, {
        "start": start_time,
        "start_readable": start_readable
    })

    print("Данные сохранены:", load_data())
