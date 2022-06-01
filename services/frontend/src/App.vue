<template>
  <div id="app">
    <NavBar v-if="isLoggedIn"/>
    <div class="main container">
      <router-view/>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
export default {
  components: {
    NavBar
  },
  computed: {
    isLoggedIn: function() {
      return this.$store.getters.isAuthenticated;
    }
  },
}
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
body {
    margin: 0;
    padding: 0;
    background-color:rgb(31,32,41);
}

</style>