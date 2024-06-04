<template>
  <nav class="navbar fixed-bottom navbar-expand-lg navbar-dark bg-dark">
    <div class="mx-auto">
      <ul class="navbar-nav text-center">
        <li v-for="(link, index) in links" :key="index">
          <router-link
            :to="`${link.url}`"
            class="nav-link"
            active-class="active"
            >{{ link.text }}</router-link
          >
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      links: [
        {
          text: "Investment",
          url: "/investment",
        },
        {
          text: "Record",
          url: "/record",
        },
        {
          text: "History",
          url: "/history",
        },
      ],
    };
  },
};
</script>

<style scoped>
.nav-link {
  font-size: 20px;
  margin-right: 2rem;
  margin-left: 2rem;
  display: flex;
  align-items: center;
  text-align: center;
  height: 5rem;
}

.nav-link:hover {
  background-color: gray;
}

.navbar {
  padding: 0;
  justify-content: center;
  display: flex;
}

li {
  height: 5rem;
  font-weight: bolder;
}
</style>
