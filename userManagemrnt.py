import eel
import mysql.connector
from passlib.hash import bcrypt

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
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    
    if user and bcrypt.verify(password, user[2]):  # ハッシュ化されたパスワードを検証
        return {"success": True}
    else:
        return {"success": False, "message": "Incorrect username or password"}

# サインアップ
@eel.expose
def signup(username, password, password_confirm):
    if password != password_confirm:
        return {"success": False, "message": "Passwords do not match"}

    # パスワードをハッシュ化
    hashed_password = bcrypt.hash(password)

    # ユーザー名の重複確認
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user:
        return {"success": False, "message": "The username is already in use"}

    # 新規ユーザー登録
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    conn.commit()
    
    return {"success": True}