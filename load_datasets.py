import json
import os

def load_dataset(json_file):
    """
    指定されたJSONファイルを読み込む関数
    """
    try:
        # ファイルパスの取得
        dataset_path = os.path.join("datasets", json_file)
        
        # JSONデータを読み込む
        with open(dataset_path, "r", encoding="utf-8") as f:
            dataset = json.load(f)
        
        return dataset
    except FileNotFoundError:
        print(f"Error: {json_file} が見つかりません。")
        return None
    except json.JSONDecodeError:
        print("Error: JSONのフォーマットが正しくありません。")
        return None


def display_dataset(dataset):
    """
    読み込んだデータセットを表示する関数
    """
    if dataset:
        print("データセットを読み込みました。")
        for entry in dataset:
            print(f"ID: {entry['id']}")
            print(f"Input: {entry['input']}")
            print(f"Output:\n{entry['output']}")
            print(f"Description: {entry['description']}\n")
    else:
        print("データセットが空です。")


# 直接呼び出し
dataset = load_dataset("printf.json")
display_dataset(dataset)

# ここにモデルの学習処理などを追加できます
# 例: train_model(dataset)