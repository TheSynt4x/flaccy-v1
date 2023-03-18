<script setup lang="ts">
import Modal from '@/components/Modal.vue';
import {ref} from 'vue';

let isOpened = ref(false);
</script>

<template>
    <Modal v-model="isOpened">
        <template #activator="{ onClick }">
            <v-btn color="primary" @click="onClick">Create a library</v-btn>
        </template>

        <v-form>
            <v-text-field label="Name" density="compact"></v-text-field>
            <v-text-field label="Path" density="compact"></v-text-field>
            <v-text-field label="Output Path" density="compact"></v-text-field>
            <v-select label="Formats" density="compact" multiple chips
                :items="[{ title: 'FLAC', value: '.flac' }, { title: 'MP3', value: '.mp3' }, { title: 'M4A', value: '.m4a' }]"></v-select>
        </v-form>

        <template #actions>
            <v-btn variant="flat" color="primary">Create</v-btn>
        </template>
    </Modal>
</template>

