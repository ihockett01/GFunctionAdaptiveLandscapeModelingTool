import { app, BrowserWindow, screen } from 'electron'
import * as path from 'path'
import * as child from 'child_process'
import * as fs from 'fs'
import * as ping from 'ping'
import * as url from 'url'

const PY_DIST_FOLDER = 'pydist'
const PY_MODULE = 'cli' // without .py suffix
const SERVER_APP = url.fileURLToPath(`file://${__dirname}/${PY_DIST_FOLDER}/${PY_MODULE}.app`)
const SERVER_ENDPOINT = 'http://localhost:1400/'
const SERVER_PING = 'ping'
const SERVER_SHUTDOWN = 'shutdown'
let pyProc : child.ChildProcessWithoutNullStreams
let serverIsRunning = false

let win: BrowserWindow = null
const args = process.argv.slice(1)
const serve = args.some(val => val === '--serve')

// Window setup logic

function createWindow (): BrowserWindow {
  console.log('starting')

  const electronScreen = screen
  const size = electronScreen.getPrimaryDisplay().workAreaSize

  // Create the browser window.
  win = new BrowserWindow({
    x: 0,
    y: 0,
    width: size.width,
    height: size.height,
    webPreferences: {
      nodeIntegration: true,
      allowRunningInsecureContent: !!(serve),
      contextIsolation: false, // false if you want to run 2e2 test with Spectron
      enableRemoteModule: true // true if you want to run 2e2 test  with Spectron or use remote module in renderer context (ie. Angular)
    }
  })

  console.log(win)

  const entryPoint = url.fileURLToPath(`file://${__dirname}/dist/index.html`)
  fileExists(entryPoint)
  win.loadURL(entryPoint)

  // Emitted when the window is closed.
  win.on('closed', () => {
    console.log('closing')
    // Dereference the window object, usually you would store window
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    win = null
  })

  return win
}

// Python setup logic

const createPyProc = () => {
  fileExists(SERVER_APP)
  // let scriptPath = path.resolve('cli.py');
  // pyProc = child.execFile(script);
  pyProc = child.spawn('open', [SERVER_APP])
  pyProc.addListener('error', function (err) {
    console.log(err)
  }).addListener('message', function (message) {
    console.log(message)
  })

  pingServer()
}

const pingServer = () => {
  console.log(`ping server: ${SERVER_ENDPOINT}${SERVER_PING}`)
  ping.sys.probe(`${SERVER_ENDPOINT}${SERVER_PING}`, pingResult, {
    timeout: 5000
  })
}

const pingResult = (result) => {
  console.log('result:' + JSON.stringify(result))
  if (result) {
    serverIsRunning = true
  } else {
    console.error('failed to load server')
  }
}

const shutdownServer = () => {
  if (serverIsRunning) {
    ping.sys.probe(`${SERVER_ENDPOINT}${SERVER_SHUTDOWN}`, shutDownResult, {})
  }

  serverIsRunning = false
}

const shutDownResult = (result) => {
  serverIsRunning = false
}

const exitPyProc = () => {
  console.log('exiting py proc')
  shutdownServer()
  pyProc.kill()
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
  setTimeout(createWindow, 400)
  setTimeout(createPyProc, 400)
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
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (win === null) {
    createWindow()
  }

  if (pyProc === null) {
    createPyProc()
  }
})

app.on('will-quit', exitPyProc)
