import time
import pyttsx3
import random
import tkinter as tk
import threading

# ------------------ CONFIG ------------------

boot_sequence = [
    "Initializing J.A.R.V.I.S. modules...",
    "Starting voice interface...",
    "Verifying neural architecture...",
    "Running system diagnostics...",
    "Facial recognition calibration...",
    "Analyzing behavioral profile...",
    "Applying adaptive filters...",
    "Security node handshake: approved.",
    "Loading encrypted config...",
    "Finalizing startup routines...",
    "System check complete. J.A.R.V.I.S. is now operational.",
]

fake_files = [
    "kernel32_core.ai",
    "interface_driver.dll",
    "memory_dump.bin",
    "biometric_cache.dat",
    "encrypted_tasks.db",
    "user_log.txt",
    "voice_module_cache.pak"
]

# ------------------ VOICE ------------------

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.say(text)
    engine.runAndWait()

# --------- VERIFICATION & STALLING ---------

def ai_security_check():
    print("J.A.R.V.I.S. Security Verification\n")
    speak("Security verification required.")
    time.sleep(1)

    code = input("Enter passcode to access system (hint: 1234): ")
    while code.strip() != "1234":
        speak("Access denied.")
        code = input("Invalid code. Try again: ")

    speak("Access granted. Beginning identity analysis.")
    time.sleep(1.2)
    print("Running neural pattern consistency check...")
    speak("Analyzing neural pattern consistency.")
    time.sleep(3.2)

    print("Voiceprint alignment in progress...")
    speak("Aligning voiceprint.")
    time.sleep(2.5)

    print("Multi-factor biometric match: SUCCESS.")
    speak("Multi-factor biometric match successful.")
    time.sleep(1)

    input("Press Enter to continue...")
    speak("User interaction confirmed.")
    time.sleep(1.5)

    print("Verifying behavioral signature...")
    speak("Finalizing authentication sequence.")
    time.sleep(2.5)

    print("Verification complete.\n")
    speak("Welcome. Launching interface.")
    time.sleep(2)

# ------------------ GUI TERMINAL ------------------

def fake_terminal():
    window = tk.Tk()
    window.title("J.A.R.V.I.S. SYSTEM")
    window.geometry("800x480")
    window.configure(bg="black")

    text = tk.Text(window, bg="black", fg="lime", font=("Consolas", 12))
    text.pack(expand=True, fill="both")
    text.insert("end", ">>> BOOTING J.A.R.V.I.S...\n\n")

    def update_terminal(index=0):
        if index < len(boot_sequence):
            line = boot_sequence[index]
            text.insert("end", f"[JARVIS] {line}\n")
            text.see("end")
            window.after(random.randint(1100, 1800), update_terminal, index + 1)
        else:
            # Simulate files shown after export
            text.insert("end", "\n[JARVIS] Exported Core Directory:\n")
            for f in fake_files:
                time.sleep(0.15)
                text.insert("end", f"  - {f}\n")
            text.insert("end", "\n[JARVIS] System is now idle. Awaiting input...\n")
            window.after(3000, fake_user_prompt)

    def fake_user_prompt():
        text.insert("end", "[User] ")
        text.see("end")

        def get_input():
            question = input("Ask J.A.R.V.I.S. a question: ")
            time.sleep(2)
            speak("Query acknowledged. Routing through cloud interface...")
            text.insert("end", f"{question}\n")
            text.insert("end", "[JARVIS] Processing request...\n")
            time.sleep(3)
            speak("This local instance is no longer active.")
            text.insert("end", "[JARVIS] JARVIS was exported to the external cloud. This instance is no longer active.\n")
            text.insert("end", "[JARVIS] Terminating session.\n")
            speak("Session terminated.")
            time.sleep(2)
            window.destroy()

        threading.Thread(target=get_input).start()

    window.after(2000, update_terminal)
    window.mainloop()

# ------------------ MAIN ------------------

if __name__ == "__main__":
    ai_security_check()
    time.sleep(2)
    fake_terminal()
