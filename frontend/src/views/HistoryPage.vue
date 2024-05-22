<template>
  <TitleBar title="History" />

  <div class="container">
    <TimeSelector />
    <div
      class="records-container"
      v-for="(record, index) in records"
      :key="index"
    >
      <RecordView :record="record" />
    </div>
  </div>

  <BottomNavbar />
</template>

<script>
import TitleBar from "@/components/TitleBar.vue";
import BottomNavbar from "@/components/BottomNavbar.vue";
import TimeSelector from "@/components/TimeSelector.vue";
import RecordView from "@/components/RecordView.vue";

import axios from "axios";

export default {
  components: {
    TitleBar,
    BottomNavbar,
    TimeSelector,
    RecordView,
  },
  created() {
    this.getAllRecords();
  },
  data() {
    return {
      records: [
        //       {
        //         rid: "001",
        //         date: "2024-05-19",
        //         name: "cake",
        //         amount: 360,
        //         tags: ["Food", "Gift", "i don't know"],
        //         type: "expense",
        //       },
        //       {
        //         rid: "002",
        //         date: "2024-05-20",
        //         name: "dinner",
        //         amount: 100,
        //         tags: ["Food"],
        //         type: "expense",
        //       },
        //       {
        //         rid: "003",
        //         date: "2024-05-21",
        //         name: "t-shirt",
        //         amount: 399,
        //         tags: ["Clothing"],
        //         type: "income",
        //       },
      ],
    };
  },
  methods: {
    getAllRecords() {
      const path = "http://localhost:5000/api/get/all_records";
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
          this.records = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
