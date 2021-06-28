const [_, _2, env, arg1, arg2] = process.argv

let toPrint = 'executed node module'

if (env) {
    toPrint += ` in ${env}`
}

if (arg1 || arg2) {
    toPrint += ' with args:'
    console.log(toPrint)
    if (arg1) {
        console.log(arg1)
    }
    if (arg2) {
        console.log(arg2)
    }
} else {
    console.log(toPrint)
}