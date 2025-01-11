document.getElementById("signin-form").onsubmit = async function(event) {
    event.preventDefault();
    
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

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
    const password = document.getElementById("signup-password").value;
    const passwordConfirm = document.getElementById("signup-password-confirm").value;

    const result = await eel.signup(username, password, passwordConfirm)();
    if (result.success) {
        alert("Sign up successful.");
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
    });
});

function move() {
    window.location.href = "./AI.html";
}