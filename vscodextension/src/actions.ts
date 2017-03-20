import axios from 'axios';
import {
    LOGIN_API_URL,
    AUTHORIZE_TOKEN_URL,
    HINTS_URL,
    EXERCISES_URL
} from './constants';
import ApplicationState from './ApplicationState';

export function debounce(fn, delay) {
    var timer = null;
    return function () {
        var context = this, args = arguments;
        clearTimeout(timer);
        timer = setTimeout(function () {
            fn.apply(context, args);
        }, delay);
    };
}

export function showHint(vscode, message) {
    return vscode.window.showInformationMessage(message);
}

export function showLoginSuccess(vscode) {
    return vscode.window.showInformationMessage('You\'ve logged in successfully');
}

export function showExerciseSelect(vscode, exercises) {
    return vscode.window.showQuickPick(
        exercises,
        { placeHolder: 'Select an exercise' }
    );
}

export function documentTextChangeHandler(state: ApplicationState) {
    return function (e) {
        const { document } = e;
        const code = document.getText();
        state.setCode(code);
    };
}

export function sendCodeChanges(payload) {
    return axios.post(HINTS_URL, payload)
        .then(
        ({ data }) => data,
        (err) => console.error(err)
        );
}

export function fetchToken(token) {
    return axios.post(
        AUTHORIZE_TOKEN_URL,
        `grant_type=authorization_code&code=${token}`
    );
}

export function fetchAuthorizationCode(username, password, clientId = 'testclient') {
    return axios.post(
        LOGIN_API_URL,
        `username=${username}&password=${password}&client_id=${clientId}&response_type=code&state=xyz`
    );
}

export function fetchExercises() {
    return new Promise((resolve) => {
        resolve([1, 2, 3].map(String));
    });
}