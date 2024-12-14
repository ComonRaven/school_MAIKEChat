from transformers import MarianMTModel, MarianTokenizer

# モデル名の指定 (日本語 → 英語の翻訳)
model_name = "Helsinki-NLP/opus-mt-ja-en"

# トークナイザーとモデルのロード
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# 翻訳したい日本語テキスト
japanese_texts = [
    "2次方程式 ax^2 + bx + c = 0 の係数を入力してください。",
    "このモデルは日本語を英語に翻訳します。",
    "わかなちゃんはとても可愛いです。",
]

# テキストをトークン化
inputs = tokenizer(japanese_texts, return_tensors="pt", padding=True, truncation=True)

# 翻訳を生成
translated = model.generate(**inputs)

# 結果をデコード
english_translations = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]

# 翻訳結果を表示
for ja, en in zip(japanese_texts, english_translations):
    print(f"日本語: {ja}")
    print(f"英語: {en}")
    print("-" * 40)