import csv
import matplotlib.pyplot as plt

# CSVファイルからデータを読み込む
def load_csv_data(csv_file='training_log.csv'):
    steps = []
    train_loss = []
    eval_loss = []
    
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダーをスキップ
        for row in reader:
            steps.append(int(row[0]))
            train_loss.append(float(row[1]))
            eval_loss.append(float(row[2]))
    
    return steps, train_loss, eval_loss

# データを読み込む
steps, train_loss, eval_loss = load_csv_data('training_log.csv')

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

# 表示
plt.show()