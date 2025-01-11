import subprocess
import eel
from openai import OpenAI

# OpenAI APIキーの設定
client = OpenAI(api_key="APIKey")


@eel.expose
def get_generated_code(text):
    response = client.chat.completions.create(model="gpt-4o-mini", # モデルの指定 40-mini or 40
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": text},
    ])
    return response.choices[0].message.content