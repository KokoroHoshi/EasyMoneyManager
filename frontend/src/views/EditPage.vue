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
import { useAuth } from "@/useAuth";

export default {
  setup() {
    const { userInfo } = useAuth();
    return {
      userInfo,
    };
  },
  components: {
    TitleBar,
    BottomNavbar,
    RecordCard,
  },
  data() {
    return {
      record: {
        record_id: "",
        name: "",
        amount: 0,
        tags: [],
        type: "",
        date: "",
      },
    };
  },
  created() {
    this.getRecord();
  },
  methods: {
    getRecord() {
      const recordId = this.$route.query.record_id;
      if (!recordId) {
        console.error("Record ID is missing");
        return;
      }
      const path = `http://localhost:5000/api/get/record?user_id=${this.userInfo.sub}&record_id=${recordId}`;
      axios
        .get(path)
        .then((res) => {
          if (res.data.status === "success") {
            const record = res.data.record;
            record.tags = record.tags ? record.tags.split(",") : [];
            this.record = record;
            this.record.record_id = recordId;
          } else {
            console.error("Record not found");
          }
        })
        .catch((err) => {
          console.error("Error fetching record:", err);
        });
    },
  },
};
</script>

<style scoped>
.container {
  margin: 1rem;
}
</style>
