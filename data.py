class ChatbotData:
    def __init__(self):
        self.greetings = [
            "👋 Hello! Welcome to JusBook — your smart booking assistant. How can I help today?",
            "✨ Hi there! I can assist with bookings, services, available slots, and contact info.",
            "🤖 JusBook Assistant at your service! Ask me about slots, services, or upcoming events."
        ]

        self.default_responses = [
            "🤔 I didn’t catch that. Try asking about services, slots, booking, or contact info.",
            "💡 You can ask me things like: 'Show slots', 'Book Monday 10 AM Business Consultation', or 'Contact details'."
        ]

        self.services = {
            "💼 Consulting": [
                "Business Consultation",
                "Legal Advisory",
                "Financial Planning",
                "Strategic Planning"
            ],
            "📊 Bookkeeping": [
                "Monthly Bookkeeping",
                "Tax Preparation",
                "Financial Reporting",
                "Payroll Services"
            ],
            "⚖️ Legal": [
                "Contract Review",
                "Legal Documentation",
                "Compliance Services",
                "Legal Research"
            ]
        }

        self.contact_info = {
            "email": "info@jusbook.com",
            "phone": "+1 (555) 123-4567",
            "address": "123 Business Street, Suite 100, City, State 12345",
            "hours": "Mon–Fri ⏰ 9:00 AM – 6:00 PM",
            "website": "🌐 https://www.jusbook.com"
        }

        self.available_slots = {
            "Monday": ["9:00 AM", "11:00 AM", "2:00 PM", "4:00 PM"],
            "Tuesday": ["10:00 AM", "1:00 PM", "3:00 PM", "5:00 PM"],
            "Wednesday": ["9:00 AM", "12:00 PM", "2:00 PM", "4:30 PM"],
            "Thursday": ["10:30 AM", "1:30 PM", "3:30 PM", "5:00 PM"],
            "Friday": ["9:00 AM", "11:30 AM", "2:30 PM", "4:00 PM"]
        }

        self.upcoming_events = [
            {
                "title": "📅 Monthly Business Review",
                "date": "December 15, 2024",
                "time": "2:00 PM",
                "description": "Quarterly business performance review session"
            },
            {
                "title": "💰 Tax Planning Workshop",
                "date": "December 20, 2024",
                "time": "10:00 AM",
                "description": "Year-end tax planning and preparation workshop"
            }
        ]
