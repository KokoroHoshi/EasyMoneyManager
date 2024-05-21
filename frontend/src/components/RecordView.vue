<template>
  <div
    class="card mb-3"
    :class="{
      'bg-danger': record.type === 'expense',
      'bg-success': record.type === 'income',
    }"
    @click="showAlert"
  >
    <div class="card-body">
      <h5 class="card-title">{{ record.name }}</h5>
      <p class="card-text">Date: {{ record.date }}</p>
      <dl class="row">
        <dt class="col-sm-3">Amount</dt>
        <dd class="col-sm-9">$ {{ record.amount }}</dd>

        <dt class="col-sm-3">Tags</dt>
        <dd class="col-sm-9">
          <div class="d-flex flex-wrap">
            <div class="me-3" v-for="(tag, index) in record.tags" :key="index">
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
export default {
  props: {
    record: {
      type: Object,
      required: true,
    },
  },
  methods: {
    showAlert() {
      alert("You clicked on: " + this.record.name);
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
