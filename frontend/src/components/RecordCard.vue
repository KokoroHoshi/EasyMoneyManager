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
      <button class="btn btn-danger me-2" @click="handleExpense">
        expense
      </button>
      <button class="btn btn-success me-2" @click="handleIncome">income</button>
    </div>
  </div>
</template>

<script>
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
    };
  },
  methods: {
    addTag() {
      const newTag = prompt("Input new tag:");
      if (newTag) {
        this.tags.push(newTag);
      }
    },
    handleExpense() {
      this.type = "expense";
      alert(
        `${this.type}: name - ${this.name}, amount - ${
          this.amount
        }, tags - ${this.selectedTags.join(", ")}`
      );
    },
    handleIncome() {
      this.type = "income";
      alert(
        `${this.type}: name - ${this.name}, amount - ${
          this.amount
        }, tags - ${this.selectedTags.join(", ")}`
      );
    },
  },
};
</script>
