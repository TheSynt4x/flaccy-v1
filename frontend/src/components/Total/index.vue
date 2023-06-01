<script setup>
import { inject } from 'vue';

defineProps(['text']);

const total = inject('total');
</script>

<template>
    <v-col cols="12" xs="12" sm="12" md="4" lg="4" xl="4">
        <v-card class="elevation-2 mb-5">
            <v-card-title>
                <h2 class="text-h6">Total {{ text }}</h2>
            </v-card-title>
            <v-card-text>
                <h1 class="text-h3">{{ total }}</h1>
            </v-card-text>
        </v-card>
    </v-col>
</template>