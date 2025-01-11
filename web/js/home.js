document.getElementById("signin-form").onsubmit = async function(event) {
    event.preventDefault();
    
    const username = document.getElementById("signin-username").value;
    const password = document.getElementById("signin-password").value;

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

function move() {
    window.location.href = "./AI.html";
}