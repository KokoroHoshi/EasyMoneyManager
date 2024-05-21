<template>
    <div class="search-bar">
      <label for="search-input" class="form-label">Search:</label>
      <div class="input-group">
        <input type="text" class="form-control" id="search-input" v-model="searchQuery" @input="onSearchInput">
        <button class="btn btn-primary" @click="search">Search</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'SearchBar',
    data() {
      return {
        searchQuery: ''
      };
    },
    methods: {
      search() {
        // Perform search action here
        console.log('Searching for:', this.searchQuery);
      },
      onSearchInput() {
        // Handle input event if needed
      }
    }
  };
  </script>
  
  <style scoped>
  .search-bar {
    margin-bottom: 1rem;
  }
  </style>
  