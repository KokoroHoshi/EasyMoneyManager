<template>
  <TitleBar title="History" />

  <div class="container">
    <TimeSelector @date-selected="getRecordsByDate" />
    <div
      class="records-container"
      v-for="record in records"
      :key="record.record_id"
    >
      <RecordView
        v-if="record"
        :record="record"
        @recordDeleted="removeRecord"
      />
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
import API_BASE_URL from "@/config";

export default {
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      vm.getRecordsByDate();
    });
  },
  setup() {
    const { userInfo } = useAuth();
    const records = ref([]);

    const getRecordsByDate = ({ startUTC, endUTC } = {}) => {
      // 如果 startUTC/endUTC 不存在，改用今天
      if (!startUTC || !endUTC) {
        const today = new Date();
        const localStart = new Date(
          today.getFullYear(),
          today.getMonth(),
          today.getDate(),
          0,
          0,
          0
        );
        const localEnd = new Date(
          today.getFullYear(),
          today.getMonth(),
          today.getDate(),
          23,
          59,
          59
        );
        startUTC = localStart.toISOString();
        endUTC = localEnd.toISOString();
      }

      const userId = userInfo.value?.sub;
      if (!userId) {
        // guest 模式
        const guestRecords = JSON.parse(
          localStorage.getItem("guest_records") || "[]"
        );
        records.value = guestRecords.filter((rec) => {
          const recDate = new Date(rec.date);
          return recDate >= new Date(startUTC) && recDate <= new Date(endUTC);
        });
        return;
      }

      // 已登入 → 後端查詢
      axios
        .get(`${API_BASE_URL}/api/get/records`, {
          params: { user_id: userId, start: startUTC, end: endUTC },
        })
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
      // RecordView has already handled deleting from storage (localStorage or server)
      // Here we just remove from the local records array to update UI
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
