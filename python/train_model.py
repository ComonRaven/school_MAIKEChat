import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset, concatenate_datasets
from transformers import Trainer, TrainingArguments, TrainerCallback
from huggingface_hub import login
import csv

# Hugging Face Hubにログイン
login("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")

# データセットをロードして統合
dataset_files = [f'local_datasets/{file}' for file in os.listdir('local_datasets') if file.endswith('.json')]
datasets = []

# 各JSONファイルから 'input' と 'output' カラムのみを抽出
for file in dataset_files:
    dataset = load_dataset('json', data_files=file)['train']
    dataset = dataset.remove_columns([col for col in dataset.column_names if col not in ['input', 'output']])
    datasets.append(dataset)

# 複数のデータセットを統合
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
    inputs['labels'] = outputs['input_ids']  # 'output' を 'labels' に設定
    inputs['attention_mask'] = inputs.get('attention_mask', [1] * len(inputs['input_ids']))  # Ensure attention_mask
    return inputs

# トークン化を実行
tokenized_datasets = full_dataset.map(tokenize_function, batched=True, remove_columns=['input', 'output'])
# 訓練と検証データの分割
train_size = int(0.8 * len(tokenized_datasets))
train_dataset = tokenized_datasets.select([i for i in range(train_size)])
val_dataset = tokenized_datasets.select([i for i in range(train_size, len(tokenized_datasets))])

class CsvLoggerCallback(TrainerCallback):
    def __init__(self, output_file):
        self.output_file = output_file
        # Initialize CSV file with headers if it doesn't exist
        #with open(self.output_file, mode='a', newline='') as file:
            #writer = csv.writer(file)
            #writer.writerow(['epoch', 'step', 'train_loss', 'eval_loss', 'eval_accuracy'])  # Adjust metrics as needed

    def on_log(self, args, state, control, logs=None, **kwargs):
        # Append logs to CSV file
        with open(self.output_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([state.epoch, state.global_step, logs.get('loss', 'N/A'), logs.get('eval_loss', 'N/A'), logs.get('eval_accuracy', 'N/A')])

# Define your output CSV file
csv_logger = CsvLoggerCallback(output_file='./model_metrics.csv')

# トレーニング設定
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=1,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    save_steps=5_000,
    save_total_limit=2,
    learning_rate=5e-5,
    eval_strategy="steps",
    eval_steps=500,
    logging_dir='./logs',  # ログの保存ディレクトリ
    logging_steps=100,  # 100ステップごとにロギング
    remove_unused_columns=False,  # 不要なカラムを削除しない
    use_cpu=True
)

# Trainerインスタンス作成
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    callbacks=[csv_logger],  # Add the callback here
)

# トレーニング開始
trainer.train()

# モデルとトークナイザーを保存
trainer.save_model("./saved_model")
tokenizer.save_pretrained("./saved_model")