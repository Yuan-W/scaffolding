const failedRegex = /[0-9]* failed/g;
const passedRegex = /[0-9]* passed/g;

const failedTestNameRegex = /([_]+ ([a-zA-Z]|_)* [_]+)/g;

export function parseFunctionName(raw) {
    return raw.replace(/[_]+ /,'').replace(/ [_]+/, '');
}

function extractTestResults(rawTestResults) {
    const [ rawFailed ] = rawTestResults.match(failedRegex) || [];
    const [ rawPassed ] = rawTestResults.match(passedRegex) || [];
    const rawFailedTests = rawTestResults.match(failedTestNameRegex) || [];

    const [ failedNumber = '0' ] = rawFailed && rawFailed.split(' ') || [];
    const [ passedNumber = '0' ] = rawPassed && rawPassed.split(' ') || [];

    const failed = {
        number: failedNumber && Number(failedNumber),
        tests: rawFailedTests.map(parseFunctionName)
    };
    const passed = {
        number: passedNumber && Number(passedNumber)
    };
    return {
        failed,
        passed
    };
}

export default extractTestResults;
