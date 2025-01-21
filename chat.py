import eel
from openai import OpenAI
import re
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
        return {"success": True, "message": "Chat history saved successfully"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        cursor_id.close()
        conn.close()

# 条件が揃ったらchat_numberを1増やす
@eel.expose
def increase_chat_number():
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
            return {"success": True, "message": max_chat_number}

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

        # データがない場合の処理
        if not rows:
            return {"success": True, "data": None}

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

        # chat_numberテーブルにその値が既に存在するか確認
        cursor.execute("SELECT COUNT(*) FROM chat_number WHERE user_id = %s AND chat_number = %s", (user_id, max_chat_history_number + 1))
        exists = cursor.fetchone()[0]

        if exists == 0:
            cursor.execute("INSERT INTO chat_number (user_id, chat_number) VALUES (%s, %s)", (user_id, max_chat_history_number + 1))
            conn.commit()
            return {"success": True, "message": max_chat_history_number + 1}
        else:
            return {"success": True, "message": max_chat_history_number + 1}

    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        cursor.close()
        conn.close()

@eel.expose
def count_code_blocks():
    try:
        # データベース接続
        conn = userManagemrnt.connect_db()
        cursor = conn.cursor()

        # 現在のユーザー情報を取得
        user_info = userManagemrnt.get_user_info()
        user_id = user_info["user_id"]

        # チャット履歴を取得
        cursor.execute(
            "SELECT response_message FROM Chat_History WHERE user_id = %s",
            (user_id,)
        )
        rows = cursor.fetchall()
        
        # データがない場合の処理
        if not rows:
            return {"success": True, "total_code_blocks": 0}

        # 対象の言語クラスを持つ <code> タグの数をカウント
        code_class_pattern = r'<code class="(c|cpp|csharp|ruby|php|javascript|java|bash|sh|python|html|css)">'
        total_code_blocks = 0

        for row in rows:
            response_message = row[0]  # 取得したメッセージ
            matches = re.findall(code_class_pattern, response_message)
            total_code_blocks += len(matches)

        return {"success": True, "total_code_blocks": total_code_blocks}

    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

    finally:
        cursor.close()
        conn.close()