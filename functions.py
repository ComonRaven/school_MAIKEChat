import eel

@eel.expose
def process_input(input_text):
    # 入力を処理して、出力を生成
    # ここでAI処理やその他のロジックを加えることができます
    output_text = f"あなたの入力は: {input_text}"
    return output_text