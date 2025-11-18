import axios from 'axios';
import keycloakConfig from './keycloak-config';

export function getCookie(name) {
    const value='; ${document.cookie}';
    console.log(value);
    const parts=value.split('; ${name}=');
    if (parts.length === 2) return parts.pop().split(';').shift();
};

export const Api = axios.create({
    baseURL: process.env.REACT_APP_API,
    headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-type, Accept',
        //'Authorization': 'Bearer ${token}'
    }
});

Api.interceptors.request.use(
    (config) => {
        console.log(config)
        const csrfToken = getCookie('csrftoken');
        config.headers['X-CSRFToken'] = csrfToken;

        console.log('Keycloak', keycloakConfig.token);

        if (keycloakConfig && keycloakConfig.token) {
            config.headers['Authorization'] = `Bearer ${keycloakConfig.token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
)