# JusBook AI Chatbot

Lightweight rule-based chatbot for jusbook.com.

Files:
- app.py
- chatbot.py
- data.py
- utils.py
- templates/index.html

Run (Windows, VS Code / PowerShell):

1. Open folder in VS Code.
2. Open integrated terminal (Ctrl+`).
3. Create & activate venv:
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   (If activation blocked: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned)
4. Install dependencies:
   pip install -r requirements.txt
5. Run:
   python app.py
   or
   uvicorn app:app --reload --host 127.0.0.1 --port 8000
6. Open http://localhost:8000

Notes:
- Booking updates in-memory slots and appends to upcoming events.
- UI does not show apology/error bot messages; server always returns a friendly response on failure.
- For persistence add a DB (sqlite) and adapt save_conversation/booking logic.
