<template>
  <div class="card p-3">
    <div class="mb-3">
      <label for="nameInput" class="form-label">name</label>
      <input type="text" id="nameInput" class="form-control" v-model="name" />
    </div>

    <div class="mb-3">
      <label for="amountInput" class="form-label">amount</label>
      <input
        type="number"
        min="0"
        id="amountInput"
        class="form-control"
        v-model="amount"
      />
    </div>

    <div class="mb-0">
      <label class="form-label">tags</label>
    </div>

    <div class="mb-3 d-flex flex-wrap">
      <div
        class="form-check me-3 mb-2"
        v-for="(tag, index) in tags"
        :key="index"
      >
        <input
          class="form-check-input"
          type="checkbox"
          :id="'checkbox-' + index"
          v-model="selectedTags"
          :value="tag"
        />
        <label class="form-check-label" :for="'checkbox-' + index">
          {{ tag }}
        </label>
      </div>
      <button class="btn btn-primary btn-sm" @click="addTag">+</button>
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
import axios from "axios";

export default {
  data() {
    return {
      name: "",
      amount: 0,
      tags: [
        "Food",
        "Clothing",
        "Housing",
        "Transportation",
        "Education",
        "Entertainment",
      ],
      selectedTags: [],
      type: "",
      date: "",
    };
  },
  methods: {
    addTag() {
      const newTag = prompt("Input new tag:");
      if (newTag) {
        this.tags.push(newTag);
      }
    },
    submit(type) {
      this.date = new Date().toISOString();
      this.type = type;

      const payload = {
        type: this.type,
        name: this.name,
        amount: this.amount,
        tags: this.selectedTags,
        date: this.date,
      };

      axios
        .post("http://localhost:5000/api/post/record", payload)
        .then((response) => {
          console.log("Data saved:", response.data);
        })
        .catch((error) => {
          console.error("Error saving data:", error);
        });

      // alert(
      //   `${this.type}: name - ${this.name}, amount - ${
      //     this.amount
      //   }, tags - ${this.selectedTags.join(", ")}, date - ${this.date}`
      // );
    },
  },
};
</script>
