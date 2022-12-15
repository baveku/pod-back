import child_process from 'child_process'
import path from 'path'
const DIR_SCRIPT_PATH = ''

// @ts-ignore
const RESOURCES_PATH = // @ts-ignore
  process.env.NODE_ENV !== 'DEV' ? process.resourcesPath : ''
type PythonScript = 'change_text'

const getProgramPath = () => {
  const isWindows = /^win/i.test(process.platform)
  const mainCmd = 'main'
  let ext = ''

  if (isWindows) {
    ext = 'exe'
  }

  return ext.length > 0 ? `${mainCmd}.${ext}` : mainCmd
}

// PROGRAM
const changeText = (type: PythonScript, args: any[] = []) => {
  return new Promise((resolve, reject) => {
    const filePath = path
      .join(RESOURCES_PATH, 'bin', getProgramPath())
      .replace('Program Files', `"Program Files"`)
    const argsStr = args.join(' ')
    const cmd = `"${filePath}" ${argsStr}`
    const spawn = child_process.spawn(`${filePath}`, args, { shell: true })
    spawn.stdout.on('data', (data) => {
      console.log(data.toString())
    })

    spawn.stderr.on('data', (data) => {
      console.error(data.toString())
    })

    spawn.on('close', (code) => {
      console.log(`Child exited with code ${code}`)
      resolve(cmd)
    })
  })
}
const PyScript = {
  changeText,
}
export default PyScript
