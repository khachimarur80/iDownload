console.log("Executing popup script.")

document.addEventListener('DOMContentLoaded', function () {
  const downloadButton = document.getElementById('downloadInit');

  downloadButton.addEventListener('click', function () {
    downloadImage();
  });
});

function downloadImage() {
	chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      const activeTab = tabs[0];
      chrome.tabs.sendMessage(activeTab.id, { message: "DownloadImage" });
    });
}