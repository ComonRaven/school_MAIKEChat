[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Fw6BNX-f)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=17388676)

# 概要
C言語のソースコードを生成するチャットボットを作成する。 <br>
既存のモデルと独自のデータとモデルを組み合わせてAIを作成し、チャットボットに搭載する。 <br>

# 役割分担
UI...山本瑞貴 <br>
処理...佐藤佑作 <br>
データ集め...山本瑞貴,佐藤佑作 <br>

# 直近のタスク
・UI作成 <br>
・データセットを大量に作成

# AIに何をさせたいか？（メモ用：随時更新）
・コード補完 <br>
・コードエラーチェック <br>
・最適化 <br>

# memo
主に使用するライブラリ <br>
・Hugging Face Transformers // 事前学習モデルを使用 <br>
・PyTorch or TensorFlow // モデルの微調整に使用 <br>
・Scikit-learn // データの前処理や評価に活用 <br>
・Detasets(Hugging Face) // データセットの管理 <br>
<br>
使用検討中モデル <br>
・gpt2-small // コード生成に特化したLLM <br>
学習済みモデルの準備 <br>
Hugging Face Transformersを使用してモデルを読み込む <br>