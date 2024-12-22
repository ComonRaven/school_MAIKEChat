document.addEventListener('DOMContentLoaded', function() {
  let sendButton = document.getElementById('send-btn');
  sendButton.addEventListener('click', function() {
      let text = document.getElementById('into-text');
      let question = document.getElementById('question');
      question.value = text.value;

      // PythonのFlask APIを呼び出してコードを生成
      eel.get_generated_code(text.value)(function(output) {
          let outputArea = document.getElementById('output');
          outputArea.value = output;
      });
  });
});