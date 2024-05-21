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

import axios from "axios";

export default {
  components: {
    TitleBar,
    BottomNavbar,
    SearchBar,
    StockView,
  },
  created() {
    // this.getResponse();
  },
  data() {
    return {
      // test: "",
    };
  },
  methods: {
    getResponse() {
      const path = "http://localhost:5000/record";
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
          this.test = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
