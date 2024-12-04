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
・基本的な処理作成 <br>

# AIに何をさせたいか？（メモ用：随時更新）
・コード補完 <br>
・コードエラーチェック <br>
・最適化 <br>

# 実行環境
python  3.11.0 <br>
Flask   3.1.0 <br>
Eel     0.18.1 <br>
numpy   2.1.3 <br>
pandas  2.2.3 <br>
matplotlib  3.9.3 <br>
scikit-learn  1.5.2 <br>
jupyter 1.1.1 <br>
transformers  4.63.3 <br>
protobuf  5.29.0 <br>
torch 2.5.1<br>
torchvision 0.20.1<br>
torchaudio  2.5.1<br>
tiktoken  0.8.0 <br>

# memo
主に使用するライブラリ <br>
・Hugging Face Transformers // 事前学習モデルを使用 <br>
・PyTorch or TensorFlow // モデルの微調整に使用 <br>
・Scikit-learn // データの前処理や評価に活用 <br>
・Detasets(Hugging Face) // データセットの管理 <br>
<br>
使用検討中モデル <br>
・CodeT5(Salesforce) // コード生成に特化したモデル <br>
<br>
データセット <br>
json形式でデータセットを作成 <br>
id,input,output,descriptionで設定する <br>
<br>
学習済みモデルの準備 <br>
Hugging Face Transformersを使用してモデルを読み込む <br>
<br>
データセットの前処理 <br>
<br>
モデルの微調整 <br>
Trainerを使用 <br>
<br>
モデルの推論 <br>
<br>
フロンんととの接続 <br>
Eelを使って接続