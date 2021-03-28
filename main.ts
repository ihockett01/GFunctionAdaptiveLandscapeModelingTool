import { app, BrowserWindow, screen } from 'electron'
import * as path from 'path'
import * as child from 'child_process'
import * as fs from 'fs'
import * as url from 'url'
import * as fetch from 'node-fetch'
import * as pRetry from 'p-retry'

const ENTRY_POINT = `file://${path.join(__dirname, 'dist/index.html')}`
const PY_DIST_FOLDER = '../pydist'
const PY_MODULE = 'gfunctionapibootstrapper' // without .py suffix

const SERVER_APP = url.fileURLToPath('file://' + path.join(__dirname, PY_DIST_FOLDER) + '/' + PY_MODULE + '.app')
const SERVER_ENDPOINT = 'http://localhost:1400/'
const SERVER_PING = 'ping'
const SERVER_SHUTDOWN = 'shutdown'

let pyProc  = null;
let serverIsRunning = false

let win: BrowserWindow = null
const args = process.argv.slice(1)
const serve = args.some(val => val === '--serve')

// Window setup logic

function createWindow (): BrowserWindow {
  console.log('starting')

  const electronScreen = screen;
  const size = electronScreen.getPrimaryDisplay().workAreaSize;

  // Create the browser window.
  win = new BrowserWindow({
    x: 0,
    y: 0,
    width: size.width,
    height: size.height,
    webPreferences: {
      nodeIntegration: true,
      allowRunningInsecureContent: (serve) ? true : false,
      contextIsolation: false,  // false if you want to run 2e2 test with Spectron
      enableRemoteModule : true // true if you want to run 2e2 test  with Spectron or use remote module in renderer context (ie. Angular)
    },
  });

  if (serve) {
    console.log('serve')
    win.webContents.openDevTools();

    require('electron-reload')(__dirname, {
      electron: require(`${__dirname}/node_modules/electron`)
    });
    win.loadURL('http://localhost:4200');

  } else {
    fileExists(ENTRY_POINT)
    win.loadURL(url.format(new url.URL(ENTRY_POINT), {

    }))
  }

  // Emitted when the window is closed.
  win.on('closed', () => {
    // Dereference the window object, usually you would store window
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    win = null;
  });

  return win
}

// Python setup logic

const createPyProc = () => {
  fileExists(SERVER_APP)
  
  pyProc = child.spawn('open', [SERVER_APP])
  pyProc.addListener('error', function (err) {
    console.log(err)
  }).addListener('message', function (message) {
    console.log(message)
  }).addListener('disconnect', function(d) {
    console.log(d);
  })

  return pingServer()
}

const pingServer = () => {
    const pingResult = pRetry(fetchPage, {onFailedAttempt: error => {
			console.log(`Attempt ${error.attemptNumber} failed. There are ${error.retriesLeft} retries left.`);
		},
		retries: 5})

    return pingResult
}

async function fetchPage () {
  const response = await fetch(`${SERVER_ENDPOINT}${SERVER_PING}`, {})

  // Abort retrying if the resource doesn't exist
  if (response.status === 404) {
    throw new pRetry.AbortError(response.statusText)
  }

  return response.blob()
}

const shutdownServer = () => {
  fetch(`${SERVER_ENDPOINT}${SERVER_SHUTDOWN}`, {}).then(shutDownResult)
}

const shutDownResult = (result) => {
  serverIsRunning = false
}

const exitPyProc = () => {
  console.log('exiting py proc')
  shutdownServer()
  if (pyProc) pyProc.kill()
  pyProc = null
}

const fileExists = (filePath: string) => {
  const fullPath = path.resolve(filePath)
  const hasPackage = fs.existsSync(fullPath)
  console.log(`${fullPath}: ${hasPackage}`)
  return hasPackage
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
// Added 400 ms to fix the black background issue while using transparent window. More detais at https://github.com/electron/electron/issues/15947
app.on('ready', () => {
  console.log('ready')
  const result = createPyProc()

  result.then(() => setTimeout(createWindow, 400)).catch((err) => {
    console.log(err);
  })
})

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  console.log('all windows closed')
  // On OS X it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  console.log('activating')
  // if (pyProc === null) {
  //   createPyProc()
  // }

  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (win === null) {
    createWindow()
  }
})

app.on('will-quit', exitPyProc)
