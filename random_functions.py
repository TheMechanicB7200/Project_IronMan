import random
import pyttsx3
import socket
import time
import datetime
import pygame
# Initialize voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 143)  # Speed of speech

def speak(text):
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()


def get_ip_address():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    speak(f"JARVIS: Your IP address is {ip}")


def play_white_noise_until_4am():
    # Initialize audio
    pygame.mixer.init()
    pygame.mixer.music.load(r"C:\Users\pjtru\OneDrive\Projects\JARVIS MK.1\01-White-Noise-10min.mp3"),
    pygame.mixer.music.play(-1)  # -1 means loop forever

    print("Playing white noise until 4:00 AM.")

    while True:
        now = datetime.datetime.now()
        if now.hour == 4 and now.minute == 0:
            pygame.mixer.music.stop()
            print("JARVIS: Stopping white noise. It's 4:00 AM.")
            break
        time.sleep(30)  # check every 30 seconds


def roll_dice():
    print(f"JARVIS: You rolled a {random.randint(1, 6)}.")

def flip_coin():
    print(f"JARVIS: It's {'Heads' if random.choice([True, False]) else 'Tails'}.")

