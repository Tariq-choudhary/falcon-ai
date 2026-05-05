Here’s a cleaner, more professional rewrite of your setup guide:

---

# 🚀 FALCON AI Assistant – Setup Guide

Follow the steps below to install and run **FALCON AI Assistant** on your system.

---

## 1️⃣ Install Python 3.11

* Download and install **Python 3.11** for your operating system.
* On Windows, make sure to check **“Add Python to PATH”** during installation.
* Verify the installation in your terminal:

```bash
python --version
```

📥 Download link (Windows x64):
[https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe](https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe)

---

## 2️⃣ Create a Virtual Environment

Inside your project folder, run:

```bash
  py -3.11 -m venv .venv
```

---

## 3️⃣ Activate the Virtual Environment

* **Windows (Command Prompt / PowerShell):**

  ```bash
  .venv\Scripts\activate
  ```
* **macOS/Linux:**

  ```bash
  source .venv/bin/activate
  ```

---

## 4️⃣ Upgrade pip (recommended)

```bash
python -m pip install --upgrade pip
```

---

## 5️⃣ Install Project Dependencies

```bash
pip install -r requirements.txt
```

---

## 6️⃣ Set Environment Variables

Create a `.env` file in the project root with the following content:

```env
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

*(Replace with your actual API keys.)*

---

## 7️⃣ Run the Application

```bash
python Falcon.py
```

Once started, open your browser and go to:
[http://localhost:8000](http://localhost:8000)

---


Your Falcon Level 1 is now officially working.

You now have:

✅ Open apps
✅ Open folders
✅ Open websites
✅ Time (local + world)
✅ Date & day
✅ Mute / Unmute
✅ Lock
✅ Sleep
✅ Restart
✅ Shutdown
✅ AI chat with memory

That’s actually a solid assistant foundation.