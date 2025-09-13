import re
import random
from typing import Optional
from data import ChatbotData
from utils import validate_time_format, normalize_time_str

class JusBookChatbot:
    def __init__(self):
        self.data = ChatbotData()

    def preprocess(self, text: str) -> str:
        return (text or "").lower().strip()

    def extract_keywords(self, text: str):
        return re.findall(r'\b\w+\b', text.lower())

    def detect_intent(self, text: str) -> str:
        t = self.preprocess(text)
        kws = self.extract_keywords(t)

        if any(w in t for w in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
            return "greeting"
        if any(k in kws for k in ["book", "booking", "reserve", "schedule", "appointment"]):
            return "booking"
        if any(k in kws for k in ["slot", "slots", "available", "availability", "when", "time"]):
            return "slots"
        if any(x in t for x in ["service", "services", "offer", "what do you offer", "what services"]):
            return "services"
        if any(k in kws for k in ["contact", "phone", "email", "address", "reach"]):
            return "contact"
        if any(k in kws for k in ["upcoming", "events", "scheduled", "next"]):
            return "upcoming"
        if "broadcast" in kws or "show all slots" in t:
            return "broadcast"
        return "default"

    def get_response(self, text: str) -> str:
        intent = self.detect_intent(text)
        if intent == "greeting":
            return random.choice(self.data.greetings)
        if intent == "services":
            return self._format_services()
        if intent == "contact":
            return self._format_contact()
        if intent == "slots":
            return self._format_available_slots()
        if intent == "upcoming":
            return self._format_upcoming()
        if intent == "broadcast":
            return self._format_available_slots(broadcast=True)
        if intent == "booking":
            return self._handle_booking(text)
        return random.choice(self.data.default_responses)

    def _format_services(self) -> str:
        out = ["📌 Here are the services we offer:"]
        for cat, items in self.data.services.items():
            out.append(f"\n{cat}")
            for s in items:
                out.append(f"   • {s}")
        return "\n".join(out)

    def _format_contact(self) -> str:
        c = self.data.contact_info
        return (
            f"📞 Contact Information:\n"
            f"📧 Email: {c['email']}\n"
            f"📱 Phone: {c['phone']}\n"
            f"📍 Address: {c['address']}\n"
            f"🕒 Hours: {c['hours']}\n"
            f"{c['website']}"
        )

    def _format_available_slots(self, broadcast: bool=False) -> str:
        header = "📢 Slot Broadcast — All Available Slots This Week:" if broadcast else "✅ Available booking slots:"
        out = [header]
        for day, times in self.data.available_slots.items():
            times_str = " | ".join(times) if times else "❌ No slots"
            out.append(f"📅 {day}: ⏰ {times_str}")
        return "\n".join(out)

    def _format_upcoming(self) -> str:
        if not self.data.upcoming_events:
            return "📭 No upcoming events or bookings."
        out = ["📅 Upcoming events and bookings:"]
        for e in self.data.upcoming_events:
            line = f"• {e['title']} — {e['date']} at {e['time']}"
            if e.get("description"):
                line += f"\n   📝 {e['description']}"
            out.append(line)
        return "\n".join(out)

    def _find_day_in_text(self, text: str) -> Optional[str]:
        t = text.lower()
        for d in self.data.available_slots.keys():
            if d.lower() in t or d[:3].lower() in t:
                return d
        return None

    def _find_time_in_text(self, text: str) -> Optional[str]:
        m = re.search(r'(\d{1,2}(:\d{2})?\s?(am|pm)?)', text, flags=re.I)
        if m:
            return normalize_time_str(m.group(1))
        return None

    def _find_service_in_text(self, text: str) -> Optional[str]:
        t = text.lower()
        for cat, services in self.data.services.items():
            for s in services:
                if s.lower() in t:
                    return s
        for cat, services in self.data.services.items():
            for s in services:
                words = s.lower().split()
                if any(w in t for w in words):
                    return s
        return None

    def _handle_booking(self, text: str) -> str:
        day = self._find_day_in_text(text)
        time = self._find_time_in_text(text)
        service = self._find_service_in_text(text)

        if not (day or time or service):
            return (
                "📖 Sure — I can help you book an appointment.\n"
                "👉 Please tell me:\n"
                "   • Day (e.g., Monday)\n"
                "   • Time (e.g., 9:00 AM)\n"
                "   • Service you'd like\n\n"
                f"{self._format_available_slots()}"
            )

        if time and not validate_time_format(time):
            return "⚠️ I couldn’t interpret that time. Use formats like '9:00 AM' or '2:30 PM'."

        if not time:
            return "⏰ Please include a preferred time. Available slots:\n" + self._format_available_slots()

        if not day:
            possible = [d for d, times in self.data.available_slots.items() if time in times]
            if len(possible) == 1:
                day = possible[0]
        if not day:
            return "📅 Which day would you like? For example: Monday, Tuesday, etc."

        if not service:
            return "💼 Which service would you like to book? Options: " + ", ".join(
                [s for cat in self.data.services.values() for s in cat]
            )

        available_times = self.data.available_slots.get(day, [])
        if time not in available_times:
            return f"❌ {time} on {day} is not available.\n✅ Available on {day}: {', '.join(available_times) if available_times else 'no slots'}"

        # Confirm booking
        self.data.available_slots[day].remove(time)
        booking = {
            "title": f"{service} (Booking)",
            "date": day,
            "time": time,
            "description": f"Booked service: {service}"
        }
        self.data.upcoming_events.append(booking)

        return (
            f"✅ Booking Confirmed!\n"
            f"📌 Service: {service}\n"
            f"📅 Day: {day}\n"
            f"⏰ Time: {time}\n"
            f"📝 Status: Added to your upcoming events\n\n"
            f"Thank you for booking with JusBook! 🎉"
        )
