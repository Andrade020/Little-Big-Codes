const { ipcRenderer } = require('electron');

document.getElementById('processButton').addEventListener('click', () => {
    const inputText = document.getElementById('inputText').value;
    ipcRenderer.send('process-code', inputText);
});

ipcRenderer.on('processed-code', (event, processedText) => {
    document.getElementById('outputText').value = processedText;
});
