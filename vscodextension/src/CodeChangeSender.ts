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
        const changes = this.codeChanges.getChangesPayload();
        clearInterval(this.sendInterval);
        // this is an example of how to make a POST request to an address using axios
        fetch.post(URL, { changes })
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