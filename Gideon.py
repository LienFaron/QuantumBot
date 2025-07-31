import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pywhatkit
import os

# --- IMPORTANT: Set the path to your Chrome installation ---
# The path might be different on your PC. 
# Double-check "C:/Program Files" or "C:/Program Files (x86)".
chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

def speak(audio):
    """
    This function initializes a new TTS engine for each call to prevent audio driver conflicts,
    and then speaks the provided audio string.
    """
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id) # Use voices[0] for male, voices[1] for female

    print(f"Gideon: {audio}")
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """Greets the user according to the time of day."""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning, Sir!")
    elif 12 <= hour < 18:
        speak("Good Afternoon, Sir!")
    else:
        speak("Good Evening, Sir!")
    
    speak("I am Gideon. How may I assist you today?")

def takeCommand():
    """Takes microphone input from the user and returns the command as a string."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()
    except Exception as e:
        speak("I'm sorry, I didn't catch that. Could you please say it again?")
        return "none"

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()

        # --- Conversational Commands ---
        if 'how are you' in query:
            speak("I am at one hundred percent efficiency, Sir. Thank you for asking.")

        elif 'who are you' in query:
            speak("I am Gideon, a virtual artificial intelligence, ready to assist you.")

        # --- Functional Commands ---
        elif 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia...")
                speak(results)
            except Exception:
                speak(f"Sorry sir, I could not find any results for {query} on Wikipedia.")

        elif 'open youtube' in query:
            speak("Opening YouTube in Chrome, Sir.")
            webbrowser.get(chrome_path).open("youtube.com")

        elif 'open whatsapp' in query:
            speak("Opening WhatsApp in Chrome, Sir.")
            webbrowser.get(chrome_path).open("web.whatsapp.com")
            
        elif 'open google' in query:
            speak("Opening Google in Chrome, Sir.")
            webbrowser.get(chrome_path).open("google.com")
            
        elif 'play' in query:
            song = query.replace('play', '')
            speak('Playing ' + song + ' on YouTube.')
            pywhatkit.playonyt(song)

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p")    
            speak(f"Sir, the time is {strTime}")

        # --- Exit Command ---
        elif 'exit' in query or 'quit' in query or 'goodbye' in query:
            speak("Goodbye, Sir. It was a pleasure to assist you.")
            break