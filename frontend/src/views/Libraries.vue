<script setup>
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
        return formatFilter.value.some(format => {
            return library.formats.toLowerCase().includes(format);
        });
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


        <div class="d-flex gap-2">
            <v-text-field v-model="search" label="Search" class="flex-grow-1 basis-half"></v-text-field>
            <v-autocomplete v-model="formatFilter" chips multiple label="Formats" :items="[
                {
                    title: 'MP3',
                    value: '.mp3',
                },
                {
                    title: 'FLAC',
                    value: '.flac',
                },
                {
                    title: 'M4A',
                    value: '.m4a',
                }
            ]" class="flex-grow-1 basis-half"></v-autocomplete>
        </div>

        <v-data-table v-model:search="search" :items-per-page="itemsPerPage" :headers="headers"
            :items="filteredLibraries" class="elevation-1" />
    </div>
</template>