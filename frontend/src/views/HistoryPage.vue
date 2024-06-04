<template>
  <TitleBar title="History" />

  <div class="container">
    <TimeSelector @date-selected="getRecordsByDate" />
    <div
      class="records-container"
      v-for="(record, index) in records"
      :key="index"
    >
      <RecordView :record="record" @recordDeleted="removeRecord" />
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
import { useAuth } from "@/useAuth";

export default {
  beforeRouteUpdate() {
    this.getRecordsByDate();
  },
  setup() {
    const { userInfo } = useAuth();

    return {
      userInfo,
    };
  },
  components: {
    TitleBar,
    BottomNavbar,
    TimeSelector,
    RecordView,
  },
  data() {
    return {
      records: [],
    };
  },
  created() {
    this.getRecordsByDate();
  },
  methods: {
    getRecordsByDate(date) {
      if (!date) {
        const today = new Date();
        date = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(
          2,
          "0"
        )}-${String(today.getDate()).padStart(2, "0")}`;
      }
      const userId = this.userInfo.sub;
      axios
        .get(`http://localhost:5000/api/get/records/${userId}/${date}`)
        .then((res) => {
          this.records = res.data.records;
        })
        .catch((err) => {
          console.error("Error fetching records:", err);
        });
    },
    removeRecord(recordId) {
      this.records = this.records.filter(
        (record) => record.record_id !== recordId
      );
    },
  },
};
</script>

<style scoped>
.container {
  margin-top: 6%;
  margin-left: auto;
  box-shadow: 1px -1px 3px 0px rgb(166, 206, 206);
  background-color: rgb(182, 209, 209);
  font-size: 25px;
  font-weight: bolder;
}
.records-container {
  margin-bottom: 1rem;
}
</style>
