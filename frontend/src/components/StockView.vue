<template>
  <div class="contain">
    <CanvasJSStockChart :options="options" :style="styleOptions" />
  </div>
</template>

<script>
import axios from "axios";
import CanvasJSStockChart from "@canvasjs/vue-stockcharts";

export default {
  components: { CanvasJSStockChart },
  created() {
    this.fetchData();
  },
  data() {
    return {
      stock_data: {},
      dps1: [],
      dps2: [],
      chart: null,
      options: {
        exportEnabled: true,
        theme: "light2",
        title: {
          text: "Vue.js StockChart with Date-Time Axis",
        },
        subtitles: [
          {
            text: "Stock Price",
          },
        ],
        charts: [
          {
            axisY: {
              title: "Price",
              prefix: "$",
              tickLength: 0,
            },
            data: [
              {
                type: "candlestick",
                name: "Price (in USD)",
                yValueFormatString: "$#,###.##",
                dataPoints: [],
              },
            ],
          },
        ],
        navigator: {
          data: [
            {
              dataPoints: [],
            },
          ],
          slider: {
            minimum: new Date(2020, 1, 1),
            maximum: new Date(2020, 11, 1),
          },
        },
      },
      styleOptions: {
        width: "50%",
        height: "200px",
      },
    };
  },

  methods: {
    async fetchData() {
      try {
        const response = await axios.get(
          "http://localhost:5000/api/get-stock-data"
        );
        this.stock_data = response.data;

        this.dps1 = [];
        this.dps2 = [];

        this.stock_data.forEach((data) => {
          this.dps1.push({
            x: new Date(data.date),
            y: [data.open, data.high, data.low, data.close],
          });
          this.dps2.push({ x: new Date(data.date), y: data.close });
        });

        this.options.charts[0].data[0].dataPoints = this.dps1;
        this.options.navigator.data[0].dataPoints = this.dps2;
      } catch (error) {
        console.error("Error fetching stock data:", error);
      }
    },
  },
};
</script>
