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
                "study": "Учеба",
                "homework": "Дз",
                "relax": "Отдых",
                "other": "Другое",
                "Stop Activity": "Завершить активность",
                "Enter Note": "Введите заметку",
                "Note for Activity:": "Заметка для активности:",
                "No active activities to stop.": "Нет активных действий для завершения.",
                "Data saved to activities.json": "Данные сохранены в activities.json",
                "Error saving data:": "Ошибка при сохранении данных:",
                "Started activity:": "Начата активность:",
                "Activity completed. Duration:": "Активность завершена. Длительность:",
                "Note:": "Заметка:",
                "was too short to save.": "была слишком короткой для сохранения.",
                "Show Weekly Data": "Показать данные за неделю",
                "Show Monthly Data": "Показать данные за месяц",
            },
            "en": {
                "study": "Study",
                "homework": "Homework",
                "relax": "Relax",
                "other": "Other",
                "Stop Activity": "Stop Activity",
                "Enter Note": "Enter Note",
                "Note for Activity:": "Note for Activity:",
                "No active activities to stop.": "No active activities to stop.",
                "Data saved to activities.json": "Data saved to activities.json",
                "Error saving data:": "Error saving data:",
                "Started activity:": "Started activity:",
                "Activity completed. Duration:": "Activity completed. Duration:",
                "Note:": "Note:",
                "was too short to save.": "was too short to save.",
                "Show Weekly Data": "Show Weekly Data",
                "Show Monthly Data": "Show Monthly Data",
            }
        }
        self.current_language = "ru"
        self.activity_keys = ["study", "homework", "relax", "other"]

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        self.buttons = {}
        self.create_activity_buttons()

        # Create the stop button
        self.stop_button = QPushButton(self.tr("Stop Activity"))
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #A93226;
                color: #FFFFFF;
                font-size: 18px;
                border: none;
                border-radius: 10px;
                padding: 10px;
                margin: 5px;
            }
            QPushButton:disabled {
                background-color: #450303;
                color: #474545;
            }
            QPushButton:hover:!disabled {
                background-color: #CB4335;
            }
        """)
        self.stop_button.clicked.connect(self.stop_last_activity)
        self.stop_button.setEnabled(False)  # Initially disabled
        self.layout.addWidget(self.stop_button)

        # Create the language switch button
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
        self.language_button.setFixedHeight(40)
        self.language_button.setMinimumWidth(150)
        self.language_button.clicked.connect(self.switch_language)
        self.layout.addWidget(self.language_button)

        # Create the week and month buttons
        self.week_button = QPushButton(self.tr("Show Weekly Data"))
        self.style_button(self.week_button, "#4B4B4B", "#5B5B5B")
        self.week_button.clicked.connect(self.show_week_data)
        self.layout.addWidget(self.week_button)

        self.month_button = QPushButton(self.tr("Show Monthly Data"))
        self.style_button(self.month_button, "#4B4B4B", "#5B5B5B")
        self.month_button.clicked.connect(self.show_month_data)
        self.layout.addWidget(self.month_button)

    def tr(self, text):
        """Перевод текста на текущий язык."""
        return self.languages[self.current_language].get(text, text)

    def localize_categories(self):
        """Возвращает локализованные названия категорий."""
        return [self.tr(key) for key in self.activity_keys]

    def create_activity_buttons(self):
        localized_labels = self.localize_categories()
        for key, label in zip(self.activity_keys, localized_labels):
            button = QPushButton(label)
            self.style_button(button, "#4B4B4B", "#5B5B5B")
            button.clicked.connect(lambda _, k=key: self.start_activity(k))
            self.layout.addWidget(button)
            self.buttons[key] = button

    def style_button(self, button, color, hover_color):
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: #A9A9A9;
                font-size: 18px;
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
        localized_labels = self.localize_categories()
        for key, button in self.buttons.items():
            button.setText(localized_labels[self.activity_keys.index(key)])
        self.stop_button.setText(self.tr("Stop Activity"))
        self.week_button.setText(self.tr("Show Weekly Data"))
        self.month_button.setText(self.tr("Show Monthly Data"))

    def start_activity(self, activity_key):
        if self.activity_timers:
            print(self.tr("There is already an active activity. Please stop it before starting a new one."))
            return

        note, ok = QInputDialog.getText(self, self.tr("Enter Note"), self.tr("Note for Activity:"))
        if ok:
            start_time = datetime.now()
            self.activity_timers[activity_key] = {
                'start': start_time,
                'note': note
            }
            print(f"{self.tr('Started activity:')} {self.tr(activity_key)} {start_time.strftime('%H:%M:%S')} {self.tr('with note:')} {note}")
            self.stop_button.setEnabled(True)

    def stop_activity(self, activity_key):
        end_time = datetime.now()
        activity_data = self.activity_timers.pop(activity_key, None)

        if activity_data:
            duration = end_time - activity_data['start']
            note = activity_data['note']
            print(f"{self.tr('Activity completed. Duration:')} {duration}. {self.tr('Note:')} {note}")

            if duration >= timedelta(seconds=10):
                self.save_to_json(activity_key, activity_data['start'], end_time, duration, note)
            else:
                print(f"{self.tr(activity_key)} {self.tr('was too short to save.')}")
        else:
            print(self.tr("No active activities to stop."))

        if not self.activity_timers:
            self.stop_button.setEnabled(False)

    def stop_last_activity(self):
        if self.activity_timers:
            last_activity = next(iter(self.activity_timers))
            self.stop_activity(last_activity)
        else:
            print(self.tr("No active activities to stop."))

    def save_to_json(self, activity_key, start_time, end_time, duration, note):
        try:
            with open('activities.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"activities": []}

        data["activities"].append({
            "name": activity_key,
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
            "duration": str(duration),
            "note": note
        })

        try:
            with open('activities.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(self.tr("Data saved to activities.json"))
        except Exception as e:
            print(f"{self.tr('Error saving data:')} {e}")

    def filter_activities_by_period(self, file_path, start_date, end_date):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"activities": []}

        activities = data.get("activities", [])
        filtered = []
        for activity in activities:
            # Проверьте, что поле "start" является строкой перед его конвертацией
            if isinstance(activity["start"], str):
                activity_start_date = datetime.fromisoformat(activity["start"]).date()
                if start_date <= activity_start_date <= end_date:
                    filtered.append(activity)
        return filtered
    def get_current_week_data(self):
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        return self.filter_activities_by_period('activities.json', start_of_week.date(), end_of_week.date())

    def get_current_month_data(self):
        today = datetime.today()
        start_of_month = today.replace(day=1)
        next_month = start_of_month + timedelta(days=31)
        end_of_month = next_month.replace(day=1) - timedelta(days=1)
        return self.filter_activities_by_period('activities.json', start_of_month.date(), end_of_month.date())

    def show_week_data(self):
        week_data = self.get_current_week_data()
        print("Weekly Data:")
        print(json.dumps(week_data, ensure_ascii=False, indent=4))

    def show_month_data(self):
        month_data = self.get_current_month_data()
        print("Monthly Data:")
        print(json.dumps(month_data, ensure_ascii=False, indent=4))

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
