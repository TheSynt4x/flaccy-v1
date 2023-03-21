<script setup>
import { ref, watchEffect } from 'vue';

const props = defineProps({
    modelValue: {
        type: Boolean,
        required: true,
    },
});

const emit = defineEmits(['update:modelValue']);

let isOpened = ref(props.modelValue);

function open() {
    isOpened.value = true;
    emit('update:modelValue', isOpened.value);
}

function close() {
    isOpened.value = false;
    emit('update:modelValue', isOpened.value);
}

watchEffect(() => {
    emit('update:modelValue', isOpened.value);
});
</script>

<template>
    <v-dialog v-model="isOpened" width="500" persistent>
        <template v-slot:activator="{ props }">
            <slot name="activator" v-on="props" :onClick="open"></slot>
        </template>

        <v-card>
            <v-card-text>
                <slot></slot>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="close">Close</v-btn>

                <slot name="actions"></slot>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>