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

        # Storing activities and their times
        self.activity_timers = {}

        # Language support
        self.languages = {
            "ru": {
                "Учеба": "Study",
                "Дз": "Homework",
                "Отдых": "Relax",
                "Другое": "Other",
                "Завершить активность": "Stop Activity",
                "Введите заметку": "Enter Note",
                "Заметка для активности:": "Note for Activity:",
                "Нет активных действий для завершения.": "No active activities to stop.",
                "Данные сохранены в activities.json": "Data saved to activities.json",
                "Ошибка при сохранении данных:": "Error saving data:",
                "Начата активность:": "Started activity:",
                "Активность завершена. Длительность:": "Activity completed. Duration:",
                "Заметка:": "Note:",
                "была слишком короткой для сохранения.": "was too short to save."
            },
            "en": {
                "Study": "Учеба",
                "Homework": "Дз",
                "Relax": "Отдых",
                "Other": "Другое",
                "Stop Activity": "Завершить активность",
                "Enter Note": "Введите заметку",
                "Note for Activity:": "Заметка для активности:",
                "No active activities to stop.": "Нет активных действий для завершения.",
                "Data saved to activities.json": "Данные сохранены в activities.json",
                "Error saving data:": "Ошибка при сохранении данных:",
                "Started activity:": "Начата активность:",
                "Activity completed. Duration:": "Активность завершена. Длительность:",
                "Note:": "Заметка:",
                "was too short to save.": "была слишком короткой для сохранения."
            }
        }
        self.current_language = "ru"
        self.activities = ["Учеба", "Дз", "Отдых", "Другое"]

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        self.buttons = {}
        self.create_activity_buttons()

        self.stop_button = QPushButton(self.tr("Завершить активность"))
        self.style_button(self.stop_button, "#A93226", "#CB4335")
        self.stop_button.clicked.connect(self.stop_last_activity)
        self.layout.addWidget(self.stop_button)

        self.language_button = QPushButton("Switch Language")
        self.language_button.setStyleSheet("""
            QPushButton {
                background-color: #2874A6;
                color: #FFFFFF;
                font-size: 14px;
                border: none;
                border-radius: 10px;
                padding: 6px;
                margin: 5px;
            }
            QPushButton:hover { background-color: #3498DB; }
        """)
        self.language_button.setFixedHeight(40)  # Height of the button is smaller
        self.language_button.setMinimumWidth(150)  # Button width is smaller

        self.language_button.clicked.connect(self.switch_language)
        self.layout.addWidget(self.language_button)

    def tr(self, text):
        """Перевод текста на текущий язык."""
        return self.languages[self.current_language].get(text, text)

    def create_activity_buttons(self):
        for activity in self.activities:
            button = QPushButton(self.tr(activity))
            self.style_button(button, "#4B4B4B", "#5B5B5B")
            button.clicked.connect(self.start_activity)
            self.layout.addWidget(button)
            self.buttons[activity] = button

    def style_button(self, button, color, hover_color):
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: #A9A9A9;
                font-size: 16px;
                border: none;
                border-radius: 10px;
                padding: 10px;
                margin: 5px;
            }}
            QPushButton:hover {{ background-color: {hover_color}; }}
        """)
        button.setCursor(Qt.PointingHandCursor)
        button.setFixedHeight(50)
        button.setMinimumWidth(200)

    def switch_language(self):
        self.current_language = "en" if self.current_language == "ru" else "ru"
        self.update_ui_language()

    def update_ui_language(self):
        for activity, button in self.buttons.items():
            button.setText(self.tr(activity))
        self.stop_button.setText(self.tr("Завершить активность"))

    def start_activity(self):
        button = self.sender()
        activity_name = button.text()

        note, ok = QInputDialog.getText(self, self.tr("Введите заметку"), self.tr("Заметка для активности:"))
        if ok:
            start_time = datetime.now()
            self.activity_timers[activity_name] = {
                'start': start_time,
                'note': note
            }
            print(f"{self.tr('Начата активность:')} {activity_name} {start_time.strftime('%H:%M:%S')} {self.tr('с заметкой:')} {note}")

    def stop_activity(self, activity_name):
        end_time = datetime.now()
        activity_data = self.activity_timers.pop(activity_name, None)

        if activity_data:
            duration = end_time - activity_data['start']
            note = activity_data['note']
            print(f"{self.tr('Активность завершена. Длительность:')} {duration}. {self.tr('Заметка:')} {note}")

            if duration >= timedelta(seconds=10):
                self.save_to_json(activity_name, activity_data['start'], end_time, duration, note)
            else:
                print(f"{activity_name} {self.tr('была слишком короткой для сохранения.')}")
        else:
            print(self.tr(f"Активность '{activity_name}' не найдена."))

    def stop_last_activity(self):
        if self.activity_timers:
            last_activity = next(iter(self.activity_timers))
            self.stop_activity(last_activity)
        else:
            print(self.tr("Нет активных действий для завершения."))

    def save_to_json(self, activity_name, start_time, end_time, duration, note):
        try:
            with open('activities.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"activities": []}

        updated = False
        for activity in data["activities"]:
            if activity["name"] == activity_name:
                activity.update({
                    "start": start_time.isoformat(),
                    "end": end_time.isoformat(),
                    "duration": str(duration),
                    "note": note
                })
                updated = True
                break

        if not updated:
            data["activities"].append({
                "name": activity_name,
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
                "duration": str(duration),
                "note": note
            })

        try:
            with open('activities.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(self.tr("Данные сохранены в activities.json"))
        except Exception as e:
            print(f"{self.tr('Ошибка при сохранении данных:')} {e}")

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
