# <img src="web/image/readme/logo.png" alt="ロゴ" width="60px">MAIKE Chat

<img src="https://img.shields.io/badge/-Html5-black.svg?logo=html5&style=flat-square" height="30px"> <img src="https://img.shields.io/badge/-Css3-black.svg?logo=css3&style=flat-square" height="30px"> <img src="https://img.shields.io/badge/-Javascript-black.svg?logo=javascript&style=flat-square" height="30px"> <img src="https://img.shields.io/badge/-Python-black.svg?logo=python&style=flat-square" height="30px"> <img src="https://img.shields.io/badge/-Mysql-black.svg?logo=mysql&style=flat-square" height="30px"> <img src="https://img.shields.io/badge/-Redis-black.svg?logo=redis&style=flat-square" height="30px">

<br />

![Sample](web/image/readme/Sample.gif)

`OpenAI API`を用いたチャットアプリです

## 目次
- [主な機能](#主な機能)
    - [サインアップ・ログイン機能](#サインアップ・ログイン機能)
    - [チャット機能](#チャット機能)
    - [コード実行機能](#コード実行機能)
    - [チャット履歴機能](#チャット履歴機能)
- [使い方](#使い方)
    - [1. リポジトリをクローン](#1-リポジトリをクローン)
    - [2. aptパッケージをインストール](#2-aptパッケージをインストール)
    - [3. python3の設定](#3-python3の設定)
    - [4. 環境変数の設定](#4-環境変数の設定)
    - [5. データベースの設定](#5-データベースの設定)
    - [6. アプリの起動](#6-アプリの起動)
- [環境](#環境)
    - [開発環境](#開発環境)
    - [動作確認済みのpythonモジュールバージョン](#動作確認済みのpythonモジュールバージョン)
- [ライセンス](#ライセンス)

# 主な機能
- ### サインアップ・ログイン機能    
  ユーザー登録画面で任意のユーザーを登録可能。    
  パスワードを忘れた場合でも、`SecretWord`を入力することによりパスワード変更を可能にした。 
- ### チャット機能    
  [OpenAI API](https://openai.com/index/openai-api/)を用いて`gpt-4o-mini`にテキストを送信し、その返答を[botUI](https://botui.org/)でチャットとして表示。    
  [Web Speech API](https://dvcs.w3.org/hg/speech-api/raw-file/tip/webspeechapi)を用いて音声入力も可能にした。    
  C言語のコード限定で色付けをした。

- ### コード実行機能    
  [paiza.io](https://paiza.io/ja)を使用して以下の言語に対応させた。    
  - 🟦 C言語  
  - 🟧 C#  
  - 🟨 C++  
  - 🐍 Python3 / Python2  
  - 🌐 生JavaScript  
  - ☕ Java  
  - 💎 Ruby  
  - 🐘 PHP
- ### チャット履歴機能    
    `Chat Historyボタン`を押すことによりチャット履歴を確認及び、選択可能。

<br>

# 使い方   
### 1. リポジトリをクローン    
- httpsでクローン    
    ```bash
    git clone https://github.com/IS2ProjectPractice1/lesson-5-team-development-mike-1.git
    cd lesson-5-team-development-mike-1
    ```
- sshでクローン    
    ```bash
    git clone git@github.com:IS2ProjectPractice1/lesson-5-team-development-mike-1.git
    cd lesson-5-team-development-mike-1
    ```
### 2. aptパッケージをインストール
```bash
sudo apt update
sudo apt install mysql-server redis build-essential libmysqlclient-dev python3.x-dev # pythonのバージョンに応じて変更してください 
sudo mysql_secure_installation
```

### 3. python3の設定    
- 仮想環境を作成(`hoge` は仮想環境名です)  
    ```bash
    sudo apt install python3-venv
    python3 -m venv ~/hoge # "hoge" の部分を好きな名前に変更できます
    ```
- 仮想環境を作動
    ```bash
    source ~/hoge/bin/activate
    ```
- 仮想環境を停止
    ```bash
    deactivate
    ```
- パッケージをインストール    
    ```bash
    source ~/hoge/bin/activate
    pip install eel openai mysql-connector-python bcrypt redis python-dotenv
    ```
### 4. 環境変数の設定
1. [`.env.sample`](./.env.sample)をコピーして`.env`ファイルを作成
    ```bash
    cp .env.sample .env
    ```
2. `.env`ファイルを編集    
    `.env`ファイルに以下のように自分のAPIキーやデータベース設定を入力
    ```bash
    # .env

    # OpenAI APIキー
    MAIKE_OPENAI_API_KEY=your-api-key-here

    # MySQLの設定
    MAIKE_DB_HOST=localhost
    MAIKE_DB_USER=your-database-user
    MAIKE_DB_PASSWORD=your-database-password
    MAIKE_DB_NAME=your-database-name

    # MySQLパスワード要件（MEDIUMポリシー）
    # 1. 長さ: 8文字以上
    # 2. 英大文字: 1文字以上（A-Z）
    # 3. 英小文字: 1文字以上（a-z）
    # 4. 数字: 1桁以上（0-9）
    # 5. 特殊文字: 1文字以上（例: @, #, $, %）

    # Redisの設定
    MAIKE_REDIS_HOST=localhost
    MAIKE_REDIS_PORT=6379
    MAIKE_REDIS_DB=0
    ```
3. `.env`ファイルを適応
    ```bash
    source .env
    ```
### 5. データベースの設定
[db_setup.sh](./db_setup.sh)を実行
```bash
chmod +x ./db_setup.sh
./db_setup.sh
```
### 6. アプリの起動
```bash
python3 main.py
```

# 環境
### 開発環境
- Python 3.11.11
- WSL2
- Raspberry Pi 400
### 動作確認済みのpythonモジュールバージョン
- [Eel 0.18.1](https://github.com/python-eel/Eel)
- [openai 1.58.1](https://platform.openai.com/docs/overview)
- [mysql-connector-python 9.1.0](https://github.com/mysql/mysql-connector-python)
- [bcrypt 4.2.1](https://github.com/pyca/bcrypt)
- [redis 5.2.1](https://github.com/redis/redis)
- [python-dotenv 1.0.1](https://github.com/theskumar/python-dotenv)

# ライセンス
このプロジェクトは [MIT License](LICENSE) のもとで公開されています。
