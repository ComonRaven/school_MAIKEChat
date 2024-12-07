import os
import csv
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset, concatenate_datasets
from transformers import Trainer, TrainingArguments
from huggingface_hub import login
from tensorboard.backend.event_processing import event_accumulator

# Hugging Face Hubにログイン
login("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")

# データセットをロードして統合
dataset_files = [f'local_datasets/{file}' for file in os.listdir('local_datasets') if file.endswith('.json')]
datasets = [load_dataset('json', data_files=file)['train'] for file in dataset_files]
full_dataset = concatenate_datasets(datasets)

# モデルとトークナイザーのロード
modelname = "gpt2"
model = AutoModelForCausalLM.from_pretrained(modelname)
tokenizer = AutoTokenizer.from_pretrained(modelname)

# トークン化
tokenizer.pad_token = tokenizer.eos_token

def tokenize_function(examples):
    inputs = tokenizer(examples['input'], padding="max_length", truncation=True, max_length=512)
    outputs = tokenizer(examples['output'], padding="max_length", truncation=True, max_length=512)
    inputs['labels'] = outputs['input_ids']
    return inputs

tokenized_datasets = full_dataset.map(tokenize_function, batched=True, remove_columns=['id'])

# 訓練と検証データの分割
train_size = int(0.8 * len(full_dataset))
train_dataset = full_dataset.select([i for i in range(train_size)])
val_dataset = full_dataset.select([i for i in range(train_size, len(full_dataset))])

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
    logging_dir='./logs',  # ログの保存ディレクトリ
    logging_steps=100,  # 100ステップごとにロギング
)

# Trainerインスタンス作成
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

# トレーニング開始
trainer.train()

# モデルとトークナイザーを保存
trainer.save_model("./saved_model")
tokenizer.save_pretrained("./saved_model")

# ログファイルから損失を抽出してCSVに保存
def extract_and_save_logs_to_csv(log_dir='./logs', csv_file='training_log.csv'):
    logs = []
    for root, dirs, files in os.walk(log_dir):
        for file in files:
            if 'events.out.tfevents' in file:
                logs.append(os.path.join(root, file))

    event_acc = event_accumulator.EventAccumulator(logs[0])
    event_acc.Reload()

    train_loss = [x.value for x in event_acc.Scalars('train/loss')]
    eval_loss = [x.value for x in event_acc.Scalars('eval/loss')]
    
    # CSVに保存
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Step', 'Train Loss', 'Eval Loss'])
        for i in range(len(train_loss)):
            writer.writerow([i * 100, train_loss[i], eval_loss[i]])

# CSVファイルにログを保存
extract_and_save_logs_to_csv('./logs', 'training_log.csv')