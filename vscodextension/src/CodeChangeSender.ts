import axios from 'axios';
import CodeChanges from './CodeChanges';

const BASE_URL = 'https://jsonplaceholder.typicode.com/posts';
const URL = BASE_URL;

class CodeChangeSender {
    private codeChanges: CodeChanges;
    private sendInterval: any;
    constructor(codeChanges: CodeChanges) {
        this.codeChanges = codeChanges;
        this.resetSendInterval(5000);
    }
    getSendInterval() {
        return this.sendInterval;
    }
    resetSendInterval(time : number = 5000) {
        clearInterval(this.sendInterval);
        this.sendInterval = setInterval(this.send.bind(this), time);
    }
    send(fetch = axios) {
        const changes = this.codeChanges.getChanges();
        const startTime = this.codeChanges.getStartTime();
        const { code = '' } = Array.isArray(changes) ? changes.slice(-1)[0] : {};
        const timeSpent = Date.now() - startTime;
        clearInterval(this.sendInterval);

        fetch.post(URL, { code, timeSpent })
            .then( ({ data }) => {
                this.codeChanges.updateHint(data);
                this.resetSendInterval(5000);
            })
            .catch( (e) => {
                console.log(e);
            });
    }
}

export default CodeChangeSender;