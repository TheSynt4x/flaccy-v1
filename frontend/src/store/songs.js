import { defineStore } from "pinia";

export const useSongStore = defineStore("songs", {
  state: () => {
    return {
      isLoading: false,
      songs: {},
      totalSongs: 0,
      artistsTotal: 0,
      albumsTotal: 0,
    };
  },
  getters: {
    songsPerPage: (state) => {
      return Object.values(state.songs);
    },

    total: (state) => state.totalSongs || 0,

    totalArtists: (state) => state.artistsTotal || 0,

    totalAlbums: (state) => state.albumsTotal || 0,
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

    async getSongsTotal() {
      try {
        this.isLoading = true;

        const response = await fetch(
          `http://localhost:8000/api/songs/total`
        );

        const { total } = await response.json();

        return total;
      } finally {
        this.isLoading = false;
      }
    },

    async getSongArtistsTotal() {
      try {
        this.isLoading = true;

        const response = await fetch(
          `http://localhost:8000/api/songs/artists/total`
        );

        const { total } = await response.json();

        this.artistsTotal = total;

      } finally {
        this.isLoading = false;
      }
    },

    async getSongAlbumsTotal() {
      try {
        this.isLoading = true;

        const response = await fetch(
          `http://localhost:8000/api/songs/albums/total`
        );

        const { total } = await response.json();

        this.albumsTotal = total;
      } finally {
        this.isLoading = false;
      }
    }
  },
});
