let chat_number = 1;
let chat_number_source;
let chat_number_latest;
let botui;

document.addEventListener('DOMContentLoaded', async function() {
    let sendButton = document.getElementById('send-btn');
    let inputText = document.getElementById('into-text');
    let historyPanel = document.querySelector(".history-panel");
    let historyContent = document.getElementById("history-content");

    chat_number_source = await eel.get_latestChatnumber()();
    chat_number = chat_number_source.message; // ここは処理的に変えちゃいけない

    // クラスの変更を監視する
    const observer = new MutationObserver((mutationsList) => {
        for (let mutation of mutationsList) {
            if (mutation.attributeName === "class") {
                if (historyPanel.classList.contains("active")) {
                    // Pythonから履歴を取得
                    eel.get_history()().then((result) => {
                        if (result.success) {
                            const historyData = result.data;

                            // historyContent をクリア
                            historyContent.innerHTML = "";

                            // chat_number ごとにボタンを作成
                            for (let chatNumber in historyData) {
                                let button = document.createElement("button");

                                let firstSendMessage = historyData[chatNumber][0]?.send_message?.slice(0,12) || "No Messages";
                                let firstResponseMessage = historyData[chatNumber][0]?.response_message?.slice(0, 10) || "No Message";
                                
                                // send_messageとresponse_messageをラップするdivを作成
                                let sendMessageDiv = document.createElement("div");
                                sendMessageDiv.classList.add("send-message");
                                sendMessageDiv.innerText = firstSendMessage;

                                let responseMessageDiv = document.createElement("div");
                                responseMessageDiv.classList.add("response-message");
                                responseMessageDiv.innerText = firstResponseMessage;

                                // ボタンにdivを追加
                                button.appendChild(sendMessageDiv);
                                button.appendChild(responseMessageDiv);
                                button.classList.add("history-button");

                                // ボタンにクリックイベントを追加
                                button.addEventListener("click", () => {
                                    displayChatHistory(historyData[chatNumber], chatNumber);
                                });

                                // ボタンを historyContent に追加
                                historyContent.appendChild(button);
                            }
                        } else {
                            console.error("履歴の取得に失敗しました:", result.message);
                            alert("履歴を取得できませんでした。");
                        }
                    });
                }
            }
        }
    });

    // 監視を開始
    observer.observe(historyPanel, { attributes: true });

    // チャット履歴を表示する関数
    async  function displayChatHistory(messages, chatNumber) {
        closeHistoryPanel();

        document.getElementById('chatScreen').style.display = 'block';
        document.getElementById('executeScreen').style.display = 'none';

        // botUIの内容をクリア
        await botui.message.removeAll();
        chat_number = parseInt(chatNumber);

        // メッセージの内容を順番に表示
        messages.forEach((messagePair) => {
            let messageContainer = document.createElement("div");
            messageContainer.classList.add("message-pair");

            // 質問内容を表示
            botui.message.add({
                content: `質問: ${messagePair.send_message}`
            });
            // 出力をHTMLとして挿入
            botui.message.add({
                type: 'html',
                content: `
                    <div>${messagePair.response_message}</div>
                `
            });
        });
    // 履歴表示領域をクリア
    historyContent.innerHTML = "";
    }


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
        // ボタンを無効化
        sendButton.disabled = true; // ボタンを無効化
        sendButton.src = 'image/send_icon_disable.png'; // 無効時の画像
        sendButton.style.pointerEvents = 'none'; // クリックを無効化

        // 画面更新を保証
        await new Promise(resolve => requestAnimationFrame(resolve));


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

        // ボタンを無効化
        sendButton.disabled = true; // ボタンを無効化
        sendButton.src = 'image/send_icon_disable.png'; // 無効時の画像
        sendButton.style.pointerEvents = 'none'; // クリックを無効化
    });
});

async function showChat() {
    document.getElementById('chatScreen').style.display = 'block';
    document.getElementById('executeScreen').style.display = 'none';

    // BotUIのメッセージをリセット
    await botui.message.removeAll(); // すべてのメッセージを削除
    
    // chat_numberの値を更新
    result_latest = await eel.get_latestChatnumber()();
    if (result_latest.success) {
        chat_number_latest = parseInt(result_latest.message);
    } else {
        console.error("Error getting latest chat number:", result_latest.message);
    }
    let result = await eel.increase_chat_number(chat_number)(); // awaitを使って非同期処理の結果を待機
    
    if(result.success) {
        chat_number = result.message + 1;  // 成功した場合は新しいchat_numberを増加させる
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