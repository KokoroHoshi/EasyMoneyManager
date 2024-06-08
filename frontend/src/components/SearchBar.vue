<template>
  <div class="search-bar">
    <h5 for="search-input" class="form-label">Search stock price by code:</h5>
    <div class="input-group">
      <input
        type="text"
        class="form-control"
        id="search-input"
        v-model="searchQuery"
        @input="onSearchInput"
      />
      <button class="btn btn-primary" @click="search">Search</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchBar",
  data() {
    return {
      searchQuery: "",
    };
  },
  methods: {
    search() {
      this.$emit("search", this.searchQuery);
    },
    onSearchInput() {
      // Handle input event if needed
    },
  },
};
</script>

<style scoped>
.search-bar {
  margin-bottom: 1rem;
  font-weight: bolder;
  font-size: 26px;
}
</style>
