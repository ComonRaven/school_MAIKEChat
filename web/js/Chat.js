document.addEventListener('DOMContentLoaded', function() {
  let sendButton = document.getElementById('send-btn');
  sendButton.addEventListener('click', function() {
      let text = document.getElementById('into-text');
      let question = document.getElementById('question');
      question.value = text.value;

      // eelでPythonの関数を呼び出す
      eel.get_generated_code(text.value)(function(output) {
          let outputArea = document.getElementById('output');
          outputArea.value = output;
      });
  });
});

function showChat() {
  document.getElementById('chatScreen').style.display = 'block';
  document.getElementById('executeScreen').style.display = 'none';
}

function showExecute() {
  document.getElementById('chatScreen').style.display = 'none';
  document.getElementById('executeScreen').style.display = 'block';
}