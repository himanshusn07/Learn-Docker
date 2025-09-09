import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from urllib3.exceptions import HTTPError


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()  #This can be used in order to send arguments to the parent class-QWidget
        self.city_label = QLabel("Enter city name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label") # Object name = unique id for the widget
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # CSS styling can be applied on a class - QLabel, etc.
        # Can precede the object ID to apply CSS styling to a particular object ID(widget)
        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 70px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#description_label{
                font-size: 50px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):

        api_key = "d90ddb31f77638b730cce1a3aea5ae2c"
        city = self.city_input.text()   # .text() to capture the text entered in the city_input line edit widget
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        #"try" does not catch HTTPError exception, so has to enter it manually.
        try:
            responce = requests.get(url)
            responce.raise_for_status() # This will raise an exception for HTTPError
            data = responce.json()  #converted to .json file
            #print(data) # At the end of .json file is http code of the response.
                        # Example - 'cod': 200 means OK, 404 means not found

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error: #naming HTTPError as http_error to print it in the end
            # HTTPError means code is b/w 400 and 500
            match responce.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorize:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad gateway:\nInvalid responce from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occured:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection.")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out.")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects:\nCheck the URL.")

        except requests.exceptions.RequestException as req_error: #Exceptions like wrong url or network issue, etc.
            self.display_error(f"Request Error:\n{req_error}")

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px")
        self.temperature_label.setText(message)
        self.emoji_label.clear() #This clears the label when getting error message and does not show any old emojis
        self.description_label.clear()

    def display_weather(self, data):
        #print(data) # Data has a "main" key which has a dictionary value.

        self.temperature_label.setStyleSheet("font-size: 75px")

        temperature_k = data["main"]["temp"]    # "Temp" value is in Kelvin temperature
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5) - 459.67
        # data has a "weather" key which has list type value and the list only has one value(index[0]) which is a dictionary itself.
        # At index[0] of list value has multiple key: value pairs. Example - 'description': 'clear sky'
        weather_description = data["weather"][0]["description"]

        # print(data) # data has a "weather" key which has list type value and the list only has one value(index[0]) which is a dictionary itself.
        # At index[0] of list value has multiple key: value pairs. Example - 'weather_id': '803
        weather_id = data["weather"][0]["id"]
        self.temperature_label.setText(f"{temperature_c:.0f}°C") # Use "Window + ." to enter special symbols or emojis
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod   #Static method belong to a class, but don't require any instance specific data or any methods
    def get_weather_emoji(weather_id):  #This method does not rely on any class or instance data - static method
        if 200 <= weather_id <= 232:   #Could use match-case statements as well
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪"
        elif weather_id == 800:
            return "☀️"
        elif 801<= weather_id <=804:
            return "☁️"
        else:
            return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())