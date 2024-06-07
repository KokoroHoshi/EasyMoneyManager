<template>
  <TitleBar title="Investment" />

  <div class="container">
    <StockView />
  </div>

  <div class="block"></div>

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

<style scoped>
.block {
  margin-top: 100px;
}

.container {
  padding-top: 1%;
  padding-bottom: 1%;
  margin-left: auto;
  font-size: 25px;
  font-weight: bolder;
}
</style>
