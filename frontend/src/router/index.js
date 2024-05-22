import { createRouter, createWebHistory } from "vue-router";
import RecordPage from "../views/RecordPage.vue";
import InvestmentPage from "../views/InvestmentPage.vue";
import HistoryPage from "../views/HistoryPage.vue";
import EditPage from "../views/EditPage.vue";

const routes = [
  {
    path: "/record",
    name: "RecordPage",
    component: RecordPage,
  },
  {
    path: "/investment",
    component: InvestmentPage,
  },
  {
    path: "/history",
    name: "HistoryPage",
    component: HistoryPage,
  },
  {
    path: "/edit",
    name: "EditPage",
    component: EditPage,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
