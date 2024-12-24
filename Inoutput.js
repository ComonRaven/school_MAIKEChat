/*document.getElementById("input").onsubmit
await function Conversion() {
    let inform = document.getElementById("input").content.value;
    }*/
document.addEventListener('DOMContentLoaded', function() {
    let sendButton = document.getElementById('send-btn'); // 送信ボタン
    sendButton.addEventListener('click', function() {
        let text = document.getElementById('into-text');  // 入力エリア
        let question = document.getElementById('question');  // 表示するテキスト
        // 'question'のvalueに入力
        question.value = text.value;
    });
});