const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

let mainWindow;

app.whenReady().then(() => {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });
    mainWindow.loadFile('index.html');
});

function normalizeWord(word) {
    word = word.toLowerCase();
    word = word.replace(/ç/g, 'c').replace(/é/g, 'eh');
    return word.normalize('NFKD').replace(/\p{Diacritic}/gu, '');
}

const SLANG_DICT = {
    "voce": "vc",
    "porque": "pq",
    "qualquer": "qqr",
    "programacao": "prog",
    "amigo": "amg",
    "comigo": "cmg",
    "valeu": "vlw",
    "projeto": "proj"
};

function abbreviateWord(word) {
    const vowels = "aeiou";
    if (word.length <= 3) return word;
    
    if (word.length <= 7) {
        const prefix = word.slice(0, 2);
        const mid = word.slice(2, -1).replace(/[aeiou]/g, '');
        const suffix = word.slice(-1);
        return prefix + mid + suffix;
    }
    
    let abbr = word.slice(0, 2) + word.slice(2).replace(/[aeiou]/g, '');
    return abbr.length > 6 ? abbr.slice(0, 6) : abbr;
}

function slangifyText(text) {
    return text.split(/\b/).map(word => {
        const norm = normalizeWord(word);
        if (SLANG_DICT[norm]) return SLANG_DICT[norm];
        return Math.random() < 0.5 ? abbreviateWord(norm) : norm;
    }).join('');
}

ipcMain.on('process-code', (event, code) => {
    const processedCode = slangifyText(code);
    event.reply('processed-code', processedCode);
});
