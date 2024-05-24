<template>
  <nav class="navbar fixed-bottom navbar-expand-lg navbar-dark bg-dark">
    <div class="mx-auto">
      <ul
        class="navbar-nav text-center"
        v-for="(link, index) in links"
        :key="index"
      >
        <li>
          <router-link
            :to="`${link.url}`"
            class="nav-link"
            active-class="active"
            >{{ link.text }}</router-link
          >
        </li>
        <!-- <li>
          <router-link to="/investment" class="nav-link" active-class="active"
            >Investment</router-link
          >
        </li>
        <li>
          <router-link to="/record" class="nav-link" active-class="active"
            >Record</router-link
          >
        </li>
        <li>
          <router-link to="/history" class="nav-link" active-class="active"
            >History</router-link
          >
        </li> -->
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
