let chat_number = 1;
let botui;

document.addEventListener('DOMContentLoaded', function() {
    let sendButton = document.getElementById('send-btn');
    let inputText = document.getElementById('into-text');

    // 初期状態で無効化
    sendButton.disabled = true;
    sendButton.src = 'image/send_icon_disable.png'; // 無効時の画像
    sendButton.style.pointerEvents = 'none'; // クリックを無効化

    // 入力欄に文字があるかチェックして、ボタンを有効化/無効化する
    inputText.addEventListener('input', () => {
        if (inputText.value.trim() === "") {
            sendButton.disabled = true; // ボタンを無効化
            sendButton.src = 'image/send_icon_disable.png'; // 無効時の画像
            sendButton.style.pointerEvents = 'none'; // クリックを無効化
        } else {
            sendButton.disabled = false; // ボタンを有効化
            sendButton.src = 'image/send_icon.png'; // 有効時の画像
            sendButton.style.pointerEvents = 'auto'; // クリックを有効化
        }
    });

    botui = new BotUI('botui-app');

    // 初回メッセージ
    botui.message.add({
        content: 'こんにちは！私はMAIkeChatです。'
    }).then(() => {
        return botui.message.add({
            content: '質問をどうぞ！'
        }); 
    });

    sendButton.addEventListener('click', async function() {
        let question = inputText.value;

        if (question === '') {
            return;
        }

        // 質問内容を表示
        botui.message.add({
            content: `質問: ${question}`
        });

        // 質問内容をクリア
        inputText.value = '';

        // ボタンを無効化
        sendButton.disabled = true; // ボタンを無効化
        sendButton.src = 'image/send_icon_disable.png'; // 無効時の画像
        sendButton.style.pointerEvents = 'none'; // クリックを無効化

        // 非同期で chat_number を取得
        let response = await eel.chat_number()();
        if (response.success) {
            chat_number = response.message; // 最大値を取得
        } else {
            console.error("Error retrieving chat number:", response.message);
            chat_number = 1; // デフォルト値
        }

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
            // データベースにチャット履歴を保存
            const username = document.getElementById('user-name').textContent;
            eel.chat_to_database(username, chat_number, question, formattedOutput);
        });
    });
});

async function showChat() {
    document.getElementById('chatScreen').style.display = 'block';
    document.getElementById('executeScreen').style.display = 'none';

    // BotUIのメッセージをリセット
    await botui.message.removeAll(); // すべてのメッセージを削除
    
    // chat_numberの値を更新
    let result = await eel.increase_chat_number(chat_number)(); // awaitを使って非同期処理の結果を待機
    
    if(result.success) {
        chat_number = result.message;  // 成功した場合は新しいchat_numberを代入
    } else {
        console.error("Error updating chat number:", result.message); // エラーメッセージをログ出力
    }
    
    // 初回メッセージ
    botui.message.add({
        content: 'こんにちは！私はMAIkeChatです。'
    }).then(() => {
        return botui.message.add({
            content: '質問をどうぞ！'
        }); 
    });
}

function showExecute() {
    document.getElementById('chatScreen').style.display = 'none';
    document.getElementById('executeScreen').style.display = 'block';
}

document.onload = showChat();

function showHistoryPanel() {
    const historyPanel = document.getElementById("historyPanel");
    const overlay = document.getElementById("historyOverlay");
    historyPanel.classList.add("active");
    overlay.classList.add("active"); // オーバーレイを表示
}

function closeHistoryPanel() {
    const historyPanel = document.getElementById("historyPanel");
    const overlay = document.getElementById("historyOverlay");
    historyPanel.classList.remove("active");
    overlay.classList.remove("active"); // オーバーレイを非表示
}