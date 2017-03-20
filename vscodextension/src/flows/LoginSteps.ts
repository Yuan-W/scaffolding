import {
    fetchAuthorizationCode,
    fetchToken,
    showLoginSuccess
} from '../actions';
import {
    clientId
} from '../constants';

class LoginSteps {
    vscode: any;
    state: any;
    constructor(vscode, state) {
        this.vscode = vscode;
        this.state = state;
        this.getUsername = this.getUsername.bind(this);
        this.addPassword = this.addPassword.bind(this);
        this.addConfirmation = this.addConfirmation.bind(this);
        this.commitTokens = this.commitTokens.bind(this);
    }
    getUsername() {
        return this.vscode.window.showInputBox({
            placeHolder: 'Username',
            prompt: 'Enter your username'
        });
    }
    addPassword(username) {
        const passwordInput = this.vscode.window.showInputBox({
            placeHolder: 'Password',
            prompt: 'Enter your password',
            password: true
        });
        return Promise.all([username, passwordInput]);
    }
    addConfirmation([username, password]) {
        const confirmationInput = this.vscode.window.showInformationMessage(`Do you authorize ${clientId}?`, 'Yes', 'No');
        return Promise.all([confirmationInput, username, password]);
    }
    checkConfirmation([authorisationResponse, username, password]) {
        if (authorisationResponse === 'Yes') {
            return Promise.all([username, password]);
        }
        throw new Error(`${clientId} not authorized`);
    }
    getAuthorizationCode([username, password]) {
        return fetchAuthorizationCode(username, password, clientId);
    }
    getRawTokens(authorizationCode) {
        return fetchToken(authorizationCode);
    }
    selectTokens({ access_token, refresh_token }) {
        return { access_token, refresh_token };
    }
    commitTokens(tokens) {
        this.state.setTokens(tokens);
        this.state.setAuthentication(true);
        return showLoginSuccess(this.vscode);
    }
}

export default LoginSteps;