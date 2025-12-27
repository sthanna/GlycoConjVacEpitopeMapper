import google.generativeai as genai
import os

api_key = "AIzaSyB3SBv3W4hUyD085Zt9SPcQ1SDVg72JhoE"
genai.configure(api_key=api_key)

try:
    print("Listing models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model: {m.name}, Display Name: {m.display_name}")
except Exception as e:
    print(f"Error: {e}")
