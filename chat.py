import eel
from openai import OpenAI
import userManagemrnt

# OpenAI APIキーの設定
client = OpenAI(api_key="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")


@eel.expose
def get_generated_code(text):
    response = client.chat.completions.create(model="gpt-4o-mini", # モデルの指定 40-mini or 40
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": text},
    ])
    return response.choices[0].message.content

# チャット履歴をDBに保存
@eel.expose
def chat_to_database(username,chat_number,input, output):
    try:
        conn = userManagemrnt.connect_db()
        cursor_id = conn.cursor()
        cursor_id.execute(
            "SELECT id FROM users WHERE username = %s",
            (username,)
        )
        user_id = cursor_id.fetchone()[0]
        cursor_insert = conn.cursor()
        cursor_insert.execute(
            "INSERT INTO Chat_History (user_id, chat_number ,send_message, response_message) VALUES (%s, %s, %s, %s)", 
            (user_id, chat_number, input, output)
        )
        conn.commit()
        #increase_chat_number(chat_number)
        return {"success": True, "message": "Chat history saved successfully"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

# chat_numberの最大値を返す
@eel.expose
def chat_number():
    try:
        conn = userManagemrnt.connect_db()
        userinfo = userManagemrnt.get_user_info()
        username = userinfo["username"]
        cursor = conn.cursor()
        
        # ユーザーIDを取得
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()[0]
        
        # 最大の chat_number を取得
        cursor.execute("SELECT MAX(chat_number) FROM chat_number WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        
        if result and result[0] is not None:
            chat_number = result[0]  # 最大値を取得
            return {"success": True, "message": chat_number}
        else:
            return {"success": False, "message": "Chat number not found"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

# 条件が揃ったらchat_numberを1増やす
@eel.expose
def increase_chat_number(chat_number):
    try:
        conn = userManagemrnt.connect_db()
        cursor = conn.cursor()
        
        # 新しい chat_number を挿入
        user_info = userManagemrnt.get_user_info()
        username = user_info["username"]
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()[0]
        
        # 最大のchat_numberを取得
        cursor.execute("SELECT MAX(chat_number) FROM chat_number WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()

        if result and result[0] is not None:
            max_chat_number = result[0]
        else:
            max_chat_number = 0  # chat_number テーブルが空の場合の初期値

        print("max_chat_number:", max_chat_number)
        print("chat_number:", chat_number)

        if max_chat_number - chat_number == 0:
            cursor.execute("INSERT INTO chat_number (user_id, chat_number) VALUES (%s, %s)", (user_id, max_chat_number+1))
            conn.commit()
            return {"success": True, "message": chat_number}
        elif max_chat_number > chat_number:
            cursor.execute("SELECT MAX(chat_number) FROM Chat_History WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            if result and result[0] is not None:
                if max_chat_number == result[0]:
                    cursor.execute("INSERT INTO chat_number (user_id, chat_number) VALUES (%s, %s)", (user_id, max_chat_number+1))
                    conn.commit()
                    return {"success": True, "message": max_chat_number}
        else:
            return {"success": False, "message": "Chat number is not greater than the current max."}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

@eel.expose
def get_history():
    try:
        # データベース接続
        conn = userManagemrnt.connect_db()
        cursor = conn.cursor()
        
        # 現在のユーザー情報を取得
        user_info = userManagemrnt.get_user_info()
        user_id = user_info["user_id"]

        # Chat_Historyテーブルから指定ユーザーのデータを取得
        cursor.execute(
            "SELECT chat_number, send_message, response_message FROM Chat_History WHERE user_id = %s ORDER BY chat_number ASC",
            (user_id,)
        )
        rows = cursor.fetchall()

        # chat_numberごとにデータを整理
        history_data = {}
        for chat_number, send_message, response_message in rows:
            if chat_number not in history_data:
                history_data[chat_number] = []  # 新しいチャット番号のリストを作成
            
            # メッセージを辞書形式で格納
            history_data[chat_number].append({
                "send_message": send_message,
                "response_message": response_message
            })

        return {"success": True, "data": history_data}

    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

    finally:
        # データベース接続をクローズ
        if conn:
            conn.close()

@eel.expose
def get_latestChatnumber():
    try:
        conn = userManagemrnt.connect_db()
        cursor = conn.cursor()
        userinfo = userManagemrnt.get_user_info()
        user_id = userinfo['user_id']
        cursor.execute("SELECT MAX(chat_number) FROM chat_number WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        if result and result[0] is not None:
            max_chat_number = result[0]
        else:
            max_chat_number = 0
        return {"success": True, "message": max_chat_number}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}