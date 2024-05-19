import { createRouter, createWebHistory } from "vue-router";
import RecordPage from "../views/RecordPage.vue";
import InvestmentPage from "../views/InvestmentPage.vue";

const routes = [
  {
    path: "/record",
    component: RecordPage,
  },
  {
    path: "/investment",
    component: InvestmentPage,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
