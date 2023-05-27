from PyQt6 import QtWidgets
import requests

API_key = '332a956d69f5d90fb1a571aa6cc9606b'

class WeatherReport(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.city_label = QtWidgets.QLabel("Введите название города:")
        self.city_entry = QtWidgets.QLineEdit()
        self.submit_button = QtWidgets.QPushButton("Получить погоду")
        self.city_name = QtWidgets.QLabel()
        self.temperature_label = QtWidgets.QLabel()
        self.humidity_label = QtWidgets.QLabel()
        self.pressure_label = QtWidgets.QLabel()
        self.description_label = QtWidgets.QLabel()
        self.wind_speed_label = QtWidgets.QLabel()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.city_label)
        layout.addWidget(self.city_entry)
        layout.addWidget(self.city_name)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.temperature_label)
        layout.addWidget(self.humidity_label)
        layout.addWidget(self.pressure_label)
        layout.addWidget(self.description_label)
        layout.addWidget(self.wind_speed_label)

        self.setLayout(layout)

        self.submit_button.clicked.connect(self.show_weather)

    def get_weather(self, city):
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}&units=metric'
        response = requests.get(url)
        weather_data = response.json()
        if weather_data['cod'] != '404':
            city_name = weather_data['name']
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            pressure = weather_data['main']['pressure']
            weather_description = weather_data['weather'][0]['description']
            wind_speed = weather_data['wind']['speed']
            return {'city_name': city_name, 'temperature': temperature, 'humidity': humidity, 'pressure': pressure,
                    'description': weather_description, 'wind_speed': wind_speed}
        else:
            return None

    def show_weather(self):
        city = self.city_entry.text()
        weather_data = self.get_weather(city)
        if weather_data:
            self.city_name.setText(f"{weather_data['name']}")
            self.temperature_label.setText(f"Temperature: {weather_data['temperature']}°C")
            self.humidity_label.setText(f"Humidity: {weather_data['humidity']}%")
            self.pressure_label.setText(f"Pressure: {weather_data['pressure']} hPa")
            self.description_label.setText(f"Weather: {weather_data['description']}")
            self.wind_speed_label.setText(f"Wind Speed: {weather_data['wind_speed']} m/s")
        else:
            self.city_name.setText("Город не найден")
            self.temperature_label.setText("")
            self.humidity_label.setText("")
            self.pressure_label.setText("")
            self.description_label.setText("")
            self.wind_speed_label.setText("")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    weather_report = WeatherReport()
    weather_report.show()
    app.exec()