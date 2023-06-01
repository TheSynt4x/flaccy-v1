<script setup>
import TotalCard from '@/components/Total/index.vue';
import { useSongStore } from '@/store/songs';
import { provide, onMounted, ref, watch } from 'vue';

const songStore = useSongStore();

let total = ref(0);
provide('total', total);

onMounted(async () => {
    await songStore.getSongArtistsTotal();

    total.value = songStore.totalArtists;
});


</script>

<template>
    <total-card text="artists"></total-card>
</template>