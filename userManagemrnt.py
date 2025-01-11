import eel
import mysql.connector
import bcrypt  # passlibからbcryptは不要です

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
            return {"success": True}
        else:
            return {"success": False, "message": "Incorrect username or password"}
    else:
        return {"success": False, "message": "Incorrect username or password"}

# サインアップ
@eel.expose
def signup(username, email, password, password_confirm):
    if password != password_confirm:
        return {"success": False, "message": "Passwords do not match"}

    # パスワードをハッシュ化
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

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
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (username, email, hashed_password),
    )
    conn.commit()

    return {"success": True, "message": "User registered successfully"}