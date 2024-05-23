<template>
  <TitleBar title="Investment" />

  <div class="container">
    <StockView />
  </div>

  <BottomNavbar />
</template>

<script>
import TitleBar from "@/components/TitleBar.vue";
import BottomNavbar from "@/components/BottomNavbar.vue";
import StockView from "@/components/StockView.vue";

export default {
  components: {
    TitleBar,
    BottomNavbar,
    StockView,
  },
  created() {},
  data() {
    return {};
  },
  methods: {},
};
</script>
