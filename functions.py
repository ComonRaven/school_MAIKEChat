import eel
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, MarianMTModel, MarianTokenizer

# GPUデバイスの指定
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# モデルとトークナイザーのロード (グローバルスコープ)
marian_model_name = "Helsinki-NLP/opus-mt-ja-en"
marian_tokenizer = MarianTokenizer.from_pretrained(marian_model_name)
marian_model = MarianMTModel.from_pretrained(marian_model_name).to(device)

codegen_model_name = "Salesforce/codegen-350M-mono"
codegen_tokenizer = AutoTokenizer.from_pretrained(codegen_model_name, legacy=False)

# pad_token が存在しない場合に設定
if codegen_tokenizer.pad_token is None:
    codegen_tokenizer.pad_token = codegen_tokenizer.eos_token

codegen_model = AutoModelForCausalLM.from_pretrained(codegen_model_name).to(device)

# 日本語翻訳関数
def translate_japanese_to_english(japanese_text):
    inputs = marian_tokenizer(japanese_text, return_tensors="pt", padding=True, truncation=True)
    input_ids = inputs.input_ids.to(device)
    attention_mask = inputs.attention_mask.to(device)
    translated = marian_model.generate(input_ids=input_ids, attention_mask=attention_mask)
    translated_decode = [marian_tokenizer.decode(t, skip_special_tokens=True) for t in translated]
    return translated_decode[0]  # 1つの翻訳結果を返す

# コード生成関数
def generate_code(parsed_prompt):
    inputs = codegen_tokenizer(parsed_prompt, return_tensors="pt", padding=True, truncation=True)
    input_ids = inputs.input_ids.to(device)

    outputs = codegen_model.generate(
        input_ids=input_ids,
        max_new_tokens=128,
        num_beams=4,
        pad_token_id=codegen_tokenizer.pad_token_id
    )
    return codegen_tokenizer.decode(outputs[0], skip_special_tokens=True)

@eel.expose
def process_input(input_text):
    try:
        # 日本語翻訳
        translated_text = translate_japanese_to_english(input_text)
        print("\nTranslated Prompt:", translated_text)

        # コード生成
        generated_code = generate_code(translated_text)
        print("\nGenerated Code:\n", generated_code)

        return generated_code
    except Exception as e:
        print("Error:", str(e))
        return f"Error occurred: {str(e)}"