import os
import requests
from fastapi import FastAPI

app = FastAPI()

VOX_ACCOUNT_ID = os.getenv("VOXIMPLANT_ACCOUNT_ID")
VOX_API_KEY = os.getenv("VOXIMPLANT_API_KEY")
TARGET_PHONE = os.getenv("TARGET_PHONE")  # например +7XXXXXXXXXX

def get_test_text():
    return "Привет, братан! Это тестовый звонок."

def call_phone(text):
    try:
        url = "https://api.voximplant.com/platform_api/StartScenarios/"
        data = {
            "account_id": VOX_ACCOUNT_ID,
            "api_key": VOX_API_KEY,
            "rule_name": "outbound_call_rule",  # имя правила, которое ты создал
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
    text = get_test_text()
    return {"ai_text": text}

@app.get("/call")
def make_call():
    text = get_test_text()
    result = call_phone(text)
    return {
        "ai_text": text,
        "vox_response": result
    }
