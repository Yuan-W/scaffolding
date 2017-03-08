import {
    fetchAuthorizationCode,
    fetchToken,
    showLoginSuccess
} from '../actions';
import {
    clientId
} from '../constants';

export default function loginFlow(vscode, state) {
    return vscode.window.showInputBox({
        placeHolder: 'Username',
        prompt: 'Enter your username'
    }).then((username) => {
        const passwordInput = vscode.window.showInputBox({
            placeHolder: 'Password',
            prompt: 'Enter your password',
            password: true
        });
        return Promise.all([passwordInput, username]);
    }).then(([password, username]) => {
        const confirmationInput = vscode.window.showInformationMessage(`Do you authorize ${clientId}?`, 'Yes', 'No')
        return Promise.all([confirmationInput, username, password]);
    }).then(([authorisationResponse, username, password]) => {
        if(authorisationResponse === 'Yes') {
            return Promise.all([username, password]);
        }
        throw new Error(`${clientId} not authorized`);
    })
    .then(([username, password]) => {
        return fetchAuthorizationCode(username, password, clientId);
    }).then(({ data }) => {
        return data;
    })
    .then(fetchToken)
    .then(({ data }) => {
        return data;
    }).then(({ access_token, refresh_token }) => {
        return { access_token, refresh_token };
    }).then((tokens) => {
        state.setTokens(tokens);
        state.setAuthentication(true);
        return showLoginSuccess(vscode);
    });
}