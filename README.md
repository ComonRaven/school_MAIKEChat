[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Fw6BNX-f)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=17388676)

# <img src="web/image/readme/logo.png" alt="ロゴ" width="60px" style="vertical-align: middle;">MAIKE Chat

![Logo](web/image/readme/sample.png)

OpenAI APIを用いたチャットアプリです

### 主な機能：
- サインアップ・ログイン機能    
  ユーザー登録画面で任意のユーザーを登録可能。    
  パスワードを忘れた場合でも、`SecretWord`を入力することによりパスワード変更を可能にした
- チャット機能    
  [OpenAI API](https://openai.com/index/openai-api/)を用いて`gpt-4o-mini`にテキストを送信し、その返答を[botUI](https://botui.org/)でチャットとして表示
- コード実行機能    
  [paiza.io](https://paiza.io/ja)を使用して以下の言語に対応させた    
  C言語・C#・C++・Python3・Python2・生JavaScript・Java・Ruby・PHP
- チャット履歴機能    
    Chat Historyボタンを押すことによりチャット履歴を確認及び、選択可能

### 各機能ごとのプレビュー：
- サインアップ・ログイン機能    
  <img src="web/image/readme/signup.png" alt="サインアップ画面" width="150px">
  <img src="web/image/readme/login.png" alt="ログイン画面" width="153.5px">
- チャット機能    
  <img src="web/image/readme/chat.png" alt="チャット画面">
- コード実行機能
  <img src="web/image/readme/webEditor.png" alt="コード実行画面">
- チャット履歴機能    
  <img src="web/image/readme/chatHistory.png" alt="チャット履歴画面">    

<br>

# インストール方法
pythonの仮想環境を作成(hogeは仮想環境名)
```bash
sudo apt install python3-venv
python3 -m venv ~/hoge
```

仮想環境を作動
```bash
source ~/venv/hoge/bin/activate
```

コマンドプロンプトの先頭に (hoge) が表示されれば成功<br>
<br>
仮想環境を停止させる
```bash
deactivate
```
コマンドプロンプトの先頭の (hoge) が非表示になれば成功<br>
<br>
仮想環境に必要なパッケージをインストール<br>
仮想環境を作動させて、以下のコマンドを実行
```bash
pip install eel openai mysql-connector-python bcrypt redis
```
