console.log("Executing content.js script.")


function extractFigures() {
  const figures = document.querySelectorAll('figure');
  const figureData = [];

  figures.forEach((figure) => {
    const caption = figure.querySelector('figcaption');
    const image = figure.querySelector('img');

    if (caption && image) {
      const captionText = caption.textContent.trim()+" - "+figureData.length;
      const imageURL = image.src;

      figureData.push({ name: captionText, url: imageURL });
    }

    if (image && !caption) {
      const captionText = "Flashcard - "+figureData.length
      const imageURL = image.src;

      figureData.push({ name: captionText, url: imageURL });
    }

  });

  return figureData;
}

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.message === "DownloadImage") {
  	console.log("Initiating Image Downloading.")
  	const figureData = extractFigures();
  	console.log(figureData)
  	chrome.runtime.sendMessage({ data: figureData });
  }
});