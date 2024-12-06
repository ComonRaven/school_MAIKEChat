import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset, concatenate_datasets
from transformers import Trainer, TrainingArguments
from huggingface_hub import login

# local_datasets内の全てのjsonファイルを取得
dataset_files = [f'local_datasets/{file}' for file in os.listdir('local_datasets') if file.endswith('.json')]

# データセットをロードして統合
datasets = []
for file in dataset_files:
    dataset = load_dataset('json', data_files=file)
    datasets.append(dataset['train'])

# 複数のデータセットを統合
full_dataset = concatenate_datasets(datasets)

# Hugging Face Hubにログイン
login("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")

# モデルとトークナイザーのロード
model = AutoModelForCausalLM.from_pretrained("bigcode/starcoder")
tokenizer = AutoTokenizer.from_pretrained("bigcode/starcoder")

# EOSトークンをパディングトークンとして設定
tokenizer.pad_token = tokenizer.eos_token

# トークン化関数
def tokenize_function(examples):
    inputs = tokenizer(examples['input'], padding="max_length", truncation=True, max_length=512)
    outputs = tokenizer(examples['output'], padding="max_length", truncation=True, max_length=512)
    inputs['labels'] = outputs['input_ids']
    return inputs

tokenized_datasets = full_dataset.map(tokenize_function, batched=True, remove_columns=['id'])

# データセットの分割
train_size = int(0.8 * len(full_dataset))
train_dataset = full_dataset.select([i for i in range(train_size)])
val_dataset = full_dataset.select([i for i in range(train_size, len(full_dataset))])

# シャッフル
train_dataset = train_dataset.shuffle(seed=42)

# トレーニング設定
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    gradient_accumulation_steps=4,
    save_steps=5_000,
    save_total_limit=2,
    learning_rate=5e-5,
    eval_strategy="steps",
    eval_steps=500,
    load_best_model_at_end=True,
    logging_dir='./logs',
    weight_decay=0.01,  # 正則化
    logging_steps=100,  # ロギングの頻度
    remove_unused_columns=False,  # 不要なカラムを削除しない
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

trainer.train()

# モデルとトークナイザーの保存
trainer.save_model("./saved_model")
tokenizer.save_pretrained("./saved_model")