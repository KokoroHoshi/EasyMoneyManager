<template>
  <TitleBar title="Edit" />

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
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

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
      const recordId = route.query.record_id;
      if (!recordId) {
        console.error("Record ID is missing");
        return;
      }
      const path = `http://localhost:5000/api/get/record?user_id=${userInfo.value?.sub}&record_id=${recordId}`;
      axios
        .get(path)
        .then((res) => {
          if (res.data.status === "success") {
            const recordData = res.data.record;
            recordData.tags = recordData.tags ? recordData.tags.split(",") : [];
            record.value = recordData;
            record.value.record_id = recordId;
          } else {
            console.error("Record not found");
          }
        })
        .catch((err) => {
          console.error("Error fetching record:", err);
        });
    };

    onMounted(() => {
      getRecord();
    });

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
.container {
  margin: 1rem;
}
</style>
