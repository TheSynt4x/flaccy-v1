import { defineStore } from "pinia";

export const useSongStore = defineStore("songs", {
  state: () => {
    return {
      isLoading: false,
      songs: {},
    };
  },
  getters: {
    allSongs: (state) => {
      return Object.values(state.songs);
    },
  },
  actions: {
    async fetchSongs() {
      try {
        this.isLoading = true;
        const response = await fetch("http://localhost:8000/api/songs");
        const { songs } = await response.json();
        for (const song of songs) {
          this.songs[song.id] = song;
        }
      } finally {
        this.isLoading = false;
      }
    },
  },
});
