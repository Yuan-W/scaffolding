import { exec } from 'child_process';
import fs from 'fs';
import promisify from 'es6-promisify';

const writeFile = promisify(fs.writeFile);
const readFile = promisify(fs.readFile);

export default class Sandbox {
    constructor({ timeoutValue, path, folder, vmName, compilerName, fileName, code, outputCommand, languageName, extraArguments, stdinData }) {
        this.timeoutValue = timeoutValue;
        this.path = path;
        this.folder = folder;
        this.vmName = vmName;
        this.compilerName = compilerName;
        this.fileName = fileName;
        this.code = code;
        this.outputCommand = outputCommand;
        this.languageName = languageName;
        this.extraArguments = extraArguments;
        this.stdinData = stdinData;
    }
    run(success) {
        this.prepare(() => {
            this.execute(success);
        });
    }
    prepare(success) {
        exec(
            `mkdir ${this.path}${this.folder} && cp ${this.path}/payload/* ${this.path}${this.folder} && chmod 777 ${this.path}${this.folder}`, 
            (stdout) => {
                writeFile(
                    `${this.path}${this.folder}/${this.fileName}`,
                    this.code
                ).then( () => {
                    console.log(this.languageName + " file was saved!");
                    exec(`chmod 777 '${this.path}${this.folder}/${this.fileName}'`);
                    return writeFile(`${this.path}${this.folder}/inputFile`, this.stdinData);
                }).then( () => {
                    console.log('Input file was saved');
                    success();
                }).catch( (err) => {
                    console.log(err);
                });
            }
        );
    }
    execute(success) {
        let myC = 0;

        const statement = `${this.path}DockerTimeout.sh ${this.timeoutValue}s -e 'NODE_PATH=/usr/local/lib/node_modules' -i -t -v  "${this.path}${this.folder}":/usercode ${this.vmName} /usercode/script.sh ${this.compilerName} ${this.fileName} ${this.outputCommand} ${this.extraArguments};`
        console.log(statement);
        exec(statement);
        console.log('----------------------------');

        const interval = setInterval( () => {
            myC = myC + 1;
            readFile(`${this.path}${this.folder}/completed`, 'utf8')
                .then( (data) => {
                    if(myC < this.timeoutValue) {
                        console.log('DONE');
                        const completed = (data, readErrorFile) => {
                            readErrorFile.then( (errorData = '') => {
                                console.log('Error file: ', errorData);
                                console.log('Main File', data);
                                const [ parsedData, time ] = data.toString().split('*-COMPILEBOX::ENDOFOUTPUT-*');
                                console.log('Time: ', time);
                                success(parsedData, time, errorData);
                                this.cleanup(interval);
                            });
                        }
                        return completed(data, readFile(`${this.path}${this.folder}/errors`, 'utf8'));
                    } else {
                        const timedOut = (readLogFile) => {
                            readLogFile.then( (data = '') => {
                                data += "\nExecution Timed Out";
                                console.log(`Timed Out: ${this.folder} ${this.languageName}`);
                                readFile(
                                    `${this.path}${this.folder}/errors`,
                                    'utf8'
                                ).then( (errorData = '') => {
                                    const [ parsedData, time ] = data.toString().split('*---*');
                                    console.log('Time: ', time);
                                    success(parsedData, errorData);
                                    this.cleanup(interval);
                                }).catch( (err) => {
                                    console.log(err);
                                });
                            });
                        };
                        return timedOut(readFile(this.path + this.folder + '/logfile.txt', 'utf8'));
                    }
                }).catch( (err) => {
                    console.log(err);
                })
        }, 1000);
    }
    cleanup(interval) {
        console.log('ATTEMPTING TO REMOVE: ' + this.folder);
        console.log('------------------------------');
        exec('rm -r ' + this.folder);
        clearInterval(interval);
    }
}