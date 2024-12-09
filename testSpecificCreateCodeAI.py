from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained GPT-2 Medium model and tokenizer
model_name = "gpt2-medium"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Encode input text (your prompt)
input_text = "Write a function to add two numbers in C language."

inputs = tokenizer(input_text, return_tensors="pt")

# Ensure attention mask and pad_token_id are set
inputs['attention_mask'] = inputs['attention_mask'] if 'attention_mask' in inputs else None
model.config.pad_token_id = model.config.eos_token_id  # Set pad_token_id to eos_token_id

# Generate output text
outputs = model.generate(inputs['input_ids'], max_length=50, num_return_sequences=1, attention_mask=inputs['attention_mask'])

# Decode the generated output
generated_code = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(generated_code)