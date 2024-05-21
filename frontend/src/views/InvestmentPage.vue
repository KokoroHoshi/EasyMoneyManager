<template>
  <TitleBar title="Investment" />

  <div class="container">
    <SearchBar />
    <StockView />
  </div>

  <BottomNavbar />
</template>

<script>
import TitleBar from "@/components/TitleBar.vue";
import BottomNavbar from "@/components/BottomNavbar.vue";
import SearchBar from "@/components/SearchBar.vue";
import StockView from "@/components/StockView.vue";

export default {
  components: {
    TitleBar,
    BottomNavbar,
    SearchBar,
    StockView,
  },
  created() {},
  data() {
    return {};
  },
  methods: {},
};
</script>
