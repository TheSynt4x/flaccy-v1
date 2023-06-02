<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useSongStore } from '@/store/songs';

import debounce from 'lodash.debounce';
import { useRouter } from 'vue-router';

import { connection } from '@/client';

import useEmitter from '@/composables/useEmitter';
import TotalArtists from '@/components/Total/TotalArtists.vue';
import TotalSongs from '@/components/Total/TotalSongs.vue';
import TotalAlbums from '@/components/Total/TotalAlbums.vue';

const songStore = useSongStore();
const router = useRouter();

let headers = ref([
    { title: 'Artist', key: 'artist' },
    { title: 'Title', key: 'title' },
    { title: 'Album', key: 'album' },
    { title: 'Year', key: 'year' },
]);

let currentPage = ref(1);

let itemsPerPage = ref(10);

let search = ref('');

let isLoading = ref(false);
let isSyncLoading = ref(false);

let sorts = ref([]);

function sync() {
    isSyncLoading.value = true;

    connection.send(JSON.stringify({
        command: 'sync',
        params: [],
    }));
}

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

useEmitter('message', async (event) => {
    const data = JSON.parse(event.data);

    if (data.status === 'start_refreshing_songs') {
        await parseUrlFilters();

        await loadItems({
            search: search.value,
            page: currentPage.value,
            itemsPerPage: itemsPerPage.value,
            sortBy: sorts.value,
        });

    } else if (data.status === 'success') {
        await loadItems({
            search: search.value,
            page: currentPage.value,
            itemsPerPage: itemsPerPage.value,
            sortBy: sorts.value,
        });

        isSyncLoading.value = false;
    }
});
</script>

<template>
    <h1>Songs</h1>

    <v-row>
        <total-songs></total-songs>
        <total-albums></total-albums>
        <total-artists></total-artists>
    </v-row>

    <v-text-field v-model="search" label="Search..." density="compact" class="ma-0" />

    <v-data-table-server v-model:items-per-page="itemsPerPage" v-model:search="search" :headers="headers"
        :items-length="songStore.total" :items="songStore.songsPerPage" :loading="isLoading" class="elevation-1"
        item-title="name" item-value="name" @update:options="debouncedLoadItems">
        <template #item="{item}">
            <tr>
                <td><router-link :to="`/artists/${item.columns.artist}`">{{item.columns.artist}}</router-link></td>
                <td><router-link :to="`/artists/${item.columns.artist}/albums/${item.columns.album}/${item.columns.title}`">{{item.columns.title}}</router-link></td>
                <td><router-link :to="`/artists/${item.columns.artist}/albums/${item.columns.album}`">{{ item.columns.album }}</router-link></td>
                <td>{{ item.columns.year }}</td>
            </tr>
        </template>
    </v-data-table-server>

    <v-tooltip position="top" text="Run song sync">
        <template #activator="{ props }">
            <v-btn :loading="isSyncLoading" :disabled="isSyncLoading" @click="sync" color="primary" v-bind="props"
                style="position: absolute; bottom: 1rem; right: 1rem;" icon="mdi-refresh"></v-btn>
        </template>
    </v-tooltip>
</template>