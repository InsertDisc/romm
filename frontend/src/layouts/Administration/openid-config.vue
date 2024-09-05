<script setup lang="ts">
import { ref } from "vue";
import { useOpenIDStore } from "@/stores/openid";

const openidStore = useOpenIDStore();

const clientId = ref(openidStore.clientId);
const clientSecret = ref(openidStore.clientSecret);
const redirectUri = ref(openidStore.redirectUri);
const authorizationEndpoint = ref(openidStore.authorizationEndpoint);
const tokenEndpoint = ref(openidStore.tokenEndpoint);

function saveConfig() {
  openidStore.updateConfig({
    clientId: clientId.value,
    clientSecret: clientSecret.value,
    redirectUri: redirectUri.value,
    authorizationEndpoint: authorizationEndpoint.value,
    tokenEndpoint: tokenEndpoint.value,
  });
}
</script>

<template>
  <v-form @submit.prevent="saveConfig">
    <v-text-field
      v-model="clientId"
      label="Client ID"
      variant="underlined"
    />
    <v-text-field
      v-model="clientSecret"
      label="Client Secret"
      variant="underlined"
    />
    <v-text-field
      v-model="redirectUri"
      label="Redirect URI"
      variant="underlined"
    />
    <v-text-field
      v-model="authorizationEndpoint"
      label="Authorization Endpoint"
      variant="underlined"
    />
    <v-text-field
      v-model="tokenEndpoint"
      label="Token Endpoint"
      variant="underlined"
    />
    <v-btn
      type="submit"
      class="bg-primary"
    >
      Save Configuration
    </v-btn>
  </v-form>
</template>

<style scoped>
/* Add your component styles here */
</style>
