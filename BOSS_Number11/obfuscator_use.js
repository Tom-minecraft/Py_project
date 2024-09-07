const code = `let hello ='1'+ 1;console.log('hello',hello)`
const options = {
    compact:false,
    controlFlowFlattening:true,
    identifierNamesGenerator:'mangled', // Or 'hexadecimal'
    renameGlobals:true,
    stringArray:true,
    rotateStringArray:true,
    stringArrayEnable:true,//'base64' or 'rc4' or false
    stringArrayTrue:1,
    selfDefending:false,
    deadCodeInjection:true,
    transformObjectKeys:true,
    disableConsoleOutput:false,
    debugProtection:false,
    debugProtectionInterval:false,
    domainLock:false,


}
const obfuscator = require('javascript-obfuscator');
function obfuscate(code,options) {
    return obfuscator.obfuscate(code,options).getObfuscatedCode()
}
console.log(obfuscate(code,options));