import eel
import requests

# Eelの初期化
eel.init("web")

@eel.expose
def get_generated_code(input_text):
    # Flask APIにPOSTリクエストを送信
    response = requests.post("http://localhost:5000/process_input", json={"input_text": input_text})

    print("Response Text:", response.text)  # レスポンスの内容を確認
    return response.json().get("generated_code", "Error")

if __name__ == "__main__":
    eel.start("AI.html", mode="default")  # フロントエンドUIの起動