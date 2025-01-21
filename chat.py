import eel
from openai import OpenAI
import userManagemrnt

# OpenAI APIキーの設定
client = OpenAI(api_key="APIKey")


@eel.expose
def get_generated_code(text):
    response = client.chat.completions.create(model="gpt-4o-mini", # モデルの指定 40-mini or 40
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": text},
    ])
    print(response.choices[0].message.content)
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
        return {"success": True, "message": "Chat history saved successfully"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        cursor_id.close()
        conn.close()

# 条件が揃ったらchat_numberを1増やす
@eel.expose
def increase_chat_number(chat_number_latest):
    try:
        conn = userManagemrnt.connect_db()
        cursor = conn.cursor()

        # ユーザー情報の取得
        user_info = userManagemrnt.get_user_info()
        username = user_info["username"]
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()[0]

        # chat_numberテーブルの最大値を取得
        cursor.execute("SELECT MAX(chat_number) FROM chat_number WHERE user_id = %s", (user_id,))
        result_chat = cursor.fetchone()
        max_chat_number = result_chat[0] if result_chat and result_chat[0] is not None else 0

        # Chat_Historyテーブルの最大値を取得
        cursor.execute("SELECT MAX(chat_number) FROM Chat_History WHERE user_id = %s", (user_id,))
        result_history = cursor.fetchone()
        max_chat_history_number = result_history[0] if result_history and result_history[0] is not None else 0

        # Chat_Historyの最大chat_numberまでしか増加させない
        if max_chat_number <= max_chat_history_number:
            new_chat_number = max_chat_number + 1
            cursor.execute("INSERT INTO chat_number (user_id, chat_number) VALUES (%s, %s)", (user_id, new_chat_number))
            conn.commit()
            return {"success": True, "message": new_chat_number}
        else:
            return {"success": False, "message": "Chat number cannot exceed Chat_History max value."}

    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        cursor.close()
        conn.close()

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
        cursor.close()
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
    finally:
        cursor.close()
        conn.close()

@eel.expose
def insert_chat_number_on_reload():
    try:
        conn = userManagemrnt.connect_db()
        cursor = conn.cursor()

        # ユーザー情報の取得
        user_info = userManagemrnt.get_user_info()
        username = user_info["username"]
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()[0]

        # Chat_Historyテーブルの最大値を取得
        cursor.execute("SELECT MAX(chat_number) FROM Chat_History WHERE user_id = %s", (user_id,))
        result_history = cursor.fetchone()
        max_chat_history_number = result_history[0] if result_history and result_history[0] is not None else 0
        print("max_chat_history_number"+str(max_chat_history_number))

        # chat_numberテーブルにその値が既に存在するか確認
        cursor.execute("SELECT COUNT(*) FROM chat_number WHERE user_id = %s AND chat_number = %s", (user_id, max_chat_history_number + 1))
        exists = cursor.fetchone()[0]

        if exists == 0:
            cursor.execute("INSERT INTO chat_number (user_id, chat_number) VALUES (%s, %s)", (user_id, max_chat_history_number + 1))
            conn.commit()
            print("chat_number inserted"+str(max_chat_history_number + 1))
            return {"success": True, "message": max_chat_history_number + 1}
        else:
            print("chat_number already exists"+str(max_chat_history_number + 1))
            return {"success": True, "message": max_chat_history_number + 1}

    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        cursor.close()
        conn.close()