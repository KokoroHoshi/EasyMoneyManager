<template>
  <div class="page-container">
    <TitleBar title="Record" />

    <div class="block"></div>

    <div class="inner">
      <div class="inner-content">
        <RecordCard :record="emptyRecord" />
      </div>
    </div>
    <BottomNavbar />
  </div>
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
.block {
  margin-top: clamp(20px, 3vw, 50px);
}

.inner {
  display: flex;
  width: 100%;
  height: auto;
  justify-content: center;
  font-size: 24px;
  font-weight: bolder;
  padding-bottom: 5%;
}

.inner-content {
  width: 80%;
}

.page-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #ffffff;
}
</style>
