from transformers import GPT2LMHeadModel, GPT2Tokenizer, MarianMTModel, MarianTokenizer

def translate_to_english(input_text):
    """
    日本語を英語に翻訳
    """
    print("Translating Japanese to English...")
    model_name_translation = "Helsinki-NLP/opus-mt-ja-en"  # 日本語→英語翻訳モデル
    tokenizer_translation = MarianTokenizer.from_pretrained(model_name_translation)
    model_translation = MarianMTModel.from_pretrained(model_name_translation)

    inputs = tokenizer_translation(input_text, return_tensors="pt", padding=True)
    translated_tokens = model_translation.generate(**inputs, max_length=100)
    translated_text = tokenizer_translation.decode(translated_tokens[0], skip_special_tokens=True)
    print("\nTranslated Text (English):\n", translated_text)
    return translated_text


def generate_code_from_english(input_text):
    """
    英語テキストからコードを生成
    """
    print("Generating code with GPT2-medium...")
    model_name_gpt2medium = "gpt2-medium"  # gpt2-mediumモデル
    tokenizer_gpt2medium = GPT2Tokenizer.from_pretrained(model_name_gpt2medium)  # Tokenizer should be initialized here
    model_gpt2medium = GPT2LMHeadModel.from_pretrained(model_name_gpt2medium)  # Model should be initialized separately

    inputs = tokenizer_gpt2medium(input_text, return_tensors="pt")
    
    # Ensure attention mask and pad_token_id are set
    inputs['attention_mask'] = inputs.get('attention_mask', None)
    model_gpt2medium.config.pad_token_id = model_gpt2medium.config.eos_token_id  # Set pad_token_id to eos_token_id
    
    # Generate output text
    outputs = model_gpt2medium.generate(inputs['input_ids'], max_length=200, num_return_sequences=1, attention_mask=inputs['attention_mask'])

    generated_code = tokenizer_gpt2medium.decode(outputs[0], skip_special_tokens=True)
    print("\nGenerated Code:\n", generated_code)
    
    return generated_code


if __name__ == "__main__":
    # サンプル入力 (日本語で記述)
    japanese_input = "pythonでハローワールドを出力するプログラムを書いて"

    # 日本語を英語に翻訳
    english_text = translate_to_english(japanese_input)

    # 英語を元にコードを生成
    generated_code = generate_code_from_english(english_text)