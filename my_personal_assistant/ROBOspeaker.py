import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import sys
import requests

# Initialize the speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 130)  # Set the speaking rate

# Set up the recognizer
recognizer = sr.Recognizer()

# API keys
API_KEY = "322e556b091f13c5d5b03fe7352e3b66"  # weathearapp api
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast?"
NEWS_API_KEY = "1e40406dd6bb43269f3ce39ed86bfa06"  # NewsAPI key
NEWS_URL = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"


def speak(text):
    """Function to convert text to speech"""
    print(text)  # Print to console for visibility
    engine.say(text)
    engine.runAndWait()


def get_audio():
    """Function to capture audio input from the user"""
    return input("Type your command: ").lower()  # Change this if you want voice input


def get_weather(city):
    """Function to get current weather for a city"""
    url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        speak(
            f"The current weather in {city} is {weather_description} with a temperature of {temperature} degrees Celsius.")
    else:
        speak("Sorry, I couldn't retrieve the weather data. Please check the city name.")


def get_weekly_forecast(city):
    """Function to get weekly weather forecast for a city"""
    url = f"{FORECAST_URL}q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast = "Weekly weather forecast: "
        for day in data['list'][:7]:  # Get 7 days of forecast
            date = day['dt_txt']
            temp = day['main']['temp']
            weather_desc = day['weather'][0]['description']
            forecast += f"On {date}, it will be {weather_desc} with a temperature of {temp} degrees Celsius. "
        speak(forecast)
    else:
        speak("Sorry, I couldn't retrieve the weekly forecast data.")


def get_news():
    """Function to get the latest news headlines"""
    response = requests.get(NEWS_URL)
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data['articles']
        headlines = "Here are the latest news headlines: \n "
        for article in articles[:5]:  # Get top 5 articles
            headlines += "\n"f"{article['title']}."
        speak(headlines)

    else:
        speak("Sorry, I couldn't retrieve the news at the moment.")

def respond_to_command(command):
    """Function to execute tasks based on the command"""
    if "hello" in command or "hi" in command:
        speak("Hello, how can I help you?")

    elif "day" in command:
        current_day = datetime.datetime.now().strftime("%A")
        speak(f"Today is {current_day}")

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}")

    elif "weather" in command:
        city = command.split("in")[-1].strip()  # Get the city from the command
        get_weather(city)

    elif "forecast" in command:
        city = command.split("in")[-1].strip()  # Get the city from the command
        get_weekly_forecast(city)

    elif "news" in command:
        print("Fetching news...")
        get_news()

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "exit" in command or "quit" in command:
        speak("Thank you for using me. Have a nice day!")
        sys.exit()

    else:
        speak("I didn't recognize that command. Let me search that for you.")
        web_search(command)


def web_search(query):
    """Perform a web search for unrecognized commands"""
    webbrowser.open(f"https://www.google.com/search?q={query}")


if __name__ == "__main__":
    speak("Welcome to your personal assistant.")
    while True:
        command = get_audio()
        if command:
            respond_to_command(command)



