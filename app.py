import streamlit as st
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import time
import subprocess
from ecapture import ecapture as ec
import requests
import pyjokes
import threading
import urllib.parse

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Function to speak text
def speak(text):
    def run_speak():
        engine.say(text)
        engine.runAndWait()
    
    # Run speech in a separate thread to avoid blocking
    threading.Thread(target=run_speak, daemon=True).start()

# Function to wish the user
def wishMe():
    hour = datetime.datetime.now().hour
    if hour < 12:
        greeting = "Good Morning"
    elif hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"
    speak(f"Hello, {greeting}")
    st.sidebar.write(f"Hello, {greeting}")

# Function to take command from user
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source)
        try:
            statement = r.recognize_google(audio, language='en-in')
            st.write(f"User said: {statement}\n")
            return statement
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
        return "None"


st.markdown("""
    <style>
        /* Global styles */
        body {
            background-color: #282c34; /* Dark background for the whole app */
            font-family: 'Arial', sans-serif;
            color: white;
            overflow-x: hidden;
        }

        /* Neon effect for the title */
        h1 {
            font-size: 50px;
            text-align: center;
            color: #61dafb; /* Light blue color */
            animation: neon 1.5s ease-in-out infinite alternate;
        }

        /* Neon effect for the sidebar header */
        .css-1q9syg9 {
            font-size: 20px;
            color: #ff00ff; /* Neon pink color */
            padding-left: 15px;
            font-weight: bold;
            animation: neon 1.5s ease-in-out infinite alternate;
        }

        /* Sidebar styles */
        .css-1d391kg {
            background-color: #21252b; /* Dark sidebar background */
            color: white;
            border-radius: 10px;
            padding: 15px;
        }

        /* Button styles */
        .stButton>button {
            background-color: #61dafb; /* Light blue background */
            color: white;
            border: none;
            border-radius: 10px;
            padding: 12px 30px;
            font-size: 18px;
            font-weight: bold;
            transition: background-color 0.3s ease, transform 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #21a1f1; /* Darker blue on hover */
            transform: scale(1.1);
        }

        /* Neon effect animation */
        @keyframes neon {
            0% {
                text-shadow: 0 0 5px #61dafb, 0 0 10px #61dafb, 0 0 15px #61dafb, 0 0 20px #61dafb, 0 0 25px #61dafb, 0 0 30px #61dafb, 0 0 35px #61dafb;
            }
            100% {
                text-shadow: 0 0 5px #ff00ff, 0 0 10px #ff00ff, 0 0 15px #ff00ff, 0 0 20px #ff00ff, 0 0 25px #ff00ff, 0 0 30px #ff00ff, 0 0 35px #ff00ff;
            }
        }

        /* Header text styling */
        h3 {
            color: #ff9800; /* Orange color for subtitle */
            font-size: 30px;
            text-align: center;
        }

        /* Sidebar links */
        .css-1m6nu1r {
            font-size: 18px;
            color: #ffcc00;
        }

        .css-1m6nu1r:hover {
            color: #ff6f61; /* Hover color */
        }

        /* Remove animation on commands like "open camera" */
        .stButton>button:focus {
            outline: none;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit app
def main():
    st.title("AI Personal Assistant -  NOVA")
    st.sidebar.title("NOVA Commands")
    st.sidebar.write("""
    - Wikipedia
    - Open YouTube
    - Open Google
    - Open Gmail
    - Open Word
    - Open Excel
    - Weather
    - Time
    - Who are you / What can you do
    - Who made you
    - Open StackOverflow
    - News
    - Camera / Take a photo
    - Joke
    - Where is [location]
    - Search [query]
    - Log off / Sign out
    """)

    assistant_started = st.sidebar.button("Start Assistant")
    
    if assistant_started:
        speak("Loading your AI personal assistant NOVA")
        wishMe()

        while True:
            speak("Tell me how can I help you now?")
            statement = takeCommand().lower()
            if statement == "none":
                continue

            if any(phrase in statement for phrase in ["good bye", "ok bye", "stop"]):
                speak('Your personal assistant NOVA is shutting down, Goodbye!')
                st.sidebar.write('Your personal assistant NOVA is shutting down, Goodbye!')
                break

            if 'wikipedia' in statement:
                speak('Searching Wikipedia...')
                statement = statement.replace("wikipedia", "").strip()
                if statement:
                    try:
                        results = wikipedia.summary(statement, sentences=3)
                        speak("According to Wikipedia")
                        st.sidebar.write(results)
                        speak(results)
                    except wikipedia.exceptions.DisambiguationError as e:
                        speak(f"There are multiple results for {statement}. Please be more specific.")
                        st.sidebar.write("Multiple results: " + ", ".join(e.options))
                    except wikipedia.exceptions.PageError:
                        speak("The page you are looking for does not exist on Wikipedia.")
                        st.sidebar.write("The page you are looking for does not exist on Wikipedia.")
                    except Exception as e:
                        speak("An error occurred while searching Wikipedia.")
                        st.sidebar.write(f"An error occurred: {e}")
                else:
                    speak("Please specify what you want to search on Wikipedia.")

            elif 'open youtube' in statement:
                webbrowser.open_new_tab("https://www.youtube.com")
                speak("YouTube is open now")
                time.sleep(5)

            elif 'open google' in statement:
                webbrowser.open_new_tab("https://www.google.com")
                speak("Google Chrome is open now")
                time.sleep(5)

            elif 'open gmail' in statement:
                webbrowser.open_new_tab("https://mail.google.com")
                speak("Gmail is open now")
                time.sleep(5)

            elif "open word" in statement:
                try:
                    subprocess.Popen(r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE')
                except Exception as e:
                    st.error(f"Could not open Word app: {e}")

            elif "open excel" in statement:
                try:
                    subprocess.Popen(r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE')
                except Exception as e:
                    st.error(f"Could not open Excel app: {e}")

            elif "weather" in statement:
                api_key = "8ef61edcf1c576d65d836254e11ea420"
                base_url = "https://api.openweathermap.org/data/2.5/weather?"
                speak("What's the city name?")
                city_name = takeCommand().strip()

                if city_name:
                    complete_url = f"{base_url}appid={api_key}&q={city_name}&units=metric"
                    response = requests.get(complete_url)
                    data = response.json()

                    if data.get("cod") == 200:
                        main = data["main"]
                        temperature = main["temp"]
                        humidity = main["humidity"]
                        weather = data["weather"]
                        weather_description = weather[0]["description"]

                        speak(f"Temperature in Celsius is {temperature} degrees. Humidity is {humidity} percent. Description: {weather_description}.")
                        st.sidebar.write(f"Temperature in Celsius: {temperature}°C\nHumidity: {humidity}%\nDescription: {weather_description}")
                    else:
                        speak("City Not Found")
                        st.sidebar.write("City Not Found")
                else:
                    speak("Please specify a city name.")

            elif 'time' in statement:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The time is {strTime}")
                st.sidebar.write(f"The time is {strTime}")

            elif 'who are you' in statement or 'what can you do' in statement:
                speak('I am NOVA version 1.0, your personal assistant. I can perform tasks like opening YouTube, Google Chrome, Gmail, StackOverflow, taking photos, searching Wikipedia, predicting weather, getting top headlines, and answering computational or geographical questions!')
                st.sidebar.write('I am NOVA version 1.0, your personal assistant. I can perform tasks like opening YouTube, Google Chrome, Gmail, StackOverflow, taking photos, searching Wikipedia, predicting weather, getting top headlines, and answering computational or geographical questions!')

            elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
                speak("I was built by Sujay")
                st.sidebar.write("I was built by Sujay")

            elif "open stack overflow" in statement:
                webbrowser.open_new_tab("https://stackoverflow.com")
                speak("Here is Stack Overflow")

            elif 'news' in statement:
                webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
                speak('Here are some headlines from the Times of India, Happy reading')
                time.sleep(6)

            elif "camera" in statement or "take a photo" in statement:
                ec.capture(0, "robo camera", "img.jpg")

            elif 'joke' in statement:
                joke = pyjokes.get_joke()
                speak(joke)
                st.sidebar.write(joke)

            elif "where is" in statement:
                query = statement.replace("where is", "").strip()
                if query:
                    speak(f"Locating {query} for you.")
                    url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(query)}"
                    webbrowser.open(url)
                    st.sidebar.write(f"Locating {query}")
                else:
                    speak("Please specify a location.")
                    st.sidebar.write("No location specified.")

            elif 'search' in statement:
                query = statement.replace("search", "").strip()
                if query:
                    query = urllib.parse.quote(query)
                    search_url = f"https://www.google.com/search?q={query}"
                    webbrowser.open_new_tab(search_url)
                    time.sleep(5)
                else:
                    speak("Please specify what you want to search.")

            elif "log off" in statement or "sign out" in statement:
                speak("Ok, your PC will log off in 10 seconds. Make sure you exit from all applications.")
                subprocess.call(["shutdown", "/l"])

            time.sleep(3)

if __name__ == '__main__':
    main()
