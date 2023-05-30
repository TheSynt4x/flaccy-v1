<script setup>
import Modal from '@/components/Modal.vue';
import { ref } from 'vue';

let isOpened = ref(false);
let isFormValid = ref(false);


function create() {
    // todo: implement create library
}
</script>

<template>
    <Modal v-model="isOpened">
        <template #activator="{ onClick }">
            <v-btn color="primary" @click="onClick">Create a library</v-btn>
        </template>

        <v-form v-model="isFormValid">
            <v-text-field :rules="[
                v => !!v || 'Name is required',
            ]" label="Name" density="compact" />
            <v-text-field :rules="[
                v => !!v || 'Path is required',
            ]" label="Path" density="compact" />

            <v-text-field :rules="[
                v => !!v || 'Output Path is required',
            ]" label="Output Path" density="compact" />

            <v-select :rules="[
                v => !!v || 'Formats is required',

            ]" label="Formats" density="compact" multiple chips
                :items="['.flac', '.mp3', '.m4a']"></v-select>
        </v-form>

        <template #actions>
            <v-btn variant="flat" color="primary" :disabled="!isFormValid">Create</v-btn>
        </template>
    </Modal>
</template>

