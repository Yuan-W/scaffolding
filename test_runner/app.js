import express from 'express';
import ExpressBrute from 'express-brute';
import morgan from 'morgan';

import * as compile from './compile';
import extractTestResults from './extractTestResults';

const app = express.createServer();
const port = process.env.PORT || 5004;

const store = new ExpressBrute.MemoryStore(); // stores state locally, don't use this in production
const bruteforce = new ExpressBrute(store, {
    freeRetries: 50,
    lifetime: 3600
});

app.use(morgan('combined'));

app.use(express.static(__dirname));
app.use(express.bodyParser());

app.all('*', function (req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'POST');
    res.header('Access-Control-Allow-Headers', 'Content-Type');

    next();
});

app.post('/test', bruteforce.prevent, function (req, res) {

    const { language = 0, code, testCode } = req.body;
    if(!code || !testCode) {
        return res.status(400).send('Parameters code or testCode are not valid');
    }
    const fullCode = code + '\n' + testCode;

    compile.run({
        language,
        code: fullCode,
        stdin: undefined
    }, function (data, time, errors) {
        const results = extractTestResults(data);
        res.send({ results, errors, time });
    });

});

console.log('Listening on port:', port)
app.listen(port);

export default app;
