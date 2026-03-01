import os
import requests
from fastapi import FastAPI

app = FastAPI()

# === Переменные окружения (через Railway / .env) ===
VOX_ACCOUNT_ID = os.getenv("VOXIMPLANT_ACCOUNT_ID")
VOX_API_KEY = os.getenv("VOXIMPLANT_API_KEY")
TARGET_PHONE = os.getenv("TARGET_PHONE")  # +7XXXXXXXXXX

# === Получение текста ИИ / тестового текста ===
def get_ai_text():
    return "Привет, братан! Это тестовый звонок."

# === Вызов Voximplant ===
def call_phone(text):
    try:
        url = "https://api.voximplant.com/platform_api/StartScenarios/"
        # Передаём объект JSON, чтобы JS получил phone и text
        import json
        custom_data = json.dumps({
            "phone": TARGET_PHONE,
            "text": text
        })
        data = {
            "account_id": VOX_ACCOUNT_ID,
            "api_key": VOX_API_KEY,
            "rule_name": "outbound_call_rule",  # имя твоего правила
            "script_custom_data": custom_data
        }
        response = requests.post(url, data=data)
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
