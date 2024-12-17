import csv
import matplotlib
matplotlib.use('Agg')  # GUIではなく画像ファイルとして保存するためのバックエンド
import matplotlib.pyplot as plt
import numpy as np

# CSVファイルからデータを読み込む
def load_csv_data(csv_file='model_metrics.csv'):
    steps = []
    train_loss = []
    eval_loss = []
    
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダーをスキップ
        for row in reader:
            steps.append(float(row[0]))  # Stepは数値として追加
            # train_lossとeval_lossを確認し、'N/A'の場合はNaNに変換
            train_loss_value = row[2] if row[2] != 'N/A' else 'NaN'
            eval_loss_value = row[3] if row[3] != 'N/A' else 'NaN'
            
            train_loss.append(float(train_loss_value) if train_loss_value != 'NaN' else np.nan)
            eval_loss.append(float(eval_loss_value) if eval_loss_value != 'NaN' else np.nan)
    
    return steps, train_loss, eval_loss

# データを読み込む
steps, train_loss, eval_loss = load_csv_data('model_metrics.csv')

# 成長曲線のプロット
plt.figure(figsize=(10, 5))
plt.plot(steps, train_loss, label='Train Loss', color='blue')
plt.plot(steps, eval_loss, label='Eval Loss', color='red')
plt.xlabel('Steps')
plt.ylabel('Loss')
plt.title('Training Progress')
plt.legend()
plt.grid(True)
# 画像として保存
plt.savefig('growth_curve/training_progress.png')