import axios from 'axios';
import {
    LOGIN_API_URL,
    AUTHORIZE_TOKEN_URL,
    HINTS_URL
} from './constants';

function debounce(fn, delay) {
    var timer = null;
    return function () {
        var context = this, args = arguments;
        clearTimeout(timer);
        timer = setTimeout(function () {
            fn.apply(context, args);
        }, delay);
    };
}

export function documentTextChangeHandler(state) {
    return debounce(
        function (e) {
            const { document } = e;
            const code = document.getText();
            state.setCode(code);
        },
        500
    );
}

export function sendCodeChanges(payload) {
    return axios.post(HINTS_URL, payload)
        .then(() => { })
        .catch((err) => console.error(err));
}

export function fetchToken(token) {
    return axios.post(
        AUTHORIZE_TOKEN_URL,
        `grant_type=authorization_code&code=${token}`
    );
}

export function fetchAuthorizationCode(username, password) {
    return axios.post(
        LOGIN_API_URL,
        `username=${username}&password=${password}&client_id=testclient&response_type=code&state=xyz`
    );
}