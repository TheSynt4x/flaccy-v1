<script setup lang="ts">
import Table from '@/components/Table.vue';
import { ref, onMounted } from 'vue'

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
}] as Array<{ title: string, key: string }>);

let libraries = ref([] as Array<{ name: string, path: string, output_path: string, formats: string }>);
let itemsPerPage = 5;

let search = ref('');

onMounted(() => {
    fetch('https://localhost:8080/api/libraries')
        .then(response => response.json())
        .then(data => {
            libraries.value = data;
        });
});
</script>

<template>
    <div>
        <h1>Libraries</h1>

        <Table v-model:search="search" :items-per-page="itemsPerPage" :headers="headers" :items="libraries"></Table>
    </div>
</template>