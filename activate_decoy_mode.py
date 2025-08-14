import subprocess
import platform
import sys
import os

def activate_decoy_and_shutdown():
    decoy_path = os.path.join(os.path.dirname(__file__), "JARVIScore.py")

    try:
        # ✅ Launch JARVIScore.py in a new terminal (Windows)
        if platform.system() == "Windows":
            subprocess.Popen([
                "start", "powershell", "-WindowStyle", "Hidden",
                "python", f'"{decoy_path}"'
            ], shell=True)
        else:
            subprocess.Popen(["x-terminal-emulator", "-e", f"python3 {decoy_path}"])

        print("JARVIS: Decoy mode activated.")

        # ✅ Kill VS Code if it's open (stealth mode)
        if platform.system() == "Windows":
            subprocess.call(["taskkill", "/F", "/IM", "Code.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.call(["pkill", "-f", "code"])

    except Exception as e:
        print(f"[ERROR] Failed to launch decoy: {e}")

    sys.exit()  # Kill the real JARVIS