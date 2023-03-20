<script setup>
import Table from '@/components/Table.vue';

import { ref, onMounted } from 'vue'
import CreateLibraryModal from '@/components/CreateLibraryModal.vue';

let headers = ref([{
    title: 'Name',
    key: 'name',
}, {
    title: 'Path',
    key: 'path',
}, {
    title: 'Output Path',
    key: 'output_path',
}, {
    title: 'Formats',
    key: 'formats',
}]);

let libraries = ref([]);
let itemsPerPage = ref(5);

let search = ref('');

let isLibraryLoading = ref(false);

async function getLibraries() {
    try {
        isLibraryLoading.value = true;

        const response = await fetch('http://localhost:8000/api/libraries');

        if (!response.ok) {
            throw new Error(response.statusText);
        }

        const data = await response.json();

        libraries.value = data.libraries;
    } finally {
        isLibraryLoading.value = false;
    }
}

onMounted(async () => {
    await getLibraries();
});
</script>

<template>
    <div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h1>Libraries</h1>

            <CreateLibraryModal />
        </div>

        <Table v-model:search="search" :items-per-page="itemsPerPage" :headers="headers" :items="libraries" :loading="isLibraryLoading"></Table>
    </div>
</template>