import os
import requests
from fastapi import FastAPI

app = FastAPI()

# === Переменные окружения ===
VOX_ACCOUNT_ID = os.getenv("VOXIMPLANT_ACCOUNT_ID")
VOX_API_KEY = os.getenv("VOXIMPLANT_API_KEY")
TARGET_PHONE = os.getenv("TARGET_PHONE")  # например +7XXXXXXXXXX

# === Текст, который будет произноситься ===
def get_ai_text():
    return "Привет, братан! Это тестовый звонок."

# === Запуск звонка через StartScenarios ===
def call_phone(text):
    try:
        url = "https://api.voximplant.com/platform_api/StartScenarios/"
        data = {
            "account_id": VOX_ACCOUNT_ID,
            "api_key": VOX_API_KEY,
            "rule_name": "bratela",  # имя твоего правила
            "script_custom_data": text,
            "phone": TARGET_PHONE
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
