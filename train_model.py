from transformers import T5ForConditionalGeneration, RobertaTokenizer
from datasets import load_dataset
from transformers import Trainer, TrainingArguments

# ローカルデータセットの読み込み
dataset = load_dataset('json', data_files='local_datasets/printf.json')

# モデルとトークナイザーのロード
model = T5ForConditionalGeneration.from_pretrained('Salesforce/codet5-base')
tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-base')  # T5Tokenizer から RobertaTokenizer に変更

# データをトークン化
def tokenize_function(examples):
    # 入力と出力両方をトークン化
    inputs = tokenizer(examples['input'], padding="max_length", truncation=True)
    outputs = tokenizer(examples['output'], padding="max_length", truncation=True)
    
    # 出力をlabelsとして設定
    inputs['labels'] = outputs['input_ids']
    return inputs

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# 手動でtrain/validationに分割
train_dataset = tokenized_datasets['train']
val_dataset = train_dataset.shuffle(seed=42).select([i for i in list(range(int(0.8 * len(train_dataset))))])  # 80% for training

# トレーニング設定
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=1,  # エポック数を1に変更
    per_device_train_batch_size=2,  # バッチサイズを2に変更
    save_steps=10_000,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,  # 手動で作成したバリデーションセット
)

trainer.train()