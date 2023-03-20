<script setup>
import { ref, watchEffect, computed } from 'vue';

const props = defineProps({
    headers: {
        type: Array,
        required: true,
    },
    items: {
        type: Array,
        required: true,
    },
    itemsPerPage: {
        type: Number,
        required: true,
    },
    search: {
        type: String,
        required: true,
    },
    loading: {
        type: Boolean,
        default: false,
    }
});

const emit = defineEmits(['update:search']);

let search = ref(props.search);

const filteredItems = computed(() => {
    if (search.value === '') return props.items;

    return props.items.filter(item => {
        return item?.name?.toLowerCase().includes(search.value.toLowerCase())
    });
});

watchEffect(() => {
    emit('update:search', search.value);
});
</script>

<template>
    <v-text-field v-model="search" label="Search..." density="compact"></v-text-field>

    <v-data-table v-model:items-per-page="props.itemsPerPage" :headers="props.headers" :items="filteredItems"
        :loading="loading" item-value="name" class="elevation-1" density="compact">
    </v-data-table>
</template>
