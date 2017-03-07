import {
    fetchAuthorizationCode,
    fetchToken,
    showLoginSuccess
} from '../actions';

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
    }).then(([username, password]) => {
        return fetchAuthorizationCode(username, password);
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