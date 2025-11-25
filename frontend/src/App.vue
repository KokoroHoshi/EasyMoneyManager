<template>
  <router-view />
</template>

<script setup>
import { useToastStore } from "@/stores/toastStore";
import { watch } from "vue";
import { toast } from "vue3-toastify";
import { useRoute } from "vue-router";

const toastStore = useToastStore();
const route = useRoute();

// 1️. 即時 toast => 監聽 toastStore.queue
watch(
  () => toastStore.queue.length,
  () => {
    console.log(toastStore.queue);
    const remaining = [];
    toastStore.queue.forEach((item) => {
      if (item.immediate) {
        // 同頁面立即顯示
        toast(item.message, {
          type: item.type,
          theme: "colored",
          position: "top-center",
          autoClose: 3000,
        });
      } else {
        // 跨頁面先保留
        remaining.push(item);
      }
    });

    // 移除已顯示的 toast
    toastStore.queue = remaining;
  }
);

// 2. 延遲 toast（跨頁面）在路由完成後觸發 => 監聽路由變化
watch(
  () => route.fullPath,
  () => {
    console.log(toastStore.queue);
    while (toastStore.queue.length > 0) {
      const item = toastStore.pop();
      toast(item.message, {
        type: item.type,
        theme: "colored",
        position: "top-center",
        autoClose: 3000,
      });
    }
  }
);
</script>
