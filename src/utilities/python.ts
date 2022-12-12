import child_process from 'child_process'
import path from 'path'
const DIR_SCRIPT_PATH = ''

// @ts-ignore
const RESOURCES_PATH = process.sanboxed ? process.resourcesPath : ''
type PythonScript = 'change_text'

const getPythonFile = (script: PythonScript) => {
  switch (script) {
    case 'change_text':
      return 'main.py'
  }
}

const changeTextPyScript = (type: PythonScript, args: any[] = []) => {
  console.log(process)

  const isWindows = /^win/i.test(process.platform)
  const fileName = !isWindows ? 'main' : 'main.exe'
  const filePath = path.join(RESOURCES_PATH, DIR_SCRIPT_PATH, 'bin', fileName)
  const argsStr = args.join(' ')
  child_process.exec(`${filePath} ${argsStr}`, (err, stdout, stderr) => {
    if (err) {
      console.log(err)
    }
    console.log(stdout, stderr)
  })
}
const PyScript = {
  changeTextPyScript,
}
export default PyScript
