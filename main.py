import os
import requests
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()

# === Переменные окружения ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VOX_ACCOUNT_ID = os.getenv("VOXIMPLANT_ACCOUNT_ID")
VOX_API_KEY = os.getenv("VOXIMPLANT_API_KEY")
TARGET_PHONE = os.getenv("TARGET_PHONE")  # +7XXXXXXXXXX

client = OpenAI(api_key=OPENAI_API_KEY)

# === Функция генерации текста ИИ ===
def get_ai_text():
    try:
        print("DEBUG: OPENAI_API_KEY =", OPENAI_API_KEY)  # проверяем, подтягивается ли ключ
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты дружелюбный ИИ-друг. Ты звонишь и просто спрашиваешь, как дела."},
                {"role": "user", "content": "Позвони мне и начни разговор"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Ошибка OpenAI:", e)  # выводим полную ошибку в лог
        return "Ошибка генерации текста ИИ"

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

# === Тест только OpenAI (без звонка) ===
@app.get("/call-test")
def call_test():
    text = get_ai_text()
    return {"ai_text": text}

# === Основной вызов с генерацией текста и звонком ===
@app.get("/call")
def make_call():
    ai_text = get_ai_text()
    vox_result = call_phone(ai_text)
    return {
        "ai_text": ai_text,
        "vox_response": vox_result
    }
