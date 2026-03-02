import os
import requests
from fastapi import FastAPI
import json

app = FastAPI()

# === Переменные окружения (Railway / .env) ===
VOX_ACCOUNT_ID = os.getenv("VOXIMPLANT_ACCOUNT_ID")
VOX_API_KEY = os.getenv("VOXIMPLANT_API_KEY")
TARGET_PHONE = os.getenv("TARGET_PHONE")  # +7XXXXXXXXXX

# === Текст для звонка ===
def get_ai_text():
    return "Привет, братан! Это тестовый звонок."

# === Вызов Voximplant StartScenarios ===
def call_phone(text):
    try:
        url = "https://api.voximplant.com/platform_api/StartScenarios/"
        # JSON с номером и текстом
        custom_data = json.dumps({
            "phone": TARGET_PHONE,
            "text": text
        })
        payload = {
            "account_id": VOX_ACCOUNT_ID,
            "api_key": VOX_API_KEY,
            "rule_name": "outbound_call_rule",  # имя твоего правила
            "script_custom_data": custom_data
        }
        response = requests.post(url, data=payload)
        return response.text
    except Exception as e:
        print("Ошибка Voximplant:", e)
        return "Ошибка при вызове звонка"

@app.get("/")
def root():
    return {"status": "alive"}

@app.get("/call-test")
def call_test():
    text = get_ai_text()
    return {"ai_text": text}

@app.get("/call")
def make_call():
    text = get_ai_text()
    vox_result = call_phone(text)
    return {
        "ai_text": text,
        "vox_response": vox_result
    }
