import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import router from './plugins/router'
import vuetify from './plugins/vuetify'
import mitt from 'mitt'
import { connection } from './client';

const emitter = mitt()

const pinia = createPinia()
const app = createApp(App);

app.use(router);
app.use(vuetify);
app.use(pinia);

app.config.globalProperties.emitter = emitter;

connection.subscribe('onmessage', (ev) => {
    emitter.emit('message', ev);
});

app.mount('#app');
