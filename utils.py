import json
import logging
from datetime import datetime
import re

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("chatbot.log"), logging.StreamHandler()]
    )
    return logging.getLogger("jusbook")

def save_conversation(user_message: str, bot_response: str, filename: str="conversations.jsonl"):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_message": user_message,
        "bot_response": bot_response
    }
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        logging.exception("Failed to write conversation")

def validate_time_format(t: str) -> bool:
    if not t:
        return False
    pattern = r'^(0?[1-9]|1[0-2])(:[0-5][0-9])?\s?(am|pm)$'
    return re.match(pattern, t.strip().lower()) is not None

def normalize_time_str(t: str) -> str:
    if not t:
        return ""
    t = t.strip().lower().replace(".", "")
    m = re.match(r'^(\d{1,2})(:(\d{2}))?\s*(am|pm)?$', t)
    if not m:
        return t.upper()
    hour = int(m.group(1))
    mins = m.group(3) or "00"
    ampm = (m.group(4) or "").upper()
    if not ampm:
        ampm = "AM"
    return f"{hour}:{mins} {ampm}"
