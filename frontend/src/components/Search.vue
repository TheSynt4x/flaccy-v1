<script setup>
import { watchEffect, ref, computed } from 'vue';

const props = defineProps({
    modelValue: {
        type: String,
        required: true,
    },

    filters: {
        type: Array,
    }
});

const emit = defineEmits(['update:modelValue']);

let search = ref(props.modelValue);

let filters = computed(() => {
    return props.filters;
});

watchEffect(() => {
    emit('update:modelValue', search.value);
});

</script>

<template>
    <v-text-field v-model="search" label="Search..." density="compact">
        <template #append v-if="filters?.length">
            
        </template>
    </v-text-field>
</template>
