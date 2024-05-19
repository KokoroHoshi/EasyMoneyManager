<template>
  <TitleBar title="Record" />

  <div class="container"></div>

  <BottomNavbar />
</template>

<script>
import TitleBar from "@/components/TitleBar.vue";
import BottomNavbar from "@/components/BottomNavbar.vue";

export default {
  components: {
    TitleBar,
    BottomNavbar,
  },
};
</script>
