import path from 'path'
import { PythonShell } from 'python-shell'
const DIR_SCRIPT_PATH = 'python'
type PythonScript = 'change_text'

const getPythonFile = (script: PythonScript) => {
  switch (script) {
    case 'change_text':
      return 'main.py'
  }
}

const changeTextPyScript = (type: PythonScript, args: any[] = []) => {
  let filePath = path.join(DIR_SCRIPT_PATH, getPythonFile(type))
  console.log(process)
  // @ts-ignore
  if (!process.sanboxed) {
    // @ts-ignore
    const RESOURCE_PATH = process.resourcesPath
    filePath = path.join(RESOURCE_PATH, DIR_SCRIPT_PATH, getPythonFile(type))
  }
  PythonShell.run(filePath, { args }, (err, result) => {
    if (err) console.log(err)
    console.log(result?.join('\n'))
  })
}
const PyScript = {
  changeTextPyScript,
}
export default PyScript
