import { expect } from 'chai';
import extractTestResults, { parseFunctionName } from './extractTestResults';

const failedTestOutput = `=================================== FAILURES ===================================
_____________________________ test_function _____________________________

    def test_function():
>   	assert False
E    assert False

usercode/test_file.py:7: AssertionError
_____________________________ test_second_function _____________________________

    def test_second_function():
>   	assert False
E    assert False

usercode/test_file.py:7: AssertionError`

const statusLineAllFailed = `
=========================== 2 failed in 0.10 seconds ===========================
`;
const statusLineSomeFailed = `
====================== 1 failed, 1 passed in 0.08 seconds ======================
`;
const statusLineAllPassed = `
=========================== 2 passed in 0.05 seconds ===========================
`;
const compilationFailedMessage = 'Compilation Failed';

describe('extractTestResults', () => {
    it('should parse the correct number of passed tests', () => {
        let { passed } = extractTestResults(statusLineAllFailed);
        expect(passed.number).to.equal(0);

        ({ passed } = extractTestResults(statusLineAllPassed));
        expect(passed.number).to.equal(2);

        ({ passed } = extractTestResults(statusLineSomeFailed));
        expect(passed.number).to.equal(1);
    });
    it('should parse the correct number of failed tests', () => {
        let { failed } = extractTestResults(statusLineAllFailed);
        expect(failed.number).to.equal(2);

        ({ failed } = extractTestResults(statusLineAllPassed));
        expect(failed.number).to.equal(0);

        ({ failed } = extractTestResults(statusLineSomeFailed));
        expect(failed.number).to.equal(1);
    });

    it('should return the correct failed tests', () => {
        let { failed } = extractTestResults(failedTestOutput);
        expect(failed.tests).to.deep.equal([ 'test_function', 'test_second_function' ]);
    });
});

describe('parseFunctionName', () => {
    it('should parse the correct function name', () => {
        expect(parseFunctionName('______ function_name _______')).to.equal('function_name');
    });
});
