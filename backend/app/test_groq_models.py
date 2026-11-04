
from groq import Groq
from app.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

print("Checking available Groq models...\n")

models = client.models.list()

for model in models.data:
    if model.active:
        print(model.id)
