import Sandbox from './sandbox/Sandbox';
import { compilerArray } from './sandbox/compilers';

function random(size) {
    //returns a crypto-safe random
    return require("crypto").randomBytes(size).toString('hex');
}

export function run({ language = 0, code, stdin }, callback) {
    const folder = 'temp/' + random(10);
    const path = __dirname + "/";
    const vmName = 'virtual_machine';
    const timeoutValue = 20; //seconds

    const [
        compilerName,
        fileName,
        outputCommand,
        languageName,
        extraArguments
    ] = compilerArray[language];

    const sandbox = new Sandbox({
        timeoutValue,
        path,
        folder,
        vmName,
        compilerName,
        fileName,
        code,
        outputCommand,
        languageName,
        extraArguments,
        stdin
    });

    sandbox.run(callback);
}
export default run;
