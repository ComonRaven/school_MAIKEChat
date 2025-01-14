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