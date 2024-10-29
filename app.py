from flask import Flask, render_template, request, jsonify
import datetime
import webbrowser
import sys
import requests
import os

app = Flask(__name__)

# API keys
API_KEY = "322e556b091f13c5d5b03fe7352e3b66"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast?"
NEWS_API_KEY = "1e40406dd6bb43269f3ce39ed86bfa06"
NEWS_URL = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"

def get_weather(city):
    url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"The current weather in {city} is {weather_description} with a temperature of {temperature}°C.", f"The current weather in {city} is {weather_description} with a temperature of {temperature}°C."
    return "Sorry, I couldn't retrieve the weather data. Please check the city name.", "Sorry, I couldn't retrieve the weather data. Please check the city name."

def get_weekly_forecast(city):
    url = f"{FORECAST_URL}q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast = "Weekly weather forecast: "
        for day in data['list'][:7]:
            date = day['dt_txt']
            temp = day['main']['temp']
            weather_desc = day['weather'][0]['description']
            forecast += f"On {date}, it will be {weather_desc} with a temperature of {temp}°C. "
        return forecast, forecast
    return "Sorry, I couldn't retrieve the weekly forecast data.", "Sorry, I couldn't retrieve the weekly forecast data."

def get_news():
    response = requests.get(NEWS_URL)
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data['articles']
        headlines = "Here are the latest news headlines: "
        for article in articles[:5]:
            headlines += f"{article['title']}. "
        return headlines, headlines
    return "Sorry, I couldn't retrieve the news at the moment.", "Sorry, I couldn't retrieve the news at the moment."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    user_input = request.json.get('command', '').lower()
    spoken_text, html_response = respond_to_command(user_input)  # Get both parts
    return jsonify({'response': html_response, 'spoken': spoken_text})  # Send both to the client

def web_search(query):
    return f"https://www.google.com/search?q={query.replace(' ', '+')}"

def respond_to_command(command):
    if "hello" in command or "hi" in command:
        return "Hello, how can I help you?", "Hello, how can I help you?"

    elif "day" in command:
        current_day = datetime.datetime.now().strftime("%A")
        return f"Today is {current_day}", f"Today is {current_day}"

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        return f"The current time is {current_time}", f"The current time is {current_time}"

    elif "weather" in command:
        city = command.split("in")[-1].strip()
        return get_weather(city)

    elif "forecast" in command:
        city = command.split("in")[-1].strip()
        return get_weekly_forecast(city)

    elif "news" in command:
        return get_news()

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube", "Opening YouTube"

    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google", "Opening Google"

    elif "exit" in command or "quit" in command:
        sys.exit("Thank you for using the assistant. Goodbye!")

    else:
        search_url = web_search(command)
        spoken_text = f"I didn't recognize that command. You can search for it online."
        html_response = f"You can search for it online here: <a href='{search_url}' target='_blank'>Search for {command}</a>"
        return spoken_text, html_response  # Return both spoken text and HTML response

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
