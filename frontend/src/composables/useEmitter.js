import { onBeforeUnmount, onMounted } from 'vue';

import { getCurrentInstance } from 'vue'

export default function useEmitter(event, listener) {
    const app = getCurrentInstance()

    const emitter = app.appContext.config.globalProperties.emitter;

    onMounted(() => {
        emitter.on(event, listener);
    })

    onBeforeUnmount(() => {
        emitter.off(event, listener);
    });
}
