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