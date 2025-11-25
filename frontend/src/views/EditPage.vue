<template>
  <div class="page-container">
    <TitleBar title="Edit" />

    <div class="inner">
      <div class="inner-content">
        <RecordCard :record="record" />
      </div>
    </div>

    <BottomNavbar />
  </div>
</template>

<script>
import TitleBar from "@/components/TitleBar.vue";
import BottomNavbar from "@/components/BottomNavbar.vue";
import RecordCard from "@/components/RecordCard.vue";
import axios from "axios";
import { useAuth } from "@/useAuth";
import { ref, watch } from "vue";
import { useRoute } from "vue-router";
import API_BASE_URL from "@/config";

export default {
  setup() {
    const route = useRoute();
    const { userInfo } = useAuth();
    const record = ref({
      record_id: "",
      name: "",
      amount: 0,
      tags: [],
      type: "",
      date: "",
    });

    const getRecord = () => {
      const userId = userInfo.value?.sub;
      const recordId = route.query.record_id;

      if (!recordId || !userId) {
        console.error("Record ID or user ID is missing");
        return;
      }

      axios
        .get(`${API_BASE_URL}/api/get/record`, {
          params: { user_id: userId, record_id: recordId },
        })
        .then((res) => {
          if (res.data.status === "success") {
            const recordData = res.data.record;
            recordData.tags = recordData.tags ? recordData.tags.split(",") : [];
            record.value = { ...recordData, record_id: recordId };
          } else {
            console.error("Record not found");
          }
        })
        .catch((err) => {
          console.error("Error fetching record:", err);
          console.error("Error response data:", err.response.data);
        });
    };

    // watch userInfo，userInfo 準備好後才抓資料
    watch(
      () => userInfo.value,
      (val) => {
        if (val?.sub) getRecord();
      },
      { immediate: true } // 頁面一載入就檢查一次
    );

    return {
      userInfo,
      record,
      getRecord,
    };
  },
  components: {
    TitleBar,
    BottomNavbar,
    RecordCard,
  },
};
</script>

<style scoped>
.inner {
  display: flex;
  width: 100%;
  height: auto;
  justify-content: center;
  font-weight: bolder;
  padding-bottom: 5%;
}

.inner-content {
  width: 80%;
}

.page-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #ffffff;
}
</style>
