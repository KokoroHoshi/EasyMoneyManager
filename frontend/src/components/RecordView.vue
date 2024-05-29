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
        <h5 class="card-title">{{ record.name }}</h5>
        <button class="btn btn-warning btn-sm" @click.stop="confirmDelete">
          Delete
        </button>
      </div>
      <p class="card-text">Date: {{ record.date }}</p>
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
      return this.record.tags ? this.record.tags.split(",") : [];
    },
  },
  methods: {
    navigateToEdit() {
      this.$router.push({
        name: "EditPage",
        query: { record_id: this.record.record_id },
      });
    },
    confirmDelete() {
      if (confirm("Are you sure you want to delete this record?")) {
        this.deleteRecord();
      }
    },
    deleteRecord() {
      const payload = {
        userId: this.userInfo.sub,
        record_id: this.record.record_id,
      };

      axios
        .delete("http://localhost:5000/api/delete/record", { data: payload })
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
</style>
