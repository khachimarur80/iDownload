console.log("Executing backround script.")

function downloadImagesInFolder(folderName, imageArray) {
  let totalJPGs = imageArray.filter((imageData) => {
    const imageExt = imageData.url.split('.').pop().split('?')[0].toLowerCase();
    return imageExt !== 'gif';
  });

  let imageDownloads = totalJPGs.map((imageData) => {
    const { name, url } = imageData;
    const imageExt = url.split('.').pop().split('?')[0].toLowerCase();
    const downloadOptions = {
      url: url,
      filename: folderName + '/' + name + '.jpg',
    };
    
    return new Promise((resolve) => {
      chrome.downloads.download(downloadOptions, () => {
        resolve();
      });
    });
  });

  Promise.all(imageDownloads).then(() => {
    const textFileData = '';
    const downloadTxtOptions = {
      url: 'data:text/plain;charset=utf-8,' + encodeURIComponent(textFileData),
      filename: 'DOWNLOAD.txt',
    };
    chrome.downloads.download(downloadTxtOptions, () => {
      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const tabId = tabs[0].id;
        chrome.tabs.remove(tabId);
      });
    });
  });
}


chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.data) {
  	console.log("Downloading Image.")
  	console.log(message.data)
  	downloadImagesInFolder('Images', message.data)
  }
});