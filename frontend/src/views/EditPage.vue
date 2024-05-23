<template>
  <TitleBar title="Record" />

  <div class="container">
    <RecordCard :record="record" />
  </div>

  <BottomNavbar />
</template>

<script>
import TitleBar from "@/components/TitleBar.vue";
import BottomNavbar from "@/components/BottomNavbar.vue";
import RecordCard from "@/components/RecordCard.vue";

import axios from "axios";

export default {
  components: {
    TitleBar,
    BottomNavbar,
    RecordCard,
  },
  created() {
    this.getRecord();
  },
  data() {
    return {
      record: {
        rid: "",
        name: "",
        amount: 0,
        tags: [],
        type: "",
        date: "",
      },
    };
  },
  methods: {
    getRecord() {
      const recordId = this.$route.query.rid;
      if (!recordId) {
        console.error("Record ID is missing");
        return;
      }
      console.log(recordId);
      const path = `http://localhost:5000/api/get/record?rid=${recordId}`;
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
          this.record = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
