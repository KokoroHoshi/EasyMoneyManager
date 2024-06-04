<template>
  <TitleBar title="Record" />

  <div class="container">
    <RecordCard :record="emptyRecord" class="record-card" />
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

<style scoped>
/* Form Styling */
.record-card {
  background-color: #d8c2b1;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 2px 1px 4px #6e6c6c;
}
.container {
  position: absolute;
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 24px;
  font-weight: bolder;
}
</style>
