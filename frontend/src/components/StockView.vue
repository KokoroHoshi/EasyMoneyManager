<template>
  <SearchBar :search-query="searchQuery" @search="searchQuery = $event" />

  <div class="container">
    <div class="row">
      <div v-if="stockId && stockName" class="col-12">
        <div class="mb-3">
          <h3>{{ stockName }} ({{ stockId }})</h3>
        </div>
        <div class="mb-3">
          <h5>current price: {{ currentPrice }}</h5>
          <h5>predicted price: {{ predictedPrice }}</h5>
        </div>
        <div class="mb-3">
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
      <div v-else class="col-12 no-data">No data</div>
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

import SearchBar from "./SearchBar.vue";
import API_BASE_URL from "@/config";

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
    SearchBar,
  },
  data() {
    return {
      searchQuery: "",
      stockId: "",
      stockName: "",
      currentPrice: "",
      predictedPrice: "",
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
    searchQuery(newSearchQuery) {
      this.stockId = newSearchQuery;
      this.fetchStockInfo();
      this.fetchStockData();
      this.getStockPrediction();
    },
  },
  methods: {
    fetchStockInfo() {
      const path = `${API_BASE_URL}/api/get/stock_info?stock_id=${this.stockId}`;
      axios
        .get(path)
        .then((res) => {
          const data = res.data;
          console.log(data);

          this.stockName = data["stock_name"];
          this.currentPrice = data["current_price"];
        })
        .catch((err) => {
          console.log(err);
        });
    },
    fetchStockData() {
      const path = `${API_BASE_URL}/api/get/stock_data?stock_id=${this.stockId}&timescale=${this.selectedTimeScale}`;
      axios
        .get(path)
        .then((res) => {
          const data = res.data;
          console.log(data);

          const labels = [];
          const datasetData = [];
          const timestamps = Object.keys(data);

          timestamps.forEach((timestamp) => {
            labels.push(timestamp);

            const stockData = data[timestamp];

            // need to check vue-chartjs how to include all messages below in line-chart
            // const stockInfo = {
            //   Close: stockData.Close,
            //   Open: stockData.Open,
            //   High: stockData.High,
            //   Low: stockData.Low,
            //   Volume: stockData.Volume,
            // };
            datasetData.push(stockData.Close);
          });

          this.chartData.labels = labels;
          this.chartData.datasets[0].data = datasetData;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getStockPrediction() {
      const path = `${API_BASE_URL}/api/get/stock_prediction?stock_id=${this.stockId}`;
      axios
        .get(path)
        .then((res) => {
          const data = res.data;
          console.log(data);

          // temporary
          this.predictedPrice = data["0"];
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
  padding-top: 5px;
}
.chart-container {
  position: relative;
  height: 200px;
  width: 100%;
}
.no-data {
  border: 2px dashed #ccc;
  padding: 30px 20px;
  text-align: center;
  color: #777;
}
</style>
