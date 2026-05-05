import os
import sys
import datetime
import sqlite3
from zoneinfo import ZoneInfo
from openai import OpenAI
from dotenv import load_dotenv
from Backend.Automation import FalconAI

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=API_KEY
)

# ================= CLEAN COMMAND ================= #

def clean_command(command):
    command = command.lower().strip()

    replacements = {
        "you tube": "youtube",
        "note pad": "notepad",
        "chat gpt": "chatgpt",
        "goggle": "google",
        "what is the time": "time",
        "tell me the time": "time",
        "today date": "date"
    }

    for wrong, correct in replacements.items():
        command = command.replace(wrong, correct)

    return command


# ================= DATABASE ================= #

class FALCONDatabase:

    def __init__(self, db_path='Database/FALCON.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            assistant TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()
        conn.close()

    def add_conversation(self, user_message):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO conversations (user) VALUES (?)", (user_message,))
        cid = cursor.lastrowid
        conn.commit()
        conn.close()
        return cid

    def update_response(self, cid, response):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE conversations SET assistant=? WHERE id=?", (response, cid))
        conn.commit()
        conn.close()


# ================= ASSISTANT ================= #

class FALCONAssistant:

    def __init__(self):
        self.task_executor = FalconAI()
        self.db = FALCONDatabase()

    # 🌍 WORLD TIME
    def get_world_time(self, user_input):

        zones = {
            "india": "Asia/Kolkata",
            "usa": "America/New_York",
            "uk": "Europe/London",
            "dubai": "Asia/Dubai",
            "japan": "Asia/Tokyo"
        }

        for place, zone in zones.items():
            if place in user_input:
                now = datetime.datetime.now(ZoneInfo(zone))
                return f"Current time in {place.title()} is {now.strftime('%I:%M %p')}."

        if "time" in user_input:
            now = datetime.datetime.now()
            return f"Current time is {now.strftime('%I:%M %p')}."

        return None

    # ================= CORE ================= #

    def process_message(self, user_input):

        print("Input:", user_input)

        user_input = clean_command(user_input)

        print("Cleaned:", user_input)

        # TIME
        time_res = self.get_world_time(user_input)
        if time_res:
            return time_res

        # AUTOMATION
        keywords = [
            "open", "youtube", "google", "chatgpt",
            "notepad", "excel", "mute", "unmute",
            "shutdown", "restart", "lock",
            "date", "day", "today"
        ]

        if any(word in user_input for word in keywords):
            result = self.task_executor.run_task(user_input)
            return result if result else "Task completed"

        # AI CHAT
        cid = self.db.add_conversation(user_input)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": user_input}]
        )

        answer = response.choices[0].message.content
        self.db.update_response(cid, answer)

        return answer