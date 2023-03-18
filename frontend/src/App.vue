<script setup lang="ts">
import type { ComputedRef, Ref } from 'vue';
import type { Route } from '@/plugins/router';

import { ref, computed } from 'vue';

import { routes } from '@/plugins/router';

let drawer: Ref = ref(true);

let filteredRoutes: ComputedRef<Array<Route>> = computed(() => {
  return routes.filter(route => route.meta?.inNavbar);
})
</script>

<template>
  <v-app id="inspire">
    <v-app-bar color="blue">
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

      <v-toolbar-title>Application</v-toolbar-title>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer">
      <v-list>
        <v-list-item v-for="route in filteredRoutes" :to="route.path" :title="route.meta.title"
          :prepend-icon="route.meta.icon"></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <div class="pa-4">
        <router-view></router-view>
      </div>
    </v-main>
  </v-app>
</template>

<style>
.v-input--horizontal .v-input__append {
  margin-inline-start: 0 !important;
}

.v-input__prepend, .v-input__append {
  padding-top: 0 !important;
}
</style>