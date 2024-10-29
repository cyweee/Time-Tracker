import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QDesktopWidget, QInputDialog
from PyQt5.QtCore import Qt
from datetime import datetime, timedelta


class TimeTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Time Tracker")
        self.setFixedSize(600, 600)
        self.center()
        self.setStyleSheet("background-color: #283747;")

        # Словарь для хранения активностей и их времени
        self.activity_timers = {}
        self.activities = ["Учеба", "Дз", "Отдых", "Другое"]  # Список активностей

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Создание кнопок для каждой активности
        for activity in self.activities:
            button = QPushButton(activity)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #4B4B4B;
                    color: #A9A9A9;
                    font-size: 16px;
                    border: none;
                    border-radius: 10px;
                    padding: 10px;
                    margin: 5px;
                }
                QPushButton:hover { background-color: #5B5B5B; }
            """)
            button.clicked.connect(self.start_activity)  # Привязка события
            button.setCursor(Qt.PointingHandCursor)
            button.setFixedHeight(50)
            button.setMinimumWidth(200)
            layout.addWidget(button)

        # Кнопка "Завершить активность"
        self.stop_button = QPushButton("Завершить активность")
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #A93226;
                color: #FFFFFF;
                font-size: 16px;
                border: none;
                border-radius: 10px;
                padding: 10px;
                margin: 5px;
            }
            QPushButton:hover { background-color: #CB4335; }
        """)
        self.stop_button.clicked.connect(self.stop_last_activity)
        self.stop_button.setCursor(Qt.PointingHandCursor)
        self.stop_button.setFixedHeight(50)
        self.stop_button.setMinimumWidth(200)
        layout.addWidget(self.stop_button)

    def start_activity(self):
        button = self.sender()
        activity_name = button.text()

        # Запрашиваем заметку у пользователя
        note, ok = QInputDialog.getText(self, "Введите заметку", "Заметка для активности:")

        if ok:
            # Запускаем активность
            start_time = datetime.now()
            self.activity_timers[activity_name] = {
                'start': start_time,
                'note': note
            }
            print(f"Начата активность: {activity_name} в {start_time.strftime('%H:%M:%S')} с заметкой: {note}")

    def stop_activity(self, activity_name):
        # Получаем время окончания активности
        end_time = datetime.now()
        activity_data = self.activity_timers.pop(activity_name, None)

        if activity_data:
            duration = end_time - activity_data['start']
            note = activity_data['note']
            print(f"Активность '{activity_name}' завершена. Длительность: {duration}. Заметка: {note}")

            # Сохраняем данные активности, если длительность >= 10 секунд
            if duration >= timedelta(seconds=10):
                self.save_to_json()  # Сохраняем данные после завершения активности
            else:
                print(f"Активность '{activity_name}' была слишком короткой для сохранения.")
        else:
            print(f"Активность '{activity_name}' не найдена.")

    def stop_last_activity(self):
        # Завершает последнюю активную активность
        if self.activity_timers:
            last_activity = next(iter(self.activity_timers))  # Получаем имя первой активной активности
            self.stop_activity(last_activity)
        else:
            print("Нет активных действий для завершения.")

    def save_to_json(self):
        # Создание структуры данных для сохранения
        activities_to_save = []
        for activity_name in self.activities:
            if activity_name in self.activity_timers:
                # Если активность активна, получаем её данные
                activity_data = self.activity_timers[activity_name]
                start_time = activity_data['start'].isoformat()
                end_time = None  # Конечное время отсутствует
                duration = None  # Продолжительность отсутствует
                note = activity_data['note']
            else:
                # Если активность не активна, заполняем пустыми значениями
                start_time = None
                end_time = None
                duration = None
                note = ""

            activities_to_save.append({
                'name': activity_name,
                'start': start_time,
                'end': end_time,
                'duration': duration,
                'note': note
            })

        # Сохраняем данные в файл JSON
        try:
            with open('activities.json', 'w', encoding='utf-8') as f:
                json.dump({"activities": activities_to_save}, f, ensure_ascii=False, indent=4)
            print("Данные сохранены в activities.json")
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")

    def center(self):
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimeTrackerApp()
    window.show()

    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        pass
