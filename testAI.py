import json
from transformers import T5ForConditionalGeneration, T5Tokenizer

# 微調整後のモデルとトークナイザーをロード
model = T5ForConditionalGeneration.from_pretrained("./saved_model")
tokenizer = T5Tokenizer.from_pretrained("google/t5-small")

# 任意のプロンプトに対して処理を行う関数
def generate_code(input_text):
    # 入力テキストをトークナイズ
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    # コードを生成（パラメータを調整）
    generated_ids = model.generate(input_ids, max_length=100, num_beams=5, do_sample=True, top_p=0.95, temperature=0.7)
    generated_code = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

    return generated_code

# 任意のプロンプトに対する処理の実行
while True:
    user_input = input("Enter a prompt (or type 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break

    generated_code = generate_code(user_input)

    # 結果を表示
    print(f"Prompt: {user_input}")
    print(f"Generated Code: {generated_code}")
    print("-" * 50)