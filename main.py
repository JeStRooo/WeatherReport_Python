import requests
import tkinter as tk
from tkinter import PhotoImage

# root = tk.Tk()

API_key = '332a956d69f5d90fb1a571aa6cc9606b'

# search_image = tk.PhotoImage(file="./assets/searchIcon.svg")

def get_weather(city):
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
        return {'city_name': city_name, 'temperature': temperature, 'humidity': humidity, 'pressure': pressure, 'description': weather_description, 'wind_speed': wind_speed}
    else:
        return None

def show_weather():
    city = city_entry.get()
    weather_data = get_weather(city)
    if weather_data:
        temperature_label.config(text=f"Температура: {weather_data['temperature']}°C")
        humidity_label.config(text=f"Влажность: {weather_data['humidity']}%")
        pressure_label.config(text=f"Давление: {weather_data['pressure']} hPa")
        description_label.config(text=f"Погода: {weather_data['description']}")
        wind_speed_label.config(text=f"Скорость ветра: {weather_data['wind_speed']} m/s")
    else:
        temperature_label.config(text="City not found.")
        humidity_label.config(text='')
        pressure_label.config(text='')
        description_label.config(text='')
        wind_speed_label.config(text='')

window = tk.Tk()
window.title("WeatherReport")

# Установка фоновых цветов для кнопок и меток
window.config(bg='#edf0fc')
city_label = tk.Label(window, text="Enter city name:")
city_label.grid(row=0, column=0, padx=10, pady=10)

city_entry = tk.Entry(window)
city_entry.grid(row=0, column=1, padx=10, pady=10)

# Изменение фонового цвета кнопки
# search_button = tk.Button(window, image=search_image, command=show_weather, bd=0, bg='dark blue')
# search_button.image = search_image # сохраните ссылку на объект изображения
# search_button.grid(row=0, column=2, padx=10, pady=10)

search_button = tk.Button(window, text='Поиск', command=show_weather, bd=0, bg='white')
search_button.grid(row=0, column=2, padx=10, pady=10)

temperature_label = tk.Label(window, text='', font=('Arial', 14))
temperature_label.grid(row=1, column=0, padx=10, pady=10)

humidity_label = tk.Label(window, text='', font=('Arial', 14))
humidity_label.grid(row=1, column=1, padx=10, pady=10)

pressure_label = tk.Label(window, text='', font=('Arial', 14))
pressure_label.grid(row=1, column=2, padx=10, pady=10)

description_label = tk.Label(window, text='', font=('Arial', 14))
description_label.grid(row=2, column=0, padx=10, pady=10)

wind_speed_label = tk.Label(window, text='', font=('Arial', 14))
wind_speed_label.grid(row=2, column=1, padx=10, pady=10)

window.mainloop()