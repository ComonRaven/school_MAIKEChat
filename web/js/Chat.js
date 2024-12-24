document.addEventListener('DOMContentLoaded', function() {
  let sendButton = document.getElementById('send-btn');

  // BotUIの初期化
  const botui = new BotUI('botui-app');

  // 初回メッセージ
  botui.message.add({
    content: 'こんにちは！私はMAIkeChatです。'
  }).then(() => {
    return botui.message.add({
      content: '質問をどうぞ！'
    });
  });

  sendButton.addEventListener('click', function() {
    let text = document.getElementById('into-text');
    let question = text.value;

    // 質問内容を表示
    botui.message.add({
      content: `質問: ${question}`
    });

    // 質問内容をクリア
    text.value = '';

    eel.get_generated_code(question)(function(output) {
      console.log(output);
      
      // 出力を整形
      let formattedOutput = output
      .replace(/#include <(.*?)>/g, '#include <$1>')  // #include の < > のみ元に戻す
      .replace(/\n/g, '<br>')  // 改行を <br> に
      .replace(/    /g, '&nbsp;&nbsp;&nbsp;&nbsp;')  // タブをスペースに
      .replace(/</g, '&lt;')  // 全ての < をエスケープ
      .replace(/>/g, '&gt;')  // 全ての > をエスケープ
      .replaceAll(/&lt;br&gt;/g, '<br>')  // <br> をタグとして戻す
      .replace(/```cpp/g, '<pre><code class="cpp">')  // コードブロック開始
      .replace(/```csharp/g, '<pre><code class="csharp">')
      .replace(/```c/g, '<pre><code class="c">')  // コードブロック開始
      .replace(/```ruby/g, '<pre><code class="ruby">')
      .replace(/```php/g, '<pre><code class="php">')
      .replace(/```javascript/g, '<pre><code class="javascript">')
      .replace(/```java/g, '<pre><code class="java">')
      .replace(/```bash/g, '<pre><code class="bash">')  // コードブロック開始
      .replace(/```sh/g, '<pre><code class="sh">')  // コードブロック開始
      .replace(/```python/g, '<pre><code class="python">')  // コードブロック開始
      .replace(/```html/g, '<pre><code class="html">')  // コードブロック開始
      .replace(/```css/g, '<pre><code class="css">')  // コードブロック開始
      .replace(/```/g, '</code></pre>')  // コードブロック終了
      .replace(/\*\*(.*?)\*\*/g, '<em>$1</em>')  // 斜体
      .replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>')  // インラインコード
      .replaceAll(/### (.*?)(<br>)/g, '<h3>$1</h3>');  // 見出し（###）を <h3> に変換
    
      // 出力をHTMLとして挿入
      botui.message.add({
        type: 'html',
        content: `
          <div>${formattedOutput}</div>
        `
      });
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

document.onload = showChat();