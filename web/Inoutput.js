document.addEventListener('DOMContentLoaded', function() {
    let sendButton = document.getElementById('send-btn'); // 送信ボタン
    sendButton.addEventListener('click', function() {
        let text = document.getElementById('into-text');  // 入力エリア
        let question = document.getElementById('question');  // 表示するテキスト

        // 'question'のvalueに入力
        question.value = text.value;

        // Pythonの関数を呼び出して処理を行う
        eel.process_input(text.value)(function(output) {
            //取得した出力をoutputエリアに表示
            let outputArea = document.getElementById('output');
            outputArea.value = output;
        });
    });
});