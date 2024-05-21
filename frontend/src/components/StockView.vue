<template>
  <div class="container">
    <div class="row">
      <div class="col-12">
        <div class="mb-3">
          <label for="timeScale" class="form-label">Time Scale</label>
          <select
            id="timeScale"
            class="form-select"
            v-model="selectedTimeScale"
            @change="fetchStockData"
          >
            <option v-for="scale in timeScales" :key="scale" :value="scale">
              {{ scale }}
            </option>
          </select>
        </div>
        <div class="chart-container">
          <line-chart :data="chartData" :options="chartOptions"></line-chart>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { Line } from "vue-chartjs";
import { Chart as ChartJS, registerables } from "chart.js";
ChartJS.register(...registerables);

export default {
  name: "StockView",
  components: {
    "line-chart": Line,
  },
  data() {
    return {
      timeScales: ["1D", "1W", "1M", "1Y"],
      selectedTimeScale: "1D",
      chartData: {
        labels: [],
        datasets: [
          {
            label: "Stock Price",
            backgroundColor: "#f87979",
            data: [],
          },
        ],
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: false,
          },
        },
      },
    };
  },
  created() {
    this.getResponse();
  },
  methods: {
    getResponse() {
      const path = `http://127.0.0.1:5000/api/stock?timescale=${this.selectedTimeScale}`;
      axios
        .get(path)
        .then((res) => {
          const data = res.data;
          console.log(data);

          this.chartData.labels = [0, 1, 2];
          this.chartData.datasets[0].data = [1, 2, 3];
        })
        .catch((err) => {
          console.log(err);
        });
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
