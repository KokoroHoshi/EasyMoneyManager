<template>
  <div
    class="card mb-3"
    :class="{
      'bg-danger': record.type === 'expense',
      'bg-success': record.type === 'income',
    }"
    @click="navigateToEdit"
  >
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-start">
        <h2 class="card-title">{{ record.name }}</h2>
        <button
          class="btn btn-warning btn-sm button-style"
          @click.stop="confirmDelete"
        >
          Delete
        </button>
      </div>
      <p class="card-text">Date: {{ formattedDate }}</p>
      <dl class="row">
        <dt class="col-sm-3">Amount</dt>
        <dd class="col-sm-9">$ {{ record.amount }}</dd>

        <dt class="col-sm-3">Tags</dt>
        <dd class="col-sm-9">
          <div class="d-flex flex-wrap">
            <div class="me-3" v-for="(tag, index) in tagsArray" :key="index">
              <label>{{ tag }}</label>
            </div>
          </div>
        </dd>

        <dt class="col-sm-3">Type</dt>
        <dd class="col-sm-9">{{ record.type }}</dd>
      </dl>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from "vue3-toastify";
import { useAuth } from "@/useAuth";
import API_BASE_URL from "@/config";

export default {
  setup() {
    const { userInfo } = useAuth();

    return {
      userInfo,
    };
  },
  props: {
    record: {
      type: Object,
      required: true,
      default: () => ({}),
    },
  },
  computed: {
    tagsArray() {
      const t = this.record.tags;

      if (Array.isArray(t)) {
        return t;
      } else if (typeof t === "string") {
        return t
          .split(",")
          .map((tag) => tag.trim())
          .filter((tag) => tag);
      } else {
        return [];
      }
    },
    formattedDate() {
      if (!this.record.date) return "";
      return new Date(this.record.date).toLocaleString("zh-TW", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
      });
    },
  },
  methods: {
    navigateToEdit() {
      if (!this.record.record_id) {
        console.error("record_id is missing!");
        return;
      }

      this.$router.push({
        name: "EditPage",
        query: {
          record_id: this.record.record_id,
        },
      });
    },
    confirmDelete() {
      if (confirm("Are you sure you want to delete this record?")) {
        this.deleteRecord();
      }
    },
    deleteRecord() {
      const userId = this.userInfo?.sub;

      if (!userId) {
        // Guest 模式：删除 localStorage
        let guestRecords = JSON.parse(
          localStorage.getItem("guest_records") || "[]"
        );
        guestRecords = guestRecords.filter(
          (rec) => rec.record_id !== this.record.record_id
        );
        localStorage.setItem("guest_records", JSON.stringify(guestRecords));

        toast("Record deleted successfully", { type: "success" });
        this.$emit("recordDeleted", this.record.record_id);
        return;
      }

      const payload = {
        userId: userId,
        record_id: this.record.record_id,
      };

      axios
        .delete(`${API_BASE_URL}/api/delete/record`, { data: payload })
        .then((response) => {
          console.log("Record deleted:", response.data);
          toast("Record deleted successfully", { type: "success" });
          this.$emit("recordDeleted", this.record.record_id);
        })
        .catch((error) => {
          console.error("Error deleting record:", error);
          toast("Error deleting record", { type: "error" });
        });
    },
  },
};
</script>

<style scoped>
.card {
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.card:hover {
  filter: brightness(90%);
}

.button-style {
  font-size: 20px;
  font-weight: bold;
}
</style>
