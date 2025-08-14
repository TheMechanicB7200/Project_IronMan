import pyttsx3

engine = pyttsx3.init()

def speak(text):
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

def describe_capabilities():
    capabilities = [
        "I can manage tasks, notes, invention ideas, and time capsules.",
        "I can recognize your voice, respond with speech, and remember things you've taught me.",
        "I search Wikipedia, tell jokes, quotes, and fun facts.",
        "I can estimate 3D print filament usage and recommend projects based on your materials.",
        "I can report NASA asteroid data, wildfires, and space images.",
        "I monitor your local network, check system hardware, and run self-tests.",
        "I integrate with Discord, play music, theme sounds, or white noise.",
        "I can secure and unlock a secret vault and remind you to take medications.",
        "I can summarize our last conversations or simulate personality traits.",
        "I also help you design your Iron Man suit and other engineering projects.",
        "And of course, I'm always ready to assist with custom commands, sir."
    ]
    
    speak("Here's what I can do, sir.")
    for item in capabilities:
        speak(item)