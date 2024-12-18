import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
def generate_code(parsed_prompt):
    # トークナイザーのロード
    codegen_tokenizer = AutoTokenizer.from_pretrained("Salesforce/codegen-2B-mono", legacy=False)

    # モデルのロード
    codegen_model = AutoModelForCausalLM.from_pretrained("Salesforce/codegen-2B-mono")
    codegen_model = torch.quantization.quantize_dynamic(
        codegen_model,  # モデル本体
        {torch.nn.Linear},  # 量子化対象のレイヤー
        dtype=torch.qint8  # 量子化後のデータ型
    ).to(device)

    # 推論実行
    inputs = codegen_tokenizer(parsed_prompt, return_tensors="pt", padding=True, truncation=True)
    input_ids = inputs.input_ids.to(device)
    attention_mask = inputs.attention_mask.to(device)
    
    outputs = codegen_model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_new_tokens=128,
        num_beams=4,
        pad_token_id=codegen_tokenizer.eos_token_id
    )
    
    result = codegen_tokenizer.decode(outputs[0], skip_special_tokens=True)

    # メモリ解放
    del codegen_model
    torch.cuda.empty_cache()

    return result
  
generate_code("Please write a function to calculate the factorial of a number to use python.")