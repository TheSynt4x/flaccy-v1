<script setup lang="ts">
import { defineProps, defineEmits, ref, watchEffect, computed } from 'vue';

interface GenericItem {
    name: string;
}

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
    return props.items.filter(item => {
        return (item as GenericItem)?.name?.toLowerCase().includes(search.value.toLowerCase())
    });
});

watchEffect(() => {
    emit('update:search', search.value);
});
</script>

<template>
    <v-text-field v-model="search" label="Search for libraries" density="compact"></v-text-field>

    <v-data-table v-model:items-per-page="props.itemsPerPage" :headers="props.headers" :items="filteredItems"
        :loading="loading" item-value="name" class="elevation-1" density="compact">
    </v-data-table>
</template>
