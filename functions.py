import subprocess
import eel
from openai import OpenAI

# OpenAI APIキーの設定
client = OpenAI(api_key="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")


@eel.expose
def get_generated_code(text):
  response = client.chat.completions.create(model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": text},
  ])
  return response.choices[0].message.content