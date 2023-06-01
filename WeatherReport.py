import requests

from PySide6.QtCore import Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit
from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QWidget
from PyQt6 import QtWidgets

API_key = '332a956d69f5d90fb1a571aa6cc9606b'

search = "./assets/searchIcon.svg"

class WeatherReport(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WeatherReport")
        self.resize(600, 600)
        # Установка фона только для WeatherReport.
        self.setStyleSheet("background-color: #edf0fc")  # Установка стиля для фона

        self.city_entry = QLineEdit()
        self.city_entry.setPlaceholderText("Введите город")
        self.city_entry.setStyleSheet("""
        QLineEdit { background-color: white; max-width: 400px; border-radius: 8px; padding: 9px; }
        """)

        self.submit_button = QPushButton()
        self.submit_button.setFixedSize(30, 30)
        self.submit_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        layout = QHBoxLayout(self.submit_button)
        layout.setContentsMargins(0, 0, 0, 0)

        # Создание QSvgWidget и установка его в качестве фона кнопки
        svg_widget = QSvgWidget("assets/searchIcon.svg")
        svg_widget.setGeometry(0, 0, 30, 30)

        layout.addWidget(svg_widget)

        self.city_name = QLabel()
        self.city_name.setStyleSheet("""
                    QLabel {
                        font-size: 45px;
                    }
                """)

        self.temperature_label = QLabel()
        self.temperature_label.setStyleSheet("""
                    QLabel {
                        font-size: 50px;
                    }
                """)
        self.weather_label = QLabel()
        self.humidity_label = QLabel()
        self.pressure_label = QLabel()
        self.wind_speed_label = QLabel()

        self.weather_icon_clouds = QSvgWidget()
        self.weather_icon_clouds.setFixedSize(0, 0)

        self.humidity_icon = QSvgWidget("assets/Humidity.svg")
        self.humidity_icon.setFixedSize(0, 0)

        self.pressure_icon = QSvgWidget("assets/Pressure.svg")
        self.pressure_icon.setFixedSize(0, 0)

        self.wind_icon = QSvgWidget("assets/Wind.svg")
        self.wind_icon.setFixedSize(0, 0)

        weather_search = QHBoxLayout()

        weather_search.addWidget(self.city_entry)
        weather_search.addWidget(self.submit_button)

        city_name_layout = QHBoxLayout()
        city_name_layout.setContentsMargins(0, 20, 0, 0)

        city_name_layout.addWidget(self.city_name)

        weather_main_info = QHBoxLayout()
        weather_main_info.setSpacing(5)

        weather_icon_layout = QVBoxLayout()
        weather_icon_layout.addWidget(self.weather_icon_clouds)
        weather_icon_layout.addWidget(self.weather_label)

        weather_main_info.addLayout(weather_icon_layout)
        weather_main_info.addWidget(self.temperature_label)

        weather_about_info = QHBoxLayout()
        weather_about_info.setSpacing(0)

        humidity_layout = QHBoxLayout()

        humidity_layout.addWidget(self.humidity_icon)
        humidity_layout.addWidget(self.humidity_label)

        pressure_layout = QHBoxLayout()

        pressure_layout.addWidget(self.pressure_icon)
        pressure_layout.addWidget(self.pressure_label)

        wind_layout = QHBoxLayout()

        wind_layout.addWidget(self.wind_icon)
        wind_layout.addWidget(self.wind_speed_label)

        weather_about_info.addLayout(humidity_layout)
        weather_about_info.addLayout(pressure_layout)
        weather_about_info.addLayout(wind_layout)

        layout = QVBoxLayout()

        layout.addLayout(weather_search, 1)
        layout.addLayout(city_name_layout)
        layout.addLayout(weather_main_info, 1)
        layout.addLayout(weather_about_info, 1)

        self.setLayout(layout)

        self.submit_button.clicked.connect(self.show_weather)

    def get_weather(self, city):
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}&units=metric'
        response = requests.get(url)
        weather_data = response.json()
        if weather_data['cod'] != '404':
            city = weather_data['name']
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            pressure = weather_data['main']['pressure']
            weather = weather_data['weather'][0]['main']
            wind_speed = weather_data['wind']['speed']
            return {'temperature': temperature, 'humidity': humidity, 'pressure': pressure,
                    'weather': weather, 'wind_speed': wind_speed, 'city': city}
        else:
            return None

    def show_weather(self):
        city = self.city_entry.text()

        if not city:  # проверка, что строка ввода не пустая
            self.city_name.setText("Город не найден")
            self.city_name.setAlignment(Qt.AlignCenter)
            self.weather_label.clear()
            self.temperature_label.clear()
            self.humidity_label.clear()
            self.pressure_label.clear()
            self.wind_speed_label.clear()
            self.humidity_icon.setFixedSize(0, 0)
            self.pressure_icon.setFixedSize(0, 0)
            self.wind_icon.setFixedSize(0, 0)
            self.weather_icon_clouds.setFixedSize(0, 0)

        else:
            weather_data = self.get_weather(city)
            if weather_data:
                self.city_entry.setText("")

                self.city_name.setText(f"{weather_data['city']}")
                self.city_name.setStyleSheet("font-size: 36px;")
                self.city_name.setAlignment(Qt.AlignCenter)

                self.weather_label.setText(f"{weather_data['weather']}")
                self.weather_label.setAlignment(Qt.AlignCenter)
                self.weather_label.setStyleSheet("font-size: 26px; color: #8398ea;")

                weather_icons = {'Clear': 'assets/Sun.svg', 'Clouds': 'assets/Clouds.svg', 'Rain': 'assets/Rain.svg',
                                 'Snow': 'assets/Snow.svg', 'Rainbow': 'assets/Rainbow.svg'}

                weather = weather_data['weather']

                if weather in weather_icons:
                    icon_path = weather_icons[weather]
                    self.weather_icon_clouds.load(icon_path)
                else:
                    self.weather_icon_clouds.load("assets/Clouds.svg")


                self.weather_icon_clouds.setFixedSize(235, 235)

                self.temperature_label.setText(f"{weather_data['temperature']}°C")
                self.temperature_label.setAlignment(Qt.AlignCenter)

                self.humidity_label.setText(f"Humidity: {weather_data['humidity']}%")
                self.humidity_label.setStyleSheet("font-size: 16px; color: #8398ea;")
                self.humidity_icon.setFixedSize(48, 48)

                self.pressure_label.setText(f"Pressure: {weather_data['pressure']}%")
                self.pressure_label.setStyleSheet("font-size: 16px; color: #8398ea;")
                self.pressure_icon.setFixedSize(48, 48)

                self.wind_speed_label.setText(f"Wind Speed: {weather_data['wind_speed']} m/s")
                self.wind_speed_label.setStyleSheet("font-size: 16px; color: #8398ea;")
                self.wind_icon.setFixedSize(48, 48)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    weather_report = WeatherReport()
    weather_report.show()
    app.exec()