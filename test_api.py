from openai import OpenAI

client = OpenAI(api_key="APIKey")

# APIキーをセット
  # 取得したAPIキーをここに貼り付ける

# チャットモデル（GPT-4）を呼び出す
response = client.chat.completions.create(model="gpt-4o-mini",
messages=[
  {"role": "system", "content": "You are a helpful assistant."},
  {"role": "user", "content": "C言語でHello Worldを出力するコードを書いて"},
])

# 応答の出力
print(response.choices[0].message.content)