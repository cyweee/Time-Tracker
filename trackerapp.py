import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QDesktopWidget
from PyQt5.QtCore import Qt

class TimeTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Time Tracker")
        self.setFixedSize(600, 600)
        self.center()
        self.setStyleSheet("background-color: #283747;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Список активностей
        self.activities = ["Учеба", "Дз", "Отдых", "Другое"]

        # Создание кнопок для каждой активности
        for activity in self.activities:
            button = QPushButton(activity)
            button.setStyleSheet("""
                background-color: #4B4B4B;
                color: #A9A9A9;
                font-size: 16px;
                border: none;
                border-radius: 10px;
                padding: 10px;
                margin: 5px;
                transition: background-color .2s;
            """)
            button.clicked.connect(self.start_activity)  # Привязка события
            button.setCursor(Qt.PointingHandCursor)  # Изменение курсора на указатель
            button.setFixedHeight(50)  # Установка фиксированной высоты кнопки
            button.setMinimumWidth(200)  # Установка минимальной ширины кнопки
            layout.addWidget(button)

            # Добавление эффекта наведения
            button.setStyleSheet(button.styleSheet() + "QPushButton:hover { background-color: #5B5B5B; }")

        # Создание тестовой кнопки
        test_button = QPushButton("Тестовая кнопка")
        test_button.setStyleSheet("""
            background-color: #4B4B4B;
            color: #A9A9A9;
            font-size: 16px;
            border: none;
            border-radius: 10px;
            padding: 10px;
            margin: 5px;
            transition: background-color .2s;
        """)
        test_button.clicked.connect(self.test_button_clicked)  # Привязка события
        test_button.setCursor(Qt.PointingHandCursor)  # Изменение курсора на указатель
        test_button.setFixedHeight(50)  # Установка фиксированной высоты кнопки
        test_button.setMinimumWidth(200)  # Установка минимальной ширины кнопки
        layout.addWidget(test_button)

        # Эффект наведения для тестовой кнопки
        test_button.setStyleSheet(test_button.styleSheet() + "QPushButton:hover { background-color: #5B5B5B; }")

    def start_activity(self):
        button = self.sender()  # Получаем кнопку, которая была нажата
        activity_name = button.text()
        print(f"Начата активность: {activity_name}")  # Временно просто выводим имя активности в консоль

    def test_button_clicked(self):
        print("Тестовая кнопка нажата!")  # Вывод сообщения в консоль

    def center(self):
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimeTrackerApp()
    window.show()
    sys.exit(app.exec_())
