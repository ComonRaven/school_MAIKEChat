let chat_number = 1;
let chat_number_source;
let chat_number_latest;
let botui;
let codeBlockCounter = 0;
let inputText = document.getElementById('into-text');
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "ja-JP"; // 日本語対応
recognition.interimResults = false; // 完全な結果のみ取得
let isListening = false; // 音声認識の状態を追跡

document.addEventListener('DOMContentLoaded', async function() {
    let sendButton = document.getElementById('send-btn');
    let historyPanel = document.querySelector(".history-panel");
    let historyContent = document.getElementById("history-content");
    const voiceInput = document.getElementById("voiceInput");

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

                            if (historyData === null) {
                                let message = document.createElement("p");
                                message.innerText = "まだ履歴がありません。";
                                message.style.color = "white";
                                historyContent.appendChild(message);
                                return;
                            }

                            // historyContent をクリア
                            historyContent.innerHTML = "";

                            // chat_numberを降順にソートしてボタンを作成
                            Object.keys(historyData)
                                .sort((a, b) => b - a)  // chat_numberを降順にソート
                                .forEach(chatNumber => {
                                    let button = document.createElement("button");

                                    let firstSendMessage = historyData[chatNumber][0]?.send_message?.slice(0,12) || "No Messages";
                                    let firstResponseMessage = historyData[chatNumber][0]?.response_message?.slice(0, 10) || "No Message";
                                    
                                    // send_messageとresponse_messageをラップするdivを作成
                                    let sendMessageDiv = document.createElement("div");
                                    sendMessageDiv.classList.add("send-message");
                                    sendMessageDiv.innerText = "{" + chatNumber + "} " + firstSendMessage;

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
                                });
                        } else {
                            let message = document.createElement("p");
                            message.innerText = "履歴を取得できませんでした。";
                            historyContent.appendChild(message);
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
                content: `{${chat_number}}質問: ${messagePair.send_message}`
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

    // 音声入力周りの処理
    voiceInput.addEventListener("click", () => {
        if (!isListening) {
            // 音声認識を開始
            recognition.start();
            voiceInput.src = "image/voiceInput_gray.png"; // 画像をgrayに変更
            voiceInput.classList.add("gray"); // クラスを追加
            isListening = true;
        } else {
            // 音声認識を停止
            recognition.stop();
            voiceInput.src = "image/voiceInput_black.png"; // 画像をblackに戻す
            voiceInput.classList.remove("gray"); // クラスを削除
            isListening = false;
        }
    });
    recognition.addEventListener("result", (event) => {
        const text = event.results[0][0].transcript;
        inputText.value += text; // Chat.jsのinputTextを参照して文字を追加
        // inputイベントを手動で発火させる
        const eventInput = new Event('input');
        inputText.dispatchEvent(eventInput);  // これで手動でinputイベントを発火させる
    });
    recognition.addEventListener("end", () => {
        if (isListening) {
            recognition.start(); // 再起動して継続する場合
        }
    });


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
        content: '{' + chat_number + '}こんにちは！私はMAIKE Chatです。'
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

        
         // 「●●●」を順番に点滅させるため、個別に `<span>` を追加
        let waitingMessage = await botui.message.add({
            content: '<span class="blinking-dot">●</span><span class="blinking-dot">●</span><span class="blinking-dot">●</span>'
        });

        eel.get_generated_code(question, chat_number)(function(output) {
            eel.count_code_blocks()().then((result) => {
                if (result.success) {
                    codeBlockCounter = result.total_code_blocks;
                } else {
                    console.error("エラー:", result.message);
                }
            });

            // 出力を整形
            console.log("整形前"+"\n"+output);
            let formattedOutput = output
            .replace(/#include <(.*?)>/g, '#include <$1>')  // #include の < > のみ元に戻す
            .replace(/\n/g, '<br>')  // 改行を <br> に
            .replace(/    /g, '&nbsp;&nbsp;&nbsp;&nbsp;')  // タブをスペースに
            .replace(/</g, '&lt;')  // 全ての < をエスケープ
            .replace(/>/g, '&gt;')  // 全ての > をエスケープ
            .replaceAll(/&lt;br&gt;/g, '<br>')  // <br> をタグとして戻す
            .replace(/```(c|cpp|csharp|ruby|php|javascript|java|bash|sh|python|html|css)/g, (match, lang) => {
                // コードブロック開始時に番号付きのクラスを追加
                codeBlockCounter++;
                return `<code class="${lang}"><div class="copy-div-${lang}"><button type="button" class="copy-button" onclick="copyCodeToClipboard(this)" data-code-block="${codeBlockCounter}">コピー</button></div><pre class="code-block-${codeBlockCounter}">`;
            })
            .replace(/```/g, '</pre></code>')  // コードブロック終了
            .replace(/<pre[^>]*>(.*?)<\/pre>/gs, (match, codeBlock) => {
                // <pre>内のコードブロックを対象にする
                return `<pre>${codeBlock
                    .replace(/#include\s+&lt;([^>]+)&gt;/g, (match, p1) => {
                        return `<span class="include-tag">#include</span> <span class="headerFile">&lt;${p1}&gt;</span>`;  // #include部分だけ囲む
                    })
                    .replace(/\b(int|char|float|double|void|short|long|unsigned|signed|bool|long long)\b/g, (match) => {
                        // 型名部分を<span>で囲んで色を付ける
                        return `<span class="type-name">${match}</span>`;
                    })
                    .replace(/\b(if|else|for|while|do|switch|case|break|continue|return|true|false)\b/g, (match) => {
                        // キーワード部分を<span>で囲んで色を付ける
                        return `<span class="keyword">${match}</span>`;
                    })
                }</pre>`;
            })
            .replace(/\*\*(.*?)\*\*/g, '<em>$1</em>')  // 斜体
            .replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>')  // インラインコード
            .replaceAll(/### (.*?)(<br>)/g, '<h3>$1</h3>');  // 見出し（###）を <h3> に変換

            console.log("整形後"+"\n"+formattedOutput);

            // 点滅を止めて「●●●」を削除
            botui.message.remove(waitingMessage);  // 「●●●」を削除

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
    let result = await eel.increase_chat_number()(); // awaitを使って非同期処理の結果を待機
    
    if(result.success) {
        chat_number = result.message;  // 成功した場合は新しいchat_numberを増加させる
    } else {
        console.error("Error updating chat number:", result.message); // エラーメッセージをログ出力
    }
    
    // 初回メッセージ
    botui.message.add({
        content: '{' + chat_number + '}こんにちは！私はMAIKE Chatです。'
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

//document.onload = showChat;
window.addEventListener('load', async function () {
    try {
        showChat();
        
        let result = await eel.insert_chat_number_on_reload()();
        if (result.success) {
            chat_number = parseInt(result.message);
        } else {
            console.warn("Chat number update failed:", result.message);
        }
    } catch (error) {
        console.error("Error during page load:", error);
    }
});

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

// コピー処理を行う関数
function copyCodeToClipboard(button) {
    // ボタンからデータ属性を取得
    if (!button || !button.getAttribute) {
        console.error("button が正しく渡されていません");
        return;
    }

    const blockNumber = button.getAttribute('data-code-block');
    const codeElement = document.querySelector(`.code-block-${blockNumber}`);

    if (codeElement) {
        // テキストを取得（innerText は改行やインデントを保持）
        const codeText = codeElement.innerText.trim();

        // クリップボードにコピー
        navigator.clipboard.writeText(codeText)
            .then(() => {
                alert(`コードをクリップボードにコピーしました`);
            })
            .catch(err => {
                alert('コピーに失敗しました: ' + err);
            });
    } else {
        alert(`コードブロックが見つかりません: ブロック番号 ${blockNumber}`);
    }
}

// 入力量に応じてチャット画面の高さを変更
function adjustChatScreenHeight() {
    const textArea = document.getElementById('into-text');
    const botUIContainer = document.querySelector('.botUI-container');
    const headerHeight = document.querySelector('.header').offsetHeight;
    const availableHeight = window.innerHeight - headerHeight - 50 - 22;  // 余白分を引く

    // 改行の数をカウント（最初の行はカウントしない）
    const lineBreaks = (textArea.value.match(/\n/g) || []).length;
    const lineHeight = 20;  // 1行あたりの高さ増加分（px）
    const baseHeight = 40;  // 入力エリアの初期高さ（CSSと一致させる）
    const maxHeight = 150;  // 最大の高さ

    // 改行がある場合のみ高さを増やす
    let newHeight = baseHeight + (lineBreaks * lineHeight);
    newHeight = Math.min(newHeight, maxHeight);
    textArea.style.height = `${newHeight}px`;

    // BotUI の高さを自動調整
    const botUIHeight = availableHeight - newHeight;
    botUIContainer.style.height = `${Math.max(botUIHeight, 200)}px`;

    // 入力が空の場合、デフォルトのサイズに戻す
    if (textArea.value.trim() === "") {
        textArea.style.height = `${baseHeight}px`;
        botUIContainer.style.height = `calc(100vh - 70px - 2vh - 100px)`;  // 初期の高さに戻す
    }
}