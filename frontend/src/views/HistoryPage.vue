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

  <div class="block"></div>

  <BottomNavbar />
</template>

<script>
import TitleBar from "@/components/TitleBar.vue";
import BottomNavbar from "@/components/BottomNavbar.vue";
import TimeSelector from "@/components/TimeSelector.vue";
import RecordView from "@/components/RecordView.vue";
import axios from "axios";
import { useAuth } from "@/useAuth";
import { ref, onMounted } from "vue";

export default {
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      vm.getRecordsByDate();
    });
  },
  setup() {
    const { userInfo } = useAuth();
    const records = ref([]);

    const getRecordsByDate = (date) => {
      if (!date) {
        const today = new Date();
        date = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(
          2,
          "0"
        )}-${String(today.getDate()).padStart(2, "0")}`;
      }
      const userId = userInfo.value?.sub;
      if (!userId) {
        console.error("User info not available.");
        return;
      }

      axios
        .get(`http://localhost:5000/api/get/records/${userId}/${date}`)
        .then((res) => {
          records.value = res.data.records;
        })
        .catch((err) => {
          console.error("Error fetching records:", err);
        });
    };

    onMounted(() => {
      getRecordsByDate();
    });

    const removeRecord = (recordId) => {
      records.value = records.value.filter(
        (record) => record.record_id !== recordId
      );
    };

    return {
      userInfo,
      records,
      getRecordsByDate,
      removeRecord,
    };
  },
  components: {
    TitleBar,
    BottomNavbar,
    TimeSelector,
    RecordView,
  },
};
</script>

<style scoped>
.block {
  margin-top: 8vh;
}

.container {
  margin-top: 2%;
  padding-top: 1%;
  padding-bottom: 1%;
  margin-left: auto;
  font-size: 25px;
  font-weight: bolder;
}

.records-container {
  margin-bottom: 1rem;
}
</style>
