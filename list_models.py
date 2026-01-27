import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

for m in client.models.list():
    # m.name 예: "models/gemini-2.0-flash" 같은 형태로 나올 수 있음
    print(m.name, getattr(m, "supported_generation_methods", None))
