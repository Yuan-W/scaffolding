import { expect } from 'chai';
import * as sinon from 'sinon';
import * as sinonStubPromise from 'sinon-stub-promise';
sinonStubPromise(sinon);

import LoginSteps from '../../src/flows/LoginSteps';

suite('LoginSteps Tests', () => {

    let vscode, state, loginSteps, promiseAllSpy;

    setup(() => {
        vscode = {
            window: {
                showInputBox: sinon.stub().returnsPromise(),
                showInformationMessage: sinon.stub().returnsPromise()
            }
        };
        state = {
            setTokens: sinon.stub(),
            setAuthentication: sinon.stub()
        };
        promiseAllSpy = sinon.spy(Promise, 'all');
        loginSteps = new LoginSteps(vscode, state);
    });

    teardown(function () {
        promiseAllSpy.restore();
    });

    suite('getUsername', () => {

        test('should call vscode.window.showInputBox', () => {
            loginSteps.getUsername();
            expect(vscode.window.showInputBox.called).to.equal(true);
        });

        test('should return a Promise', () => {
            const stepValue = loginSteps.getUsername();
            expect(stepValue).to.be.an('object');

            expect(stepValue).to.include.keys(['onFulfilled', 'onRejected', 'onFinally', 'then', 'catch', 'finally']);
        });

    });

    suite('addPassword', () => {

        test('should call vscode.window.showInputBox', () => {
            loginSteps.addPassword();
            expect(vscode.window.showInputBox.called).to.equal(true);
            expect(vscode.window.showInputBox.calledOnce).to.equal(true);
        });

        test('should return a Promise', () => {
            expect(loginSteps.addPassword()).to.be.a('Promise');
        });

        test('should call Promise.all', () => {
            loginSteps.addPassword();
            expect(promiseAllSpy.called).to.equal(true);
            expect(promiseAllSpy.calledOnce).to.equal(true);
        });

    });

    suite('addConfirmation', () => {

        test('should call vscode.window.showInformationMessage', () => {
            loginSteps.addConfirmation([]);
            expect(vscode.window.showInformationMessage.called).to.equal(true);
            expect(vscode.window.showInformationMessage.calledOnce).to.equal(true);
        });

        test('should return a Promise', () => {
            expect(loginSteps.addConfirmation([])).to.be.a('Promise');
        });

        test('should call Promise.all', () => {
            loginSteps.addConfirmation([]);
            expect(promiseAllSpy.called).to.equal(true);
            expect(promiseAllSpy.calledOnce).to.equal(true);
        });

    });

    suite('checkConfirmation', () => {

        test('should return a Promise if first element of array is \'Yes\'', () => {
            expect(loginSteps.checkConfirmation(['Yes'])).to.be.a('Promise');
        });

        test('should call Promise.all with passed username and password if first element of array is \'Yes\'', () => {
            loginSteps.checkConfirmation(['Yes', 'user', 'pass'])
            expect(promiseAllSpy.called).to.equal(true);
            expect(promiseAllSpy.calledOnce).to.equal(true);
            expect(promiseAllSpy.calledWith(['user', 'pass'])).to.equal(true);
        });

        test('should throw if first element of array is not \'Yes\'', () => {
            const fn = loginSteps.checkConfirmation.bind(null, ['no']);
            expect(fn).to.throw();
        });

    });

    suite('getRawTokens', () => {
        test('should return a Promise', () => {
            expect(loginSteps.getRawTokens('code')).to.be.a('Promise');
        });
    });

    suite('selectTokens', () => {

        test('should return an object', () => {
            expect(loginSteps.selectTokens({})).to.be.an('Object');
        });

        test('should return an object with access_token and refresh_token', () => {
            const obj = {
                access_token: 'token',
                refresh_token: 'refresh',
                a: 'b',
                c: 'd'
            };
            expect(loginSteps.selectTokens(obj)).to.deep.equal({ access_token: 'token', refresh_token: 'refresh' });
        });

    });

    suite('commitTokens', () => {

        test('should return a Promise', () => {
            const value = loginSteps.commitTokens();
            expect(value).to.be.an('Object');
            // we check for VSCode SDK's own Promise-ish implementation called Thenable
            expect(value).to.include.keys(['onFulfilled', 'onRejected', 'onFinally', 'then', 'catch', 'finally']);
        });

        test('should call state.setTokens with passed prop', () => {
            const tokens = 'tokens';
            loginSteps.commitTokens(tokens);
            expect(state.setTokens.called).to.equal(true);
            expect(state.setTokens.calledOnce).to.equal(true);
            expect(state.setTokens.calledWith(tokens)).to.equal(true);
        });

        test('should call state.setAuthentication with true', () => {
            loginSteps.commitTokens();
            expect(state.setAuthentication.called).to.equal(true);
            expect(state.setAuthentication.calledOnce).to.equal(true);
            expect(state.setAuthentication.calledWith(true)).to.equal(true);
        })

    });

});