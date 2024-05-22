<template>
  <TitleBar title="Record" />

  <div class="container">
    <RecordCard :record="emptyRecord" />
  </div>

  <BottomNavbar />
</template>

<script>
import TitleBar from "@/components/TitleBar.vue";
import BottomNavbar from "@/components/BottomNavbar.vue";
import RecordCard from "@/components/RecordCard.vue";

export default {
  components: {
    TitleBar,
    BottomNavbar,
    RecordCard,
  },
  data() {
    return {
      emptyRecord: {
        name: "",
        amount: 0,
        tags: [],
        type: "",
        date: "",
      },
    };
  },
};
</script>
