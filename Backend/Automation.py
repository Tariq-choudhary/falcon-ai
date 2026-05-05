import os
import webbrowser
import subprocess
import datetime
import ctypes


class FalconAI:

    def run_task(self, task):

        task = task.lower().strip()

        # ================= DATE & DAY (FIXED 🔥) ================= #

        if "date" in task or "day" in task or "today" in task:
            today = datetime.datetime.now().strftime("%A, %d %B %Y")
            return f"Today is {today}."

        # ================= TIME ================= #

        if "time" in task:
            now = datetime.datetime.now().strftime("%I:%M %p")
            return f"Current time is {now}."

        # ================= VOLUME CONTROL ================= #

        if "unmute" in task:
            ctypes.windll.winmm.waveOutSetVolume(0, 0xFFFFFFFF)
            return "System unmuted."

        if "mute" in task:
            ctypes.windll.winmm.waveOutSetVolume(0, 0)
            return "System muted."

        # ================= POWER CONTROLS ================= #

        if "shutdown" in task:
            os.system("shutdown /s /f /t 1")
            return "Shutting down the system."

        if "restart" in task:
            os.system("shutdown /r /f /t 1")
            return "Restarting the system."

        if "sleep" in task:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return "System going to sleep."

        if "lock" in task:
            ctypes.windll.user32.LockWorkStation()
            return "System locked."

        # ================= WEBSITES ================= #

        if "chatgpt" in task:
            webbrowser.open("https://chat.openai.com")
            return "Opening ChatGPT."

        if "youtube" in task:
            webbrowser.open("https://www.youtube.com")
            return "Opening YouTube."

        if "gmail" in task:
            webbrowser.open("https://mail.google.com")
            return "Opening Gmail."

        if "github" in task:
            webbrowser.open("https://github.com")
            return "Opening GitHub."

        if "google" in task:
            webbrowser.open("https://www.google.com")
            return "Opening Google."

        # ================= WINDOWS SYSTEM ================= #

        if "file explorer" in task or "explorer" in task:
            subprocess.Popen("explorer")
            return "Opening File Explorer."

        if "downloads" in task:
            path = os.path.join(os.path.expanduser("~"), "Downloads")
            subprocess.Popen(f'explorer "{path}"')
            return "Opening Downloads folder."

        if "documents" in task:
            path = os.path.join(os.path.expanduser("~"), "Documents")
            subprocess.Popen(f'explorer "{path}"')
            return "Opening Documents folder."

        if "desktop" in task:
            path = os.path.join(os.path.expanduser("~"), "Desktop")
            subprocess.Popen(f'explorer "{path}"')
            return "Opening Desktop folder."

        # ================= APPLICATIONS ================= #

        if "notepad" in task:
            subprocess.Popen("notepad")
            return "Opening Notepad."

        if "excel" in task:
            try:
                subprocess.Popen("excel")
                return "Opening Microsoft Excel."
            except:
                possible_paths = [
                    r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\root\Office16\EXCEL.EXE"
                ]
                for path in possible_paths:
                    if os.path.exists(path):
                        subprocess.Popen(path)
                        return "Opening Microsoft Excel."
                return "Excel not found in system."

        if "vs code" in task or "visual studio code" in task:
            try:
                subprocess.Popen("code")
                return "Opening VS Code."
            except:
                return "VS Code not found in system."

        if "chrome" in task:
            try:
                subprocess.Popen("chrome")
                return "Opening Google Chrome."
            except:
                webbrowser.open("https://www.google.com")
                return "Opening browser."

        # ================= DEFAULT ================= #

        return "Sorry, I didn't understand that command."