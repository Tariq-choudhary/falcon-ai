import eel
import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import backend modules
try:
    from Backend.Brain import FALCONAssistant
    from Backend.TTS import SpeakFalcon
    from Database.Database import save_conversation
except Exception as e:
    print(f"❌ Critical Import Error: {e}")
    sys.exit(1)

# Initialize Assistant
try:
    print("🚀 Initializing FALCON Assistant...")
    assistant = FALCONAssistant()
    print("✅ FALCON Assistant initialized successfully.")
except Exception as e:
    print(f"❌ Error initializing FALCONAssistant: {e}")
    sys.exit(1)

# Verify web folder
web_folder = os.path.join(current_dir, 'web')
if not os.path.isdir(web_folder):
    print("❌ Web folder not found.")
    sys.exit(1)

eel.init(web_folder)

# -----------------------------------------
# PROCESS USER QUERY
# -----------------------------------------
@eel.expose
def process_user_query(user_query_text: str):

    print(f"\n🟡 Received Query: {user_query_text}")

    if not user_query_text or not user_query_text.strip():
        print("⚠️ Empty input received")
        return {'response': "Please say something.", 'should_speak': True}

    try:
        # Process query
        response = assistant.process_message(user_query_text)

        if not response:
            response = "I couldn't process that."

        print(f"🟢 Response: {response}")

        # Save to database
        try:
            save_conversation(user_query_text, response)
            print("💾 Conversation saved")
        except Exception as db_error:
            print(f"⚠️ Database Error: {db_error}")

        return {'response': response, 'should_speak': True}

    except Exception as e:
        print(f"❌ Processing Error: {e}")
        return {'response': "Something went wrong.", 'should_speak': True}


# -----------------------------------------
# TEXT TO SPEECH
# -----------------------------------------
@eel.expose
def request_tts(text_to_speak: str):

    print(f"🔊 Speaking: {text_to_speak}")

    if text_to_speak and text_to_speak.strip():
        try:
            SpeakFalcon(text_to_speak)
        except Exception as e:
            print(f"❌ TTS Error: {e}")
    else:
        print("⚠️ Empty TTS request ignored")


# -----------------------------------------
# START APPLICATION
# -----------------------------------------
if __name__ == '__main__':

    print("\n🌐 Starting FALCON UI...")
    print("👉 Open browser at http://localhost:8000")

    try:
        eel.start(
            'index.html',
            size=(990, 540),
            host='localhost',
            port=8000,
            block=True
        )

    except Exception as e:
        print(f"❌ Failed to start UI: {e}")