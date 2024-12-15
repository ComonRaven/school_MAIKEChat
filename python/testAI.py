from transformers import AutoTokenizer, AutoModelForCausalLM, T5ForConditionalGeneration, T5Tokenizer

# 1. T5: プロンプトを解析して意図を抽出
t5_tokenizer = T5Tokenizer.from_pretrained("t5-small")
t5_model = T5ForConditionalGeneration.from_pretrained("t5-small")

def analyze_prompt(prompt):
    input_text = f"paraphrase: {prompt} </s>"
    input_ids = t5_tokenizer.encode(input_text, return_tensors="pt")
    outputs = t5_model.generate(input_ids, max_new_tokens=64, num_beams=4, pad_token_id=t5_tokenizer.eos_token_id)
    return t5_tokenizer.decode(outputs[0], skip_special_tokens=True)

# 2. CodeGen: 解析結果を元にコードを生成
codegen_tokenizer = AutoTokenizer.from_pretrained("Salesforce/codegen-350M-multi")
codegen_model = AutoModelForCausalLM.from_pretrained("Salesforce/codegen-350M-multi")

def generate_code(parsed_prompt):
    input_ids = codegen_tokenizer(parsed_prompt, return_tensors="pt").input_ids
    generated_ids = codegen_model.generate(input_ids, max_new_tokens=128, num_beams=4, pad_token_id=codegen_tokenizer.eos_token_id)
    return codegen_tokenizer.decode(generated_ids[0], skip_special_tokens=True)

# 3. PolyCoder: 生成されたコードを補完および最適化
polycoder_tokenizer = AutoTokenizer.from_pretrained("NinedayWang/PolyCoder-160M")
polycoder_model = AutoModelForCausalLM.from_pretrained("NinedayWang/PolyCoder-160M")

def optimize_code(generated_code):
    input_ids = polycoder_tokenizer(generated_code, return_tensors="pt").input_ids
    optimized_ids = polycoder_model.generate(input_ids, max_new_tokens=128, num_beams=4, pad_token_id=polycoder_tokenizer.eos_token_id)
    return polycoder_tokenizer.decode(optimized_ids[0], skip_special_tokens=True)

# メイン処理: プロンプトからコード生成と補完を実行
prompt = "Please write a function to calculate the factorial of a number to use C language."
print("Original Prompt:", prompt)

# ステップ 1: プロンプト解析
parsed_prompt = analyze_prompt(prompt)
print("\nParsed Prompt:", parsed_prompt)

# ステップ 2: コード生成
generated_code = generate_code(parsed_prompt)
print("\nGenerated Code:\n", generated_code)

# ステップ 3: コード補完と最適化
optimized_code = optimize_code(generated_code)
print("\nOptimized Code:\n", optimized_code)