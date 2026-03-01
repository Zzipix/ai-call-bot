import os
import requests
from fastapi import FastAPI

app = FastAPI()

# === Переменные окружения ===
VOX_ACCOUNT_ID = os.getenv("VOXIMPLANT_ACCOUNT_ID")
VOX_API_KEY = os.getenv("VOXIMPLANT_API_KEY")
TARGET_PHONE = os.getenv("TARGET_PHONE")  # +7XXXXXXXXXX

# === Функция генерации текста (тестовый фиксированный текст) ===
def get_ai_text():
    return "Привет, братан! Это тестовый звонок."

# === Функция вызова телефона через Voximplant ===
def call_phone(text):
    try:
        url = "https://api.voximplant.com/platform_api/StartScenarios/"
        data = {
            "account_id": VOX_ACCOUNT_ID,
            "api_key": VOX_API_KEY,
            "rule_name": "ai_call",  # убедись, что такой сценарий есть в Voximplant
            "script_custom_data": text,
            "phone": TARGET_PHONE
        }
        response = requests.post(url, data=data)
        return response.text
    except Exception as e:
        print("Ошибка Voximplant:", e)
        return "Ошибка при вызове звонка"

# === Главная проверка сервера ===
@app.get("/")
def root():
    return {"status": "alive"}

# === Тест только текста (без звонка) ===
@app.get("/call-test")
def call_test():
    text = get_ai_text()
    return {"ai_text": text}

# === Основной вызов с тестовым текстом и звонком ===
@app.get("/call")
def make_call():
    ai_text = get_ai_text()
    vox_result = call_phone(ai_text)
    return {
        "ai_text": ai_text,
        "vox_response": vox_result
    }
