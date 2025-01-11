document.getElementById("signin-form").onsubmit = async function(event) {
    event.preventDefault();
    
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;
    console.log(username, password);

    const result = await eel.signin(username, password)();
    if (result.success) {
        window.location.href = "AI.html"; // ログイン成功後のリダイレクト
    } else {
        alert(result.message); // エラーメッセージの表示
    }
};

document.getElementById("signup-form").onsubmit = async function(event) {
    event.preventDefault();
    
    const username = document.getElementById("signup-username").value;
    const email = document.getElementById("signup-email").value;
    const password = document.getElementById("signup-password").value;
    const passwordConfirm = document.getElementById("signup-password-confirm").value;
    const secretWord = document.getElementById("signup-secretWord").value;

    const result = await eel.signup(username, email, password, passwordConfirm, secretWord)();
    if (result.success) {
        alert("Sign up successful.");
        // 現在アクティブなフォームを探して非アクティブにする
        document.getElementById('signup-form').parentElement.classList.remove('is-active')
        
        // サインインフォームをアクティブにする
        document.getElementById('signin-form').parentElement.classList.add('is-active')
        
        // フォーム内容をリセット
        resetFormFields('signup-form');
        resetFormFields('signin-form');
    } else {
        alert(result.message); // エラーメッセージの表示
    }
};


// Switcher ボタンを取得
const switchers = [...document.querySelectorAll('.switcher')];

// 各スイッチャーにクリックイベントを設定
switchers.forEach(item => {
    item.addEventListener('click', function () {
        // 他のフォームを非アクティブに
        switchers.forEach(switcher => switcher.parentElement.classList.remove('is-active'));

        // 現在のフォームをアクティブに
        this.parentElement.classList.add('is-active');

        // フォームの入力内容をリセット
        resetFormFields('signup-form');
        resetFormFields('signin-form');
    });
});

// フォームの入力内容をリセットする関数
function resetFormFields(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset(); // フォームの内容をリセット
    }
}

/* パスワードリセットのポップアップ */
// ポップアップを表示する関数
document.getElementById("forgot-password-link").addEventListener("click", function() {
    document.getElementById("forgot-password-popup").style.display = "block"; // ポップアップを表示
});

// ポップアップを閉じる
document.getElementById("close-popup").addEventListener("click", function() {
    document.getElementById("forgot-password-popup").style.display = "none"; // ポップアップを非表示
    resetFormFields('forgot-password-form'); // フォームの入力内容をリセット
});
document.getElementById("close-popup-change-password").addEventListener("click", function() {
    document.getElementById("change-password-popup").style.display = "none"; // ポップアップを非表示
    resetFormFields('change-password-form'); // フォームの入力内容をリセット
});

// パスワードリセットフォームの送信
document.getElementById("forgot-password-form").onsubmit = async function(event) {
    event.preventDefault();

    const username = document.getElementById("forgot-username").value;
    const secretWord = document.getElementById("forgot-secretWord").value;

    const result = await eel.verify_secret_word(username, secretWord)(); // サーバーサイドで確認

    if (result.success) {
        resetFormFields('forgot-password-form');
        alert("Secret Word validated. You can now reset your password.");
        document.getElementById("forgot-password-popup").style.display = "none";
        document.getElementById("change-password-popup").style.display = "block";
        document.getElementById("change-password-form").onsubmit = async function(event) {
            event.preventDefault();
            const newPassword = document.getElementById("newpassword").value;
            const newPasswordConfirm = document.getElementById("newpassword_confirm").value;
            const result = await eel.change_password(newPassword, newPasswordConfirm, username)();
            if (result.success) {
                resetFormFields('change-password-form');
                alert("Password changed successfully.");
                document.getElementById("change-password-popup").style.display = "none";
            } else {
                alert(result.message); // エラーメッセージの表示
            }
        }
    } else {
        alert(result.message); // エラーメッセージの表示
    }
};