<template>
  <TitleBar title="History" />

  <div class="container">
    <TimeSelector />
  </div>

  <BottomNavbar />
</template>

<script>
import TitleBar from "@/components/TitleBar.vue";
import BottomNavbar from "@/components/BottomNavbar.vue";
import TimeSelector from "@/components/TimeSelector.vue";

import axios from "axios";

export default {
  components: {
    TitleBar,
    BottomNavbar,
    TimeSelector,
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