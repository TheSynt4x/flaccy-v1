<script setup>
import { ref, onMounted } from 'vue'
import { useSongStore } from '@/store/songs';

import debounce from 'lodash.debounce';
import { useRouter } from 'vue-router';

const songStore = useSongStore();
const router = useRouter();

let headers = ref([
    { title: 'Artist', key: 'artist' },
    { title: 'Title', key: 'title' },
    { title: 'Album', key: 'album' },
    { title: 'Year', key: 'year' },
]);

let currentPage = ref(1);

let allFilters = [];

let itemsPerPage = ref(10);

let search = ref('');

let isLoading = ref(false);

let sorts = ref([]);

async function parseUrlFilters() {
    const { page, q, per_page } = router.currentRoute.value.query;

    if (page) {
        currentPage.value = page;
    }

    if (q) {
        search.value = q;
    }

    if (per_page) {
        itemsPerPage.value = per_page;
    }
}

async function loadItems(context) {
    if (isLoading.value) return;

    let filters = [];
    const obj = {}

    try {
        isLoading.value = true;

        search.value = context.search || '';
        currentPage.value = context.page || 1; ``
        itemsPerPage.value = context.itemsPerPage || itemsPerPage.value;
        sorts.value = context.sortBy;


        if (currentPage.value) {
            obj.page = currentPage.value;
        }

        if (search.value) {
            obj.q = search.value;
            filters.push(["q", search.value]);
        }

        if (itemsPerPage.value) {
            obj.per_page = itemsPerPage.value;
            filters.push(["per_page", itemsPerPage.value]);
        }

        if (sorts.value) {
            for (const sort of sorts.value) {
                if (sort.key && sort.order) {
                    filters.push(['sorts', `${sort.key}.${sort.order}`])
                }
            }
        }

        await songStore.fetchSongs(currentPage.value, filters);
    } finally {
        router.push({
            query: obj,
        });

        isLoading.value = false;
    }
}

let debouncedLoadItems = debounce(loadItems, 300);

onMounted(async () => {
    await parseUrlFilters();
});
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

        <v-data-table-server v-model:items-per-page="itemsPerPage" v-model:search="search" :headers="headers"
            :items-length="songStore.total" :items="songStore.songsPerPage" :loading="isLoading" class="elevation-1"
            item-title="name" item-value="name" @update:options="debouncedLoadItems"></v-data-table-server>
    </div>
</template>