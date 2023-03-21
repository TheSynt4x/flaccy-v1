import { defineStore } from "pinia";

export const useSongStore = defineStore("songs", {
  state: () => {
    return {
      isLoading: false,
      songs: {},
      totalSongs: 0,
    };
  },
  getters: {
    songsPerPage: (state) => {
      return Object.values(state.songs);
    },

    total: (state) => state.totalSongs || 0,
  },
  actions: {
    async fetchSongs(page = 1, filters = []) {
      try {
        this.isLoading = true;
        const response = await fetch(
          `http://localhost:8000/api/songs?${new URLSearchParams([
            ["page", page],
            ...filters,
          ]).toString()}`
        );
        const { songs, total_count } = await response.json();

        this.songs = { ...songs };
        this.totalSongs = total_count;
      } finally {
        this.isLoading = false;
      }
    },
  },
});
