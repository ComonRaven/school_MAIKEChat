function updateIframe() {
  const select = document.getElementById('language-select');
  const iframe = document.getElementById('language-iframe');
  const selectedLanguage = select.value;

  // 言語に基づいて表示するURLを変更
  if (selectedLanguage === 'C') {
    iframe.src = "https://paiza.io/projects/e/2Nky9ZxFHFepkvg1DC0LSA?theme=ambiance"; // C言語用のiframe URL
  } else if (selectedLanguage === 'C#') {
    iframe.src = "https://paiza.io/projects/e/bCl7j5ELHjYyPVSJxIKvCg?theme=ambiance"; // C#用のiframe URL
  } else if (selectedLanguage === 'C++') {
    iframe.src = "https://paiza.io/projects/e/MW9I6PhIts_-LUbVKJpZlg?theme=ambiance"; // フランス語用のiframe URL
  } else if (selectedLanguage === 'Python3') {
    iframe.src = "https://paiza.io/projects/e/XF-fKHHXdX8Vlh0p_eYbVA?theme=ambiance"; // Python3用のiframe URL
  } else if (selectedLanguage === 'Python2') {
    iframe.src = "https://paiza.io/projects/e/sHA2gXgrA1IikNTOl2iX0w?theme=ambiance"; // Python2用のiframe URL
  } else if (selectedLanguage === 'JavaScript') {
    iframe.src = "https://paiza.io/projects/e/Yt6zrkB-qcmZqWRaPhEOMQ?theme=ambiance"; // JavaScript用のiframe URL
  } else if (selectedLanguage === 'Java') {
    iframe.src = "https://paiza.io/projects/e/vxu9guRjHwh0vaPHiNW0hQ?theme=ambiance"; // Java用のiframe URL
  } else if (selectedLanguage === 'Ruby') {
    iframe.src = "https://paiza.io/projects/e/MgjyoBAsyEIuCz0aAEsxZQ?theme=ambiance"; // Ruby用のiframe URL
  } else if (selectedLanguage === 'PHP') {
    iframe.src = "https://paiza.io/projects/e/g7PeJOOmXhHfaxKkReBMxw?theme=ambiance"; // PHP用のiframe URL
  }
}

// 初期表示で英語のiframeを表示
window.onload = function() {
  updateIframe();
}