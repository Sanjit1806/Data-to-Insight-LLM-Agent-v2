"""
Test script to check which Gemini models work with your API key.
Uses direct REST API calls to avoid SDK version conflicts.
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Models to test (current free-tier models as of Aug 2026)
models_to_test = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-pro",
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.6-flash",
]

test_prompt = "What is 2+2? Reply with just the number."

print("=" * 60)
print("TESTING GEMINI MODELS WITH YOUR API KEY")
print(f"API Key: {API_KEY[:10]}...{API_KEY[-4:]}")
print("=" * 60)
print()

working_models = []

for model_name in models_to_test:
    print(f"Testing: {model_name}...", end=" ", flush=True)
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": test_prompt}]
        }],
        "generationConfig": {
            "temperature": 0,
            "maxOutputTokens": 50
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            print(f"SUCCESS! Response: {text}")
            working_models.append(model_name)
        elif response.status_code == 429:
            print(f"RATE LIMITED (quota exhausted)")
        elif response.status_code == 404:
            print(f"MODEL NOT FOUND")
        elif response.status_code == 403:
            print(f"PERMISSION DENIED")
        else:
            error_msg = response.json().get("error", {}).get("message", "Unknown error")
            print(f"ERROR ({response.status_code}): {error_msg[:80]}")
    except requests.exceptions.Timeout:
        print("TIMEOUT")
    except Exception as e:
        print(f"ERROR: {str(e)[:80]}")

print()
print("=" * 60)
print("RESULTS:")
print("=" * 60)
if working_models:
    print(f"\nWorking models: {', '.join(working_models)}")
    print(f"\nBest for your project: {working_models[0]}")
    print(f"\nUpdate agent.py model to: {working_models[0]}")
else:
    print("\nNo models worked. Your API key may need a fresh quota reset.")
    print("Try generating a new key at: https://aistudio.google.com/apikey")
