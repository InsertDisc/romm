import { defineStore } from 'pinia';

export const useOpenIDStore = defineStore('openid', {
  state: () => ({
    clientId: '',
    clientSecret: '',
    redirectUri: '',
    authorizationEndpoint: '',
    tokenEndpoint: '',
    userinfoEndpoint: '',
  }),
  actions: {
    setConfig(config: {
      clientId: string;
      clientSecret: string;
      redirectUri: string;
      authorizationEndpoint: string;
      tokenEndpoint: string;
      userinfoEndpoint: string;
    }) {
      this.clientId = config.clientId;
      this.clientSecret = config.clientSecret;
      this.redirectUri = config.redirectUri;
      this.authorizationEndpoint = config.authorizationEndpoint;
      this.tokenEndpoint = config.tokenEndpoint;
      this.userinfoEndpoint = config.userinfoEndpoint;
    }
  },
});
