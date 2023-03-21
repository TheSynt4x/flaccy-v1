<script setup>
import Table from '@/components/Table.vue';

import { ref, onMounted, computed } from 'vue'
import CreateLibraryModal from '@/components/CreateLibraryModal.vue';

import { useLibraryStore } from '@/store/libraries';

const libraryStore = useLibraryStore();

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

let itemsPerPage = ref(5);

let search = ref('');

let formatFilter = ref([]);

const filteredLibraries = computed(() => {
    if (!formatFilter.value.length) return libraryStore.allLibraries;

    return libraryStore.allLibraries.filter(library => {
        return formatFilter.value.every(format => library.formats.includes(format));
    });
});

onMounted(async () => {
    await libraryStore.fetchLibraries();
});
</script>

<template>
    <div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h1>Libraries</h1>

            <CreateLibraryModal />
        </div>

        <Table v-model:search="search" :items-per-page="itemsPerPage" :headers="headers" :items="filteredLibraries"
            :hasFilters="true">
            <template #filters>
                <div style="flex-grow: 1;">
                    <v-select v-model="formatFilter" label="Formats" :items="['.mp3', '.flac', '.m4a']" multiple chips />
                </div>
            </template>
        </Table>

    </div>
</template>