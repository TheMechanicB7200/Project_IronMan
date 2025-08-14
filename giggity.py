import cv2
import mediapipe as mp
import tkinter as tk
from PIL import Image, ImageTk
import math
import pygame
import time
import subprocess
import os

class HandTracker:
    def __init__(self):
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Initialize tkinter window
        self.root = tk.Tk()
        self.root.title("Hand Gesture Tracker")
        self.root.geometry("1280x720")

        self.label = tk.Label(self.root)
        self.label.pack(fill="both", expand=True)

        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

        # Sound & script paths
        self.rock_sound_path = r"c:\Users\pjtru\OneDrive\Projects\JARVIS MK.1\Acdc-Dc-BackInBlack.mp3"
        self.peace_sound_path = r"c:\Users\pjtru\OneDrive\Projects\JARVIS MK.1\iron-man.mp3"
        self.launch_script_path = r"C:\Path\To\Your\Script.py"  # Update this!

        # Initialize sound engine
        pygame.mixer.init()

        # State tracking
        self.sound_playing = False
        self.peace_sound_playing = False
        self.rock_hold_start = None
        self.peace_hold_start = None
        self.script_launched = False

    # --- Gesture Detection Methods ---

    def fingers_touching(self, thumb, index):
        return math.dist(thumb, index) < 30

    def is_extended(self, landmarks, tip, pip, h):
        return landmarks.landmark[tip].y * h < landmarks.landmark[pip].y * h

    def is_fist(self, landmarks, h):
        return all(
            not self.is_extended(landmarks, tip, pip, h)
            for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]
        )

    def is_rock_symbol(self, landmarks, h):
        return (
            self.is_extended(landmarks, 8, 6, h) and     # Index
            self.is_extended(landmarks, 20, 18, h) and   # Pinky
            not self.is_extended(landmarks, 12, 10, h) and
            not self.is_extended(landmarks, 16, 14, h)
        )

    def is_peace_sign(self, landmarks, h):
        return (
            self.is_extended(landmarks, 8, 6, h) and      # Index
            self.is_extended(landmarks, 12, 10, h) and    # Middle
            not self.is_extended(landmarks, 16, 14, h) and
            not self.is_extended(landmarks, 20, 18, h)
        )

    # --- Core Frame Processing ---

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        h, w, _ = frame.shape
        gestures = {
            "rock": False,
            "peace": False,
            "fist": False,
            "touch": False,
        }

        if results.multi_hand_landmarks:
            for idx, lm in enumerate(results.multi_hand_landmarks):
                self.mp_draw.draw_landmarks(frame, lm, self.mp_hands.HAND_CONNECTIONS)

                thumb = (int(lm.landmark[4].x * w), int(lm.landmark[4].y * h))
                index = (int(lm.landmark[8].x * w), int(lm.landmark[8].y * h))

                if self.fingers_touching(thumb, index):
                    gestures["touch"] = True
                    self._annotate(frame, f"Hand {idx+1}: Fingers touching!", 50 + idx * 100, (255, 0, 0))

                if self.is_fist(lm, h):
                    gestures["fist"] = True
                    self._annotate(frame, f"Hand {idx+1}: Fist detected!", 100 + idx * 100, (0, 255, 255))

                if self.is_rock_symbol(lm, h):
                    gestures["rock"] = True
                    self._annotate(frame, f"Hand {idx+1}: Rock n Roll!", 150 + idx * 100, (0, 128, 255))

                if self.is_peace_sign(lm, h):
                    gestures["peace"] = True
                    self._annotate(frame, f"Hand {idx+1}: Peace sign!", 200 + idx * 100, (128, 0, 255))

        self._handle_gestures(gestures)

        return frame

    def _annotate(self, frame, text, y, color):
        cv2.putText(frame, text, (50, y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    def _handle_gestures(self, gestures):
        now = time.time()

        # Rock hold detection
        if gestures["rock"]:
            if self.rock_hold_start is None:
                self.rock_hold_start = now
            elif now - self.rock_hold_start >= 3 and not self.sound_playing:
                self._play_sound(self.rock_sound_path)
                self.sound_playing = True
        else:
            self.rock_hold_start = None

        # Peace hold detection
        if gestures["peace"]:
            if self.peace_hold_start is None:
                self.peace_hold_start = now
            elif now - self.peace_hold_start >= 3 and not self.peace_sound_playing:
                self._play_sound(self.peace_sound_path)
                self.peace_sound_playing = True
        else:
            self.peace_hold_start = None

        # Fist stops all sounds
        if gestures["fist"]:
            self._stop_sounds()

        # Launch script on touch gesture
        if gestures["touch"] and not self.script_launched:
            if os.path.exists(self.launch_script_path):
                subprocess.Popen(["python", self.launch_script_path], shell=True)
                self.script_launched = True
            else:
                print("Launch script not found!")

    def _play_sound(self, path):
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Error playing sound: {e}")

    def _stop_sounds(self):
        pygame.mixer.music.stop()
        self.sound_playing = False
        self.peace_sound_playing = False

    # --- UI & Frame Loop ---

    def update_image(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Webcam access error.")
            self.root.after(10, self.update_image)
            return

        frame = cv2.flip(frame, 1)
        frame = self.process_frame(frame)

        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img = img.resize((1280, 720), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image=img)

        self.label.config(image=photo)
        self.label.image = photo
        self.root.after(10, self.update_image)

    def run(self):
        self.update_image()
        self.root.mainloop()
        self.cap.release()
        cv2.destroyAllWindows()
        self._stop_sounds()

# --- Main Execution ---

if __name__ == "__main__":
    tracker = HandTracker()
    tracker.run()
