function showSettingPopup() {
    const overlay = document.getElementById("overlay");
    const popup = document.getElementById("popup");

    overlay.classList.add("active");
    setTimeout(() => {
        popup.classList.add("slide-in");
    }, 10); // 遅延を設定してスライドアニメーションを確実に発火
}

function closeSettingPopup() {
    const overlay = document.getElementById("overlay");
    const popup = document.getElementById("popup");

    popup.classList.remove("slide-in");
    setTimeout(() => {
        overlay.classList.remove("active");
    }, 500); // アニメーションが完了するまで待機
}
document.getElementById("overlay").addEventListener("click", closeSettingPopup);
// ポップアップ内をクリックしてもイベントが伝播しないようにする
document.getElementById("popup").addEventListener("click", function(event) {
    event.stopPropagation();
});
function logout() {
    window.location.href = "./home.html";
}