<template>
  <vue-highcharts
    type="stockChart"
    :options="chartOptions"
    :redrawOnUpdate="true"
    :oneToOneUpdate="false"
    :animateOnUpdate="true"
    @updated="onUpdated"
  />
</template>

<script>
import axios from "axios";
import VueHighcharts from "vue3-highcharts";
import HighCharts from "highcharts";
import StockCharts from "highcharts/modules/stock";

StockCharts(HighCharts);

export default {
  components: {
    VueHighcharts,
  },
  //   setup() {
  //     const chartOptions = {
  //       rangeSelector: {
  //         selected: 1,
  //       },

  //       title: {
  //         text: "Stock Prices",
  //       },
  //       series: [
  //         {
  //           name: "MyStock",
  //           data: [],
  //         },
  //       ],
  //     };

  //     const fetchData = async () => {
  //       try {
  //         const response = await axios.get(
  //           "http://localhost:5000/api/stock-data"
  //         );
  //         chartOptions.series[0].data = response.data;
  //       } catch (error) {
  //         console.error("Error fetching stock data:", error);
  //       }
  //     };

  //     fetchData();

  //     return {
  //       chartOptions,
  //     };
  //   },
  data() {
    return {
      chartOptions: {
        rangeSelector: {
          selected: 1, // 3m
          buttons: [
            { type: "month", count: 1, text: "1m" },
            { type: "month", count: 3, text: "3m" },
            { type: "month", count: 6, text: "6m" },
            { type: "ytd", text: "YTD" },
            { type: "year", count: 1, text: "1y" },
            { type: "all", text: "All" },
          ],
          inputEnabled: true,
        },
        title: {
          text: "Stock Prices",
        },
        series: [
          {
            name: "MyStock",
            data: [],
          },
        ],
      },
    };
  },
  methods: {
    async fetchData(selected) {
      try {
        const response = await axios.post(
          "http://localhost:5000/api/stock-data",
          { selected }
        );
        this.chartOptions.series[0].data = response.data;
      } catch (error) {
        console.error("Error fetching stock data:", error);
      }
    },

    onUpdated() {
      console.log("Chart updated");
    },
  },
  watch: {
    "chartOptions.rangeSelector.selected"(newVal) {
      console.log(newVal);
    },
  },
};
</script>
