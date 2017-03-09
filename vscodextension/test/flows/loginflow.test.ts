import { expect } from 'chai';
import * as sinon from 'sinon';
import * as sinonStubPromise from 'sinon-stub-promise';
sinonStubPromise(sinon);

import { loginFlow } from '../../src/flows';
import LoginSteps from '../../src/flows/LoginSteps';

suite('Login Flow Tests', () => {

    suite('loginFlow', () => {

        let vscode, state, steps;

        let getUsernameStub, addPasswordStub, addConfirmationStub, checkConfirmationStub,
        getAuthorizationCodeStub, getDataStub, getRawTokensStub, selectTokensStub,
        commitTokensStub;

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
            steps = new LoginSteps(vscode, state);

            getUsernameStub = sinon.stub(steps, 'getUsername').returnsPromise();
            addPasswordStub = sinon.stub(steps, 'addPassword').returnsPromise();
            addConfirmationStub = sinon.stub(steps, 'addConfirmation').returnsPromise();
            checkConfirmationStub = sinon.stub(steps, 'checkConfirmation').returnsPromise();
            getAuthorizationCodeStub = sinon.stub(steps, 'getAuthorizationCode').returnsPromise();
            getDataStub = sinon.stub(steps, 'getData').returnsPromise();
            getRawTokensStub = sinon.stub(steps, 'getRawTokens').returnsPromise();
            selectTokensStub = sinon.stub(steps, 'selectTokens').returnsPromise();
            commitTokensStub = sinon.stub(steps, 'commitTokens').returnsPromise();
        });

        test('should call steps.getUsername', () => {
            loginFlow(vscode, state, steps);
            expect(getUsernameStub.called).to.equal(true);
            expect(getUsernameStub.calledOnce).to.equal(true);
        });

        test('should call steps.addPassword', () => {
            steps.getUsername.resolves();
            loginFlow(vscode, state, steps);
            expect(addPasswordStub.called).to.equal(true);
            expect(addPasswordStub.calledOnce).to.equal(true);
        });

        test('should call steps.addConfirmation', () => {
            steps.getUsername.resolves();
            steps.addPassword.resolves();
            loginFlow(vscode, state, steps);
            expect(addConfirmationStub.called).to.equal(true);
            expect(addConfirmationStub.calledOnce).to.equal(true);
        });

        test('should call steps.checkConfirmation', () => {
            steps.getUsername.resolves();
            steps.addPassword.resolves();
            steps.addConfirmation.resolves();
            loginFlow(vscode, state, steps);
            expect(checkConfirmationStub.called).to.equal(true);
            expect(checkConfirmationStub.calledOnce).to.equal(true);
        });

        test('should call steps.getAuthorizationCode', () => {
            steps.getUsername.resolves();
            steps.addPassword.resolves();
            steps.addConfirmation.resolves();
            steps.checkConfirmation.resolves();
            loginFlow(vscode, state, steps);
            expect(getAuthorizationCodeStub.called).to.equal(true);
            expect(getAuthorizationCodeStub.calledOnce).to.equal(true);
        });

        test('should call steps.getData', () => {
            steps.getUsername.resolves();
            steps.addPassword.resolves();
            steps.addConfirmation.resolves();
            steps.checkConfirmation.resolves();
            steps.getAuthorizationCode.resolves();
            loginFlow(vscode, state, steps);
            expect(getDataStub.called).to.equal(true);
            expect(getDataStub.calledOnce).to.equal(true);
        });

        test('should call steps.getRawTokens', () => {
            steps.getUsername.resolves();
            steps.addPassword.resolves();
            steps.addConfirmation.resolves();
            steps.checkConfirmation.resolves();
            steps.getAuthorizationCode.resolves();
            steps.getData.resolves();
            loginFlow(vscode, state, steps);
            expect(getRawTokensStub.called).to.equal(true);
            expect(getRawTokensStub.calledOnce).to.equal(true);
        });

        test('should call steps.selectTokens', () => {
            steps.getUsername.resolves();
            steps.addPassword.resolves();
            steps.addConfirmation.resolves();
            steps.checkConfirmation.resolves();
            steps.getAuthorizationCode.resolves();
            steps.getData.resolves();
            steps.getRawTokens.resolves();
            loginFlow(vscode, state, steps);
            expect(selectTokensStub.called).to.equal(true);
            expect(selectTokensStub.calledOnce).to.equal(true);
        });

        test('should call steps.commitTokens', () => {
            steps.getUsername.resolves();
            steps.addPassword.resolves();
            steps.addConfirmation.resolves();
            steps.checkConfirmation.resolves();
            steps.getAuthorizationCode.resolves();
            steps.getData.resolves();
            steps.getRawTokens.resolves();
            steps.selectTokens.resolves()
            loginFlow(vscode, state, steps);
            expect(commitTokensStub.called).to.equal(true);
            expect(commitTokensStub.calledOnce).to.equal(true);
        });

    });

});