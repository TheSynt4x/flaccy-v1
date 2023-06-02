<script setup>
import { useArtistStore } from '@/store/artists';
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router';
let search = ref('');

const route = useRoute();
const artistStore = useArtistStore();

onMounted(async () => {
    await artistStore.getArtistByName(route.params.name);
});

const artist = computed(() => {
    return artistStore.artistByName(route.params.name);
})

const getArtistCover = computed(() => {
    return artist.value?.images?.find((image) => {
        return image.type === 'primary';
    })?.uri;
})

const computedAlbums = computed(() => {
    return albums.value.filter((album) => {
        return album.title.toLowerCase().includes(search.value.toLowerCase());
    });
});
</script>

<template>
    <v-row class="mb-5" v-if="!artistStore.isLoading">
        <v-col cols="12" xs="12" sm="12" md="4" lg="4" xl="4">
            <v-img :cover="true" :src="getArtistCover"></v-img>
        </v-col>

        <v-col cols="12" xs="12" sm="12" m="8" lg="8" xl="8">
            <h1>Bayside</h1>
            <div class="d-flex flex-column gap-1">
                <span class="mt-5">
                    {{ artist?.profile }}
                </span>
                <div class="mt-5">
                    <v-chip class="mr-1" :href="url" v-for="url, index in artist?.urls" :key="index">{{ url }}</v-chip>
                </div>
            </div>
        </v-col>
    </v-row>

    <v-progress-circular class="mb-5" v-else indeterminate></v-progress-circular>

    <v-text-field v-model="search" class="ml-1 mr-1" density="compact" label="Search for albums"
        placeholder="Enter album name..."></v-text-field>

    <v-row>
        <v-col v-for="i in 4" :key="i" cols="12" xs="12" sm="12" md="3" lg="3" xl="3">
            <v-card>
                <v-img cover
                    src="https://i.discogs.com/ICMLOuu5fg99INp9tVXLUkQIhY40pMrrORhZrZddx3s/rs:fit/g:sm/q:90/h:599/w:600/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9SLTI5ODMy/MTktMTY0NjYwMjA2/Mi0yNzM1LmpwZWc.jpeg"></v-img>

                <v-card-title>
                    <h3>lol</h3>
                </v-card-title>

                <v-card-text>
                    <p><strong>Released:</strong> 2005</p>
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" variant="elevated" :to="`/artists/a/albums/lol`">View</v-btn>
                </v-card-actions>
            </v-card>
        </v-col>
    </v-row>
</template>
