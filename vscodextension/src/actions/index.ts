import axios from 'axios';
import {
    LOGIN_API_URL,
    AUTHORIZE_TOKEN_URL,
    HINTS_URL,
    EXERCISES_URL
} from '../constants';
import ApplicationState from '../ApplicationState';

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

export function showExerciseSelect(vscode, exercises = []) {
    return vscode.window.showQuickPick(
        exercises.map(({ id, name }) => {
            return { label: id, description: name };
        }),
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

function handleError(err) {
    console.log(err);
}

export function fetchHints(payload) {
    const { headers, data } = payload;
    return axios.post(HINTS_URL, data, { headers })
        .then(
            ({ data }) => {
                return data;
            },
            handleError
        );
}

export function fetchToken(token) {
    return axios.post(
        AUTHORIZE_TOKEN_URL,
        `grant_type=authorization_code&code=${token}`
    ).then(
        ({data}) => {
            return data;
        },
        handleError
    );
}

export function fetchAuthorizationCode(username, password, clientId = 'testclient') {
    return axios.post(
        LOGIN_API_URL,
        `username=${username}&password=${password}&client_id=${clientId}&response_type=code&state=xyz`
    ).then(
        ({data}) => {
            return data;
        },
        handleError
    );
}

export function fetchExercises(access_token) {
    const config = {
        headers: {
            access_token
        }
    };
    return axios.get(EXERCISES_URL, config)
        .then(
            ({ data }) => {
                return data;
            },
            handleError
        );
}