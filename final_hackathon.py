import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime
import requests
import subprocess
import psutil

# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize the speech engine
engine = pyttsx3.init()

# API Keys
WEATHER_API_KEY = '4fd2c1ecc176d4402c115bd5296c25e7'
NEWS_API_KEY = 'e7fb4c4793774a4bb6602b7e5dfdfa7f'

def speak(text):
    print(text)  # Display the output in the console
    engine.say(text)  # Speak the text
    engine.runAndWait()  # Wait for the speech to finish

def listen_command():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        user_command = recognizer.recognize_google(audio).lower()
        print("You said:", user_command)
    except sr.UnknownValueError:
        speak("Sorry, I could not understand that.")
        return None
    except sr.RequestError as e:
        speak(f"Error with speech recognition service: {e}")
        return None
    return user_command

def search_web(query):
    speak(f"Searching for {query} on the web.")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def open_website(website):
    speak(f"Opening {website}.")
    webbrowser.open(f"https://{website}")

def open_application(app_name):
    try:
        if "youtube" in app_name.lower():
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")
        elif "notepad" in app_name.lower():
            speak("Opening Notepad.")
            subprocess.Popen("notepad", shell=True)
        elif "calculator" in app_name.lower() or "calc" in app_name.lower():
            speak("Opening Calculator.")
            subprocess.Popen("calc", shell=True)
        else:
            speak(f"Trying to open {app_name}.")
            subprocess.Popen(app_name, shell=True)
    except FileNotFoundError:
        speak(f"Could not find an application named {app_name}. Please check the name and try again.")
    except Exception as e:
        speak(f"An error occurred while trying to open {app_name}: {str(e)}")

def tell_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {current_time}.")

def get_weather():
    speak("Fetching the weather report.")
    url = f"http://api.openweathermap.org/data/2.5/weather?q=London&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            weather_desc = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            speak(f"The weather is {weather_desc} with a temperature of {temperature}°C.")
        else:
            speak("Sorry, I could not fetch the weather data.")
    except requests.exceptions.RequestException as e:
        speak(f"Error fetching weather data: {e}")

def get_latest_news():
    speak("Fetching the latest news.")
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data["status"] == "ok":
            for article in data["articles"][:5]:
                speak(f"Headline: {article['title']}")
        else:
            speak("Sorry, I could not fetch the latest news.")
    except requests.exceptions.RequestException as e:
        speak(f"Error fetching news data: {e}")

def perform_system_check():
    speak("Performing system check.")
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    speak(f"CPU usage is at {cpu_usage} percent. Memory usage is at {memory_usage} percent. Disk usage is at {disk_usage} percent.")

def main():
    speak("Hello! How can I assist you today?")
    while True:
        command = listen_command()
        if command is None:
            continue
        if "search" in command:
            query = command.replace("search", "").strip()
            search_web(query)
        elif "open" in command:
            app_or_website = command.replace("open", "").strip()
            # Check if it's likely a website or an application
            if "." in app_or_website:  # A website usually contains '.'
                open_website(app_or_website)
            else:
                open_application(app_or_website)
        elif "time" in command:
            tell_time()
        elif "weather" in command:
            get_weather()
        elif "news" in command:
            get_latest_news()
        elif "system check" in command:
            perform_system_check()
        elif "exit" in command or "quit" in command:
            speak("Goodbye! See you on your next visit.")
            break

if __name__ == "__main__":
    main()
