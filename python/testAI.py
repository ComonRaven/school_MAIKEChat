import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, T5ForConditionalGeneration, T5Tokenizer

# GPUデバイスの指定
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# 共通の生成関数
def generate_text(model, tokenizer, input_text, max_new_tokens=128, num_beams=4):
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(device)
    outputs = model.generate(
        input_ids, 
        max_new_tokens=max_new_tokens, 
        num_beams=num_beams, 
        pad_token_id=tokenizer.eos_token_id
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# ステップ 1: T5でプロンプト解析
def analyze_prompt(prompt):
    t5_tokenizer = T5Tokenizer.from_pretrained("t5-small")
    t5_model = T5ForConditionalGeneration.from_pretrained("t5-small").to(device)
    input_text = f"paraphrase: {prompt} </s>"
    result = generate_text(t5_model, t5_tokenizer, input_text, max_new_tokens=64)
    del t5_model  # モデルのメモリ解放
    torch.cuda.empty_cache()
    return result

# ステップ 2: CodeGenでコード生成
def generate_code(parsed_prompt):
    codegen_tokenizer = AutoTokenizer.from_pretrained("Salesforce/codegen-350M-multi")
    codegen_model = AutoModelForCausalLM.from_pretrained("Salesforce/codegen-350M-multi").to(device)
    result = generate_text(codegen_model, codegen_tokenizer, parsed_prompt)
    del codegen_model  # メモリ解放
    torch.cuda.empty_cache()
    return result

# メイン処理
if __name__ == "__main__":
    prompt = "Please write a function to calculate the factorial of a number to use python."
    print("Original Prompt:", prompt)

    # ステップ 1: プロンプト解析
    parsed_prompt = analyze_prompt(prompt)
    print("\nParsed Prompt:", parsed_prompt)

    # ステップ 2: コード生成
    generated_code = generate_code(parsed_prompt)
    print("\nGenerated Code:\n", generated_code)