import React from 'react';
import {createRoot} from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { ReactKeycloakProvider } from '@react-keycloak/web';
import keycloakConfig from './keycloak-config';

const root = createRoot(document.getElementById('root'));
root.render(
  <ReactKeycloakProvider authClient={keycloakConfig} 
          initOptions={{onLoad: 'login-required', checkLoginIframe: false, pkceMethod: 'S256' }}
          onEvent={(event, error) => {
              console.log('Keycloak event:', event, error);
            }}
          onTokens={(tokens) => {
            console.log('INDExhjis: ', tokens)
          }}    
      >
      <App />
  </ReactKeycloakProvider>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
