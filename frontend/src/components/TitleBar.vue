<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <h1>{{ title }}</h1>
  </nav>
</template>

<script>
export default {
  props: {
    title: String,
  },
};
</script>
