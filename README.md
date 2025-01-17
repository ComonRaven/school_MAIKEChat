[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Fw6BNX-f)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=17388676)

# 概要
チャットwebアプリ <br>
チャット機能とソースコード実行機能が搭載されている <br>
チャットは履歴管理機能も追加されている <br>

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
