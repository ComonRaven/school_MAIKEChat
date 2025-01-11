function showSettingPopup(){
    document.getElementById("overlay").style.display = "block";
    document.getElementById("popup").style.display = "block";
}

function closeSettingPopup() {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("popup").style.display = "none";
}
document.getElementById("overlay").addEventListener("click", closeSettingPopup);
// ポップアップ内をクリックしてもイベントが伝播しないようにする
document.getElementById("popup").addEventListener("click", function(event) {
    event.stopPropagation();
});
function logout() {
    window.location.href = "./home.html";
}