import os
import requests
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()

# === КЛЮЧИ ИЗ ENV ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VOX_ACCOUNT_ID = os.getenv("VOXIMPLANT_ACCOUNT_ID")
VOX_API_KEY = os.getenv("VOXIMPLANT_API_KEY")
TARGET_PHONE = os.getenv("TARGET_PHONE")  # +7XXXXXXXXXX

client = OpenAI(api_key=OPENAI_API_KEY)


def get_ai_text():
    """Что скажет ИИ"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Ты дружелюбный ИИ-друг. Звонишь и просто спрашиваешь, как дела."
            },
            {
                "role": "user",
                "content": "Позвони мне и начни разговор"
            }
        ]
    )
    return response.choices[0].message.content


def call_phone(text):
    """Инициируем звонок через Voximplant"""
    url = "https://api.voximplant.com/platform_api/StartScenarios/"
    payload = {
        "account_id": VOX_ACCOUNT_ID,
        "api_key": VOX_API_KEY,
        "rule_name": "ai_call",
        "script_custom_data": text,
        "phone": TARGET_PHONE
    }
    r = requests.post(url, data=payload)
    return r.text


@app.get("/")
def root():
    return {"status": "alive"}


@app.get("/call")
def make_call():
    ai_text = get_ai_text()
    result = call_phone(ai_text)
    return {
        "message": "call started",
        "ai_text": ai_text,
        "vox_response": result
    }
