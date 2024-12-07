from transformers import AutoModelForCausalLM, AutoTokenizer

def main():
    # モデルとトークナイザーのロード
    model_name = "gpt2"  # GPT-2 Small モデル
    model = AutoModelForCausalLM.from_pretrained("saved_model")
    tokenizer = AutoTokenizer.from_pretrained("saved_model")
    #model = AutoModelForCausalLM.from_pretrained(model_name)
    #tokenizer = AutoTokenizer.from_pretrained(model_name)

    # pad_tokenを設定
    tokenizer.pad_token = tokenizer.eos_token

    # テスト用のプロンプト
    prompt = "C言語でHello Worldを書いて"

    # トークン化
    inputs = tokenizer(prompt, return_tensors="pt", padding=True)

    # テキスト生成
    output = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],  # attention_maskを指定
        max_length=50,  # 出力の最大長
        num_return_sequences=1,  # 生成するシーケンス数
        temperature=0.7,  # 生成の多様性を制御
        top_p=0.9,  # nucleus sampling のパラメータ
        do_sample=True,  # サンプリングを有効化
    )

    # 出力のデコード
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    # 結果を表示
    print("Generated Text:")
    print(generated_text)

if __name__ == "__main__":
    main()