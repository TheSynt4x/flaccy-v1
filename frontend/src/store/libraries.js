import { defineStore } from "pinia";

export const useLibraryStore = defineStore("libraries", {
  state: () => {
    return {
      isLoading: false,
      libraries: {},
    };
  },
  getters: {
    allLibraries: (state) => {
      return Object.values(state.libraries);
    },
  },
  actions: {
    async fetchLibraries(page = 1, filters = {}) {
      const params = new URLSearchParams({ page, ...filters });

      this.isLoading = true;
      try {
        const response = await fetch(
          `http://localhost:8000/api/libraries?${params.toString()}`
        );
        const { libraries } = await response.json();
        for (const library of libraries) {
          this.libraries[library.id] = library;
        }
      } finally {
        this.isLoading = false;
      }
    },
  },
});
