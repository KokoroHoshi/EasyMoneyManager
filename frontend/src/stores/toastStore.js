import { defineStore } from "pinia";

export const useToastStore = defineStore("toast", {
  state: () => ({
    queue: [], //存放要顯示的toast
  }),
  actions: {
    add(message, type = "info", immediate = true) {
      this.queue.push({ message, type, immediate });
    },
    pop() {
      return this.queue.length ? this.queue.shift() : null;
    },
    remove(index) {
      this.queue.splice(index, 1);
    },
    clear() {
      this.queue = [];
    },
  },
});
