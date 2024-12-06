import json
import os
import subprocess
import tempfile

# load_dataset関数の定義
def load_dataset(json_file):
    """
    指定されたJSONファイルを読み込む関数
    """
    try:
        # ファイルパスの取得
        dataset_path = os.path.join("local_datasets", json_file)
        
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

def compile_and_run_c_code(c_code):
    """
    Cコードをコンパイルして実行結果を返す関数
    """
    try:
        # 一時ファイルを作成して C コードを書き込む
        with tempfile.NamedTemporaryFile(suffix=".c", delete=False) as temp_c_file:
            temp_c_file.write(c_code.encode('utf-8'))
            temp_c_filename = temp_c_file.name

        # コンパイル用の一時ファイルを作成
        temp_executable = temp_c_filename.replace(".c", "")
        
        # gcc でコンパイル
        compile_result = subprocess.run(
            ["gcc", temp_c_filename, "-o", temp_executable],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if compile_result.returncode != 0:
            # コンパイルエラーの場合
            return f"Compilation Error:\n{compile_result.stderr}"

        # 実行結果を取得
        run_result = subprocess.run(
            [temp_executable],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if run_result.returncode != 0:
            # 実行時エラーの場合
            return f"Runtime Error:\n{run_result.stderr}"
        
        # 正常に実行できた場合の出力
        return f"Execution Output:\n{run_result.stdout}"

    finally:
        # 一時ファイルを削除
        if os.path.exists(temp_c_filename):
            os.remove(temp_c_filename)
        if os.path.exists(temp_executable):
            os.remove(temp_executable)


def update_dataset_with_compilation(dataset):
    """
    データセット内の C コードをコンパイルして結果を description に追加する
    """
    if not dataset:
        print("データセットが空です。")
        return None

    for entry in dataset:
        c_code = entry.get("output", "")
        if c_code:
            print(f"Compiling ID {entry['id']}...")
            compilation_result = compile_and_run_c_code(c_code)
            entry["description"] += f"\n\n[Compilation Result]\n{compilation_result}"
    return dataset


# local_datasetsディレクトリ内の全てのjsonファイルを処理
dataset_directory = 'local_datasets'

for file_name in os.listdir(dataset_directory):
    if file_name.endswith('.json'):
        print(f"Processing file: {file_name}")
        # JSON データセットの読み込み
        dataset = load_dataset(file_name)

        if dataset:
            # データセットを更新
            updated_dataset = update_dataset_with_compilation(dataset)

            # 更新されたデータセットを新しいファイルに保存
            output_file = os.path.join("datasets", f"updated_{file_name}")
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(updated_dataset, f, ensure_ascii=False, indent=4)

            print(f"更新されたデータセットを {output_file} に保存しました。")