import {
    fetchAuthorizationCode,
    fetchToken
} from './actions';

export default function loginFlow(vscode, state) {
    return vscode.window.showInputBox({
        placeHolder: 'Username',
        prompt: 'Enter your username'
    }).then((username) => {
        vscode.window.showInputBox({
            placeHolder: 'Password',
            prompt: 'Enter your password',
            password: true
        }).then((password) => {
            return fetchAuthorizationCode(username, password);
        }).then(({ data }) => {
            return data;
        }).then((authorizationCode) => {
            return fetchToken(authorizationCode);
        }).then(({ data }) => {
            return data;
        }).then(({ access_token, refresh_token }) => {
            return { access_token, refresh_token };
        }).then((tokens) => {
            state.setTokens(tokens);
            state.setAuthentication(true);
        }).then(() => {
            vscode.window.showInformationMessage('Start Coding, you can request a hint any time');
        });
    });
}