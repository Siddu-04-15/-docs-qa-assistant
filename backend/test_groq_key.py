
from app.config import settings

if settings.GROQ_API_KEY:
    print("Groq API key loaded successfully!")
    print("Key length:", len(settings.GROQ_API_KEY))
    print("Key starts correctly:", settings.GROQ_API_KEY.startswith("gsk_"))
else:
    print("Groq API key was NOT loaded!")
