import { PythonShell } from 'python-shell'
const DIR_SCRIPT_PATH = 'scripts'
type PythonScript = 'change_text'

const getPythonFile = (script: PythonScript) => {
  switch (script) {
    case 'change_text':
      return 'pts.py'
  }
}

const changeTextPyScript = (type: PythonScript, args: string[] = []) => {
  const path = DIR_SCRIPT_PATH + '/' + getPythonFile(type)
  PythonShell.run(path, { args }, (err, result) => {
    if (err) console.log(err)
    console.log(result?.join('\n'))
  })
}
const PyScript = {
  changeTextPyScript,
}
export default PyScript
