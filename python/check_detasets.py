import json
import os

# local_datasetsディレクトリ内の全てのjsonファイルを対象にする
dataset_directory = 'local_datasets'

# idでデータを検索する関数
def get_data_by_id(id):
    try:
        # ディレクトリ内の全てのファイルを読み込む
        for file_name in os.listdir(dataset_directory):
            if file_name.endswith('.json'):
                file_path = os.path.join(dataset_directory, file_name)
                # jsonファイルを開く
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # idで指定されたデータを検索
                for item in data:
                    if item.get('id') == id:
                        return item
        
        # 指定されたidが見つからなかった場合
        print(f"ID {id}のデータは見つかりませんでした。")
        return None
    
    except FileNotFoundError:
        print(f"ファイル {file_path} が見つかりません。")
        return None
    except json.JSONDecodeError:
        print(f"JSONファイルの読み込みに失敗しました。")
        return None

# 使用例: idが1のデータを表示
id_to_search = int(input("idを指定してください: "))
data = get_data_by_id(id_to_search)

if data:
    print("指定されたIDのデータ:")
    print(f"ID: {data['id']}")
    print(f"Input: {data['input']}")
    print(f"Output: {data['output']}")