import google.generativeai as genai
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'src'))
from virtual_lab.constants import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

print("Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Name: {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")
