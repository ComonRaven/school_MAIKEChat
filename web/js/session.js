// セッションチェック関数
async function checkSession() {
    const sessionId = localStorage.getItem("session_id"); // ローカルストレージからセッションIDを取得
    if (!sessionId) {
        redirectToLogin();
        return;
    }

    const response = await eel.check_session(sessionId)(); // Pythonのセッションチェック関数を呼び出し
    if (!response.success) {
        redirectToLogin();
    }
}

// ログイン画面へのリダイレクト関数
function redirectToLogin() {
    alert("Your session has expired. Please log in again.");
    localStorage.removeItem("session_id"); // セッションIDを削除
    window.location.href = "home.html";   // ログイン画面にリダイレクト
}

// 一定間隔でセッションチェックを実行
setInterval(checkSession, 30000); // 30秒ごとにチェック