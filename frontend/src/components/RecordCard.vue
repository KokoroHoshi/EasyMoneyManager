<template>
  <div class="card p-3">
    <div class="mb-3">
      <label for="nameInput" class="form-label">name</label>
      <input
        type="text"
        id="nameInput"
        class="form-control"
        v-model="localRecord.name"
      />
    </div>

    <div class="mb-3">
      <label for="amountInput" class="form-label">amount</label>
      <input
        type="number"
        min="0"
        id="amountInput"
        class="form-control"
        v-model="localRecord.amount"
      />
    </div>

    <div class="mb-0">
      <label class="form-label">tags</label>
    </div>

    <div class="mb-3 d-flex flex-wrap">
      <div
        class="form-check me-3 mb-2"
        v-for="(tag, index) in mergedTags"
        :key="index"
      >
        <input
          class="form-check-input"
          type="checkbox"
          :id="'checkbox-' + index"
          v-model="localRecord.selectedTags"
          :value="tag"
        />
        <label class="form-check-label" :for="'checkbox-' + index">
          {{ tag }}
        </label>
      </div>
      <button class="btn btn-primary btn-sm" @click="addTag">+</button>
    </div>

    <div v-if="localRecord.record_id" class="mb-3">
      <label for="dateInput" class="form-label">Date</label>
      <input
        type="datetime-local"
        id="dateInput"
        class="form-control"
        v-model="formattedDate"
        @input="updateLocalRecordDate"
      />
    </div>

    <div class="mx-auto">
      <button class="btn btn-danger me-2" @click="submit('expense')">
        expense
      </button>
      <button class="btn btn-success me-2" @click="submit('income')">
        income
      </button>
    </div>
  </div>
</template>

<script>
import { useAuth } from "@/useAuth";
import axios from "axios";
import { toast } from "vue3-toastify";

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
      default: () => ({
        name: "",
        amount: 0,
        tags: [],
        type: "",
        date: "",
      }),
    },
  },
  data() {
    return {
      defaultTags: [
        "Food",
        "Clothing",
        "Housing",
        "Transportation",
        "Education",
        "Entertainment",
      ],
      localRecord: {
        record_id: "",
        name: "",
        amount: 0,
        selectedTags: [],
        type: "",
        date: "",
      },
      formattedDate: "",
    };
  },
  computed: {
    mergedTags() {
      return [
        ...new Set([...this.defaultTags, ...this.localRecord.selectedTags]),
      ];
    },
  },
  watch: {
    record: {
      immediate: true,
      handler(newRecord) {
        this.localRecord = { ...newRecord, selectedTags: [...newRecord.tags] };
        this.formattedDate = this.formatDateForInput(newRecord.date); // Format date for input
      },
    },
    "localRecord.selectedTags": {
      handler(newTags) {
        newTags.forEach((tag) => {
          if (!this.defaultTags.includes(tag)) {
            this.defaultTags.push(tag);
          }
        });
      },
      deep: true,
    },
  },
  methods: {
    formatDateForInput(dateString) {
      if (!dateString) return "";
      const date = new Date(dateString);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const day = String(date.getDate()).padStart(2, "0");
      const hours = String(date.getHours()).padStart(2, "0");
      const minutes = String(date.getMinutes()).padStart(2, "0");
      return `${year}-${month}-${day}T${hours}:${minutes}`;
    },
    updateLocalRecordDate(event) {
      this.localRecord.date = event.target.value;
    },
    addTag() {
      const newTag = prompt("Input new tag:");
      if (newTag && !this.defaultTags.includes(newTag)) {
        this.defaultTags.push(newTag);
      }
    },
    async submit(type) {
      if (
        (!this.localRecord.amount && this.localRecord.amount !== 0) ||
        isNaN(this.localRecord.amount)
      ) {
        alert("Please enter a valid number for the amount.");
        return;
      }

      this.localRecord.type = type;

      if (!this.localRecord.record_id) {
        const now = new Date();
        this.localRecord.date = now.toISOString().slice(0, 16);
      }

      const payload = {
        userId: this.userInfo.sub,
        records: [
          {
            name: this.localRecord.name,
            amount: this.localRecord.amount,
            tags: this.localRecord.selectedTags,
            type: this.localRecord.type,
            date: this.localRecord.date,
          },
        ],
      };

      this.localRecord.record_id = this.$route.query.record_id;

      const url = this.localRecord.record_id
        ? `http://localhost:5000/api/update/record`
        : "http://localhost:5000/api/add/record";

      const method = this.localRecord.record_id ? "put" : "post";

      await axios[method](
        url,
        this.localRecord.record_id
          ? {
              userId: this.userInfo.sub,
              record_id: this.localRecord.record_id,
              record: payload.records[0],
            }
          : payload
      )
        .then(() => {
          toast(`${payload.records[0].name} $ ${payload.records[0].amount}`, {
            theme: "colored",
            type: payload.records[0].type === "income" ? "success" : "error",
            position: "top-center",
            pauseOnFocusLoss: false,
            dangerouslyHTMLString: true,
          });
        })
        .catch((err) => {
          console.error("Error saving data:", err);
        });

      if (this.$route.name === "RecordPage") {
        this.cleanForm();
      } else if (this.$route.name === "EditPage") {
        this.$router.push({ name: "HistoryPage" });
      }
    },
    cleanForm() {
      this.localRecord = {
        name: "",
        amount: 0,
        selectedTags: [],
        type: "",
        date: "",
      };
      this.formattedDate = "";
    },
  },
};
</script>

<style scoped>
.container {
  padding-top: 20px;
}
.chart-container {
  position: relative;
  height: 200px;
  width: 100%;
}
</style>
