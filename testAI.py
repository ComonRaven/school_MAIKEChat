import json
from transformers import T5ForConditionalGeneration, T5Tokenizer

# 微調整後のモデルをロード
model = T5ForConditionalGeneration.from_pretrained("./results")
tokenizer = T5Tokenizer.from_pretrained('Salesforce/codet5-base')

# データセットの読み込み
with open('datasets/printf.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

# テストの実行
for example in dataset:
    input_text = example['input']
    output_text = example['output']

    # プロンプトをトークナイズ
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids
    output_ids = tokenizer(output_text, return_tensors="pt").input_ids

    # コードを生成
    generated_ids = model.generate(input_ids, max_length=100, num_beams=5, do_sample=False, top_p=0.95, temperature=0.1)
    generated_code = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

    # 結果を表示
    print(f"Prompt: {input_text}")
    print(f"Generated Code: {generated_code}")
    print(f"Expected Output: {output_text}")
    print("-" * 50)