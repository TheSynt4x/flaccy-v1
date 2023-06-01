<script setup>
import TotalCard from '@/components/Total/index.vue';
import { useSongStore } from '@/store/songs';

import { ref, provide, onMounted } from 'vue';

const songStore = useSongStore();

let total = ref(0);
provide('total', total);

onMounted(async () => {
    total.value = await songStore.getSongsTotal();
});
</script>

<template>
    <total-card text="songs"></total-card>
</template>