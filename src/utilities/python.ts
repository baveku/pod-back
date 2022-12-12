import { PythonShell } from 'python-shell'
const DIR_SCRIPT_PATH = 'python'
type PythonScript = 'change_text'

// @ts-ignore
const RESOURCE_PATH = process.resourcesPath

const getPythonFile = (script: PythonScript) => {
  switch (script) {
    case 'change_text':
      return 'main.py'
  }
}

const changeTextPyScript = (type: PythonScript, args: any[] = []) => {
  let filePath = DIR_SCRIPT_PATH + '/' + getPythonFile(type)
  if (RESOURCE_PATH) {
    filePath = RESOURCE_PATH + '/' + filePath
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
