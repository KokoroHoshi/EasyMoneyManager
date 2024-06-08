<template>
  <nav class="navbar fixed-bottom navbar-expand-lg navbar-light">
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
.navbar {
  padding: 0;
  justify-content: center;
  display: flex;
  height: 4rem;
}

.navbar-nav {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

li {
  font-weight: bolder;
  display: flex;
  align-items: center;
}

.nav-link {
  font-size: 1.25rem;
  margin: 0 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 4rem;
  border-radius: 10px;
}

.nav-link:hover {
  background-color: gray;
  border-radius: 10px;
}

@media (max-width: 600px) {
  .nav-link {
    font-size: 1rem;
    height: 2rem;
    margin: 0 0.75rem;
  }

  .navbar {
    height: 3rem;
  }

  li {
    height: 3rem;
  }
}
</style>
