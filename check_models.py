from google import genai
import os

api_key = "AIzaSyAarvWr0hFZWw6fOSxnGpkMMmXPudtYHdU"
client = genai.Client(api_key=api_key)

try:
    print("Listing models...")
    for m in client.models.list():
        print(f"Model: {m.name}, Display Name: {m.display_name}")
except Exception as e:
    print(f"Error: {e}")
