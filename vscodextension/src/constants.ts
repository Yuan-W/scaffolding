const production = false;

const DOMAIN = production ? 'ubuntu.jedge.uk' : '127.0.0.1:5000';
const HTTP_PREFIX = production ? 'https://' : 'http://';

const BASE_URL = HTTP_PREFIX + DOMAIN;

export const clientId = 'testclient';
const client_password = 'testpass';


export const LOGIN_URL = BASE_URL + '/login';
export const LOGIN_API_URL = BASE_URL + '/api/login';
export const HINTS_URL = BASE_URL + '/hints';

export const AUTHORIZE_TOKEN_URL = HTTP_PREFIX + clientId + ':' + client_password + '@' + DOMAIN + '/token';