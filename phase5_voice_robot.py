import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    print("ROBOT:", text)
    engine.say(text)
    engine.runAndWait()

r = sr.Recognizer()
mic = sr.Microphone()

speak("Voice control activated")

while True:
    try:
        with mic as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source)

        command = r.recognize_google(audio).lower()
        print("You said:", command)

        if "forward" in command:
            speak("Moving forward")

        elif "left" in command:
            speak("Turning left")

        elif "right" in command:
            speak("Turning right")

        elif "stop" in command:
            speak("Stopping")

        elif "exit" in command:
            speak("Shutting down")
            break

        else:
            speak("Command not recognized")

    except:
        print("Could not understand")