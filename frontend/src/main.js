import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import router from './plugins/router'
import vuetify from './plugins/vuetify'

const pinia = createPinia()
const app = createApp(App);

app.use(router);
app.use(vuetify);
app.use(pinia);

app.mount('#app');
