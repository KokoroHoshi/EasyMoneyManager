import { createRouter, createWebHistory } from "vue-router";
import RecordPage from "../views/RecordPage.vue";

const routes = [
  {
    path: "/record",
    component: RecordPage,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
