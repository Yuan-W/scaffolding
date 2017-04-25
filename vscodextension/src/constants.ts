const production = true;

const DOMAIN = production ? 'scaffolding.ml' : '127.0.0.1:5000';
const HTTP_PREFIX = production ? 'https://' : 'http://';

const BASE_URL = HTTP_PREFIX + DOMAIN;
const PUBLIC_API = 'http://' + DOMAIN + ':5000/api';

export const clientId = 'VSCode';
const client_password = 'password';


export const LOGIN_URL = BASE_URL + '/login';
export const LOGIN_API_URL = BASE_URL + '/api/login';
export const HINTS_URL = PUBLIC_API + '/hints';
export const EXERCISES_URL = PUBLIC_API + '/exercises';

export const AUTHORIZE_TOKEN_URL = HTTP_PREFIX + clientId + ':' + client_password + '@' + DOMAIN + '/token';
