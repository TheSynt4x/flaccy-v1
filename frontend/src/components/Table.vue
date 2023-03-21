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
    },
    hasFilters: {
        type: Boolean,
        default: false,
    }
});

const emit = defineEmits(['update:search']);

let search = ref(props.search);
let itemsPerPage = ref(props.itemsPerPage);
let hasFilters = ref(false);

const filteredItems = computed(() => {
    if (search.value === '') return props.items;

    return props.items.filter(item => {
        return Object.keys(item).some(key => {
            return String(item[key]).toLowerCase().includes(search.value.toLowerCase());
        });
    });
});

watchEffect(() => {
    emit('update:search', search.value);
});
</script>

<template>
    <v-text-field v-model="search" label="Search..." density="compact" class="ma-0">
        <template #append>
            <v-btn icon variant="plain" @click="hasFilters = true">
                <v-icon icon="mdi-filter"></v-icon>
            </v-btn>
        </template>
    </v-text-field>
    
    <div v-if="hasFilters" style="display: flex; align-items: center; gap: 1rem;">
        <slot name="filters"></slot>
    </div>

    <v-data-table v-model:items-per-page="itemsPerPage" :headers="props.headers" :items="filteredItems" :loading="loading"
        item-value="name" class="elevation-1 mt-2" density="compact">
    </v-data-table>
</template>
