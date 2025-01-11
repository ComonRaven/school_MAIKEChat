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

    const result = await eel.signup(username, email, password, passwordConfirm)();
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