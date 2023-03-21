<script setup>
import { ref, watch } from 'vue'

import { useSongStore } from '@/store/songs';

import debounce from 'lodash.debounce'


const songStore = useSongStore();

let headers = ref([
    { title: 'Artist', key: 'artist' },
    { title: 'Title', key: 'title' },
    { title: 'Album', key: 'album' },
    { title: 'Year', key: 'year' },
]);

let currentPage = ref(1);

let filters = [];

async function load(search, sortBy) {
    if (search && search.length > 0) {
        filters.push(['q', search]);
    }

    if (sortBy && sortBy.length > 0) {
        for (const sort of sortBy) {
            if (filters.find(f => f[0] === 'sort')) {
                filters = filters.filter(f => f[0] !== 'sort');
            }

            filters.push(['sort', `${sort.key}.${sort.order}`])
        }
    }

    console.log(filters);

    // &sortBy=artist.asc&sortBy=title.asc

    await songStore.fetchSongs(currentPage.value, filters);
}

async function loadItems(p) {
    currentPage.value = p.page;

    await load(search.value, p.sortBy);
}

let itemsPerPage = ref(10);

let search = ref('');

let isLoading = ref(false);

watch(search, () => {
    if (isLoading.value) return;

    isLoading.value = true;

    debounce(async () => {
        currentPage.value = 1;

        await load(search.value);

        isLoading.value = false;
    }, 2000)();
})
</script>

<template>
    <div>
        <h1>Songs</h1>

        <v-text-field v-model="search" label="Search..." density="compact" class="ma-0">
            <template #append>
                <v-btn icon variant="plain" @click="hasFilters = true">
                    <v-icon icon="mdi-filter"></v-icon>
                </v-btn>
            </template>
        </v-text-field>

        <div style="display: flex; align-items: center; gap: 1rem;">
            <slot name="filters"></slot>
        </div>

        <v-data-table-server v-model:items-per-page="itemsPerPage" :headers="headers" :items-length="songStore.total"
            :items="songStore.songsPerPage" :loading="isLoading" class="elevation-1" item-title="name" item-value="name"
            @update:options="loadItems"></v-data-table-server>
    </div>
</template>