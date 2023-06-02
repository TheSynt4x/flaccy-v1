import { defineStore } from "pinia";

export const useArtistStore = defineStore("artists", {
    state: () => {
        return {
            isLoading: false,
            artists: {},
            totalArtists: 0,
        };
    },

    getters: {
        artistByName: (state) => (name) => {
            return Object.values(state.artists).find(
                (artist) => artist.name === name
            );
        }
    },

    actions: {
        async getArtistByName(name) {
            try {
                this.isLoading = true;

                const response = await fetch(
                    `http://localhost:8000/api/artists/${name}`
                );

                const artist = await response.json();
                
                this.artists = { [artist.id]: artist };
            }
            finally {
                this.isLoading = false;
            }
        },

    },
});