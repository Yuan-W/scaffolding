import express from 'express';
import ExpressBrute from 'express-brute';
import morgan from 'morgan';

import run from './compile';
import extractTestResults from './extractTestResults';

const app = express.createServer();
const port = 3000;

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
    res.header('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Content-Type');

    next();
});

app.post('/test', bruteforce.prevent, function (req, res) {

    const language = req.body.language;
    const code = req.body.code;
    const stdin = req.body.stdin;

    const testCode = 'def test_function():\n\tassert True\ndef test_second_function():\n\tassert False';

    const fullCode = code + '\n' + testCode;

    console.log(fullCode);

    run({
        language,
        code: fullCode,
        stdin
    }, function(data, time, errors) {
        const results = extractTestResults(data);
        res.send({ results, errors, time });
    });

});


app.get('/', function (req, res) {
    res.sendfile('./index.html');
});

console.log('Listening on port:',port)
app.listen(port);
