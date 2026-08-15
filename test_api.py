import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GEMINI_API_KEY")

print("Key found:", key is not None)

if key:
    print("Key starts with:", key[:8])