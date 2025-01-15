import eel
import mysql.connector
import bcrypt
import redis
import uuid
import json

# Redisに接続
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# MySQLデータベース接続
def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='MAIkeUser',
        password='3@WaM2cEZDpu4SR*KUAQt',
        database='MAIke'
    )

# サインイン
@eel.expose
def signin(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    
    # ユーザーを取得
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user:
        # パスワードの検証
        stored_password = user[3]  # データベースに保存されたハッシュ
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):  # パスワード照合
            # セッションIDを生成
            session_id = str(uuid.uuid4())
            # Redisにセッション情報を保存
            redis_client.hset(session_id, mapping={
                "username": user[1],
                "email": user[2],
                "password": password,
            })
            redis_client.expire(session_id, 3600)  # セッション有効期限を1時間に設定

            return {"success": True, "session_id": session_id, "message": "Login successful"}
        else:
            return {"success": False, "message": "Incorrect username or password"}
    else:
        return {"success": False, "message": "Incorrect username or password"}

# サインアップ
@eel.expose
def signup(username, email, password, password_confirm, secretWord):
    if password != password_confirm:
        return {"success": False, "message": "Passwords do not match"}

    # パスワードをハッシュ化
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_secretWord = bcrypt.hashpw(secretWord.encode('utf-8'), bcrypt.gensalt())

    # データベース接続
    conn = connect_db()
    cursor = conn.cursor()

    # ユーザー名の重複確認
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if user:
        return {"success": False, "message": "The username is already in use"}

    # メールアドレスの重複確認
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    email_check = cursor.fetchone()
    if email_check:
        return {"success": False, "message": "The email address is already in use"}

    # 新規ユーザー登録
    cursor.execute(
        "INSERT INTO users (username, email, password, secretWord) VALUES (%s, %s, %s, %s)",
        (username, email, hashed_password, hashed_secretWord),
    )
    conn.commit()
    
    # user_idを取得
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    user_id = user[0]
    
    # chat_numverテーブルにchat_numberを追加
    cursor.execute(
        "INSERT INTO chat_number (user_id,chat_number) VALUES (%s,1)",
        (user_id,)
    )
    conn.commit()

    return {"success": True, "message": "User registered successfully"}

# ユーザー名とsecretWordを確認する関数
@eel.expose
def verify_secret_word(username, secretWord):
    # データベース接続
    conn = connect_db()
    cursor = conn.cursor()

    # ユーザーが存在するか確認
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user:
        return {"success": False, "message": "User not found"}

    # secretWordを比較
    stored_secretWord = user[4]  # secretWordのカラム番号が4と仮定

    if bcrypt.checkpw(secretWord.encode('utf-8'), stored_secretWord.encode('utf-8')):
        return {"success": True, "message": "Secret Word validated"}
    else:
        return {"success": False, "message": "Invalid Secret Word"}

# パスワードを変更する(newPassword, newPasswordConfirmが同じ場合のみ)  
@eel.expose
def change_password(newPassword, newPasswordConfirm, username):
    # パスワードが一致するか確認
    if newPassword != newPasswordConfirm:
        return {"success": False, "message": "Passwords do not match"}

    # パスワードをハッシュ化
    hashed_password = bcrypt.hashpw(newPassword.encode('utf-8'), bcrypt.gensalt())

    # データベース接続
    conn = connect_db()
    cursor = conn.cursor()

    # パスワードを更新するクエリ
    cursor.execute("UPDATE users SET password = %s WHERE username = %s", (hashed_password, username))

    # 更新されたユーザーが存在するか確認
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user:
        return {"success": False, "message": "User not found"}

    # コミットして変更を保存
    conn.commit()

    return {"success": True, "message": "Password changed successfully"}

# セッションチェック関数
@eel.expose
def check_session(session_id):
    if redis_client.exists(session_id):
        return {"success": True}
    else:
        return {"success": False, "message": "Session expired"}

# セッションからユーザー情報を取得する関数
@eel.expose
def get_user_info():
    try:
        # JavaScriptからセッションIDを取得
        session_id = eel.get_session_id()()
        
        # データ型を確認
        data_type = redis_client.type(session_id)
        if data_type != 'hash':
            print(f"Redisエラー: キー {session_id} の型は {data_type} です")
            return {"username": "エラー", "email": "取得失敗"}

        # Redisのハッシュ型データを取得
        user_data = redis_client.hgetall(session_id)

        # データをそのまま辞書に変換（すでに文字列型である場合はdecode()は不要）
        user_info = {k: v for k, v in user_data.items()}
        
        return {
            "username": user_info.get("username", "ゲスト"),
            "email": user_info.get("email", "未登録"),
            "password": user_info.get("password", "未登録")
        }
    
    except redis.exceptions.RedisError as e:
        print(f"Redisエラー: {e}")
        return {"username": "エラー", "email": "取得失敗"}