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
          <line-chart
            :data="chartData"
            :options="chartOptions"
            :key="chartKey"
          ></line-chart>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default {
  components: {
    "line-chart": Line,
  },
  data() {
    return {
      timeScales: ["1D", "1W", "1M", "1Y"],
      selectedTimeScale: "1D",
      chartKey: 0, // use this to force the line chart re-render temporary
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
      },
    };
  },
  created() {
    this.fetchStockData();
  },
  watch: {
    chartData: {
      handler() {
        this.chartKey += 1;
      },
      deep: true,
    },
  },
  methods: {
    fetchStockData() {
      const path = `http://127.0.0.1:5000/api/stock?timescale=${this.selectedTimeScale}`;
      axios
        .get(path)
        .then((res) => {
          const data = res.data;

          this.chartData.labels = data.map((point) => point.date);
          this.chartData.datasets[0].data = data.map((point) => point.price);
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
