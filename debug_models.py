from google import genai
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'src'))
from virtual_lab.constants import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

print("Listing available models...")
try:
    for m in client.models.list():
        print(f"Name: {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")
