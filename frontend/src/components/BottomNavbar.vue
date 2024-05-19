<template>
  <nav class="navbar fixed-bottom navbar-expand-lg navbar-dark bg-dark">
    <div class="mx-auto">
      <ul class="navbar-nav text-center">
        <li>
          <router-link to="/investment" class="nav-link"
            >Investment</router-link
          >
        </li>
        <li>
          <router-link to="/record" class="nav-link active">Record</router-link>
        </li>
        <li>
          <router-link to="/history" class="nav-link">History</router-link>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {};
</script>
