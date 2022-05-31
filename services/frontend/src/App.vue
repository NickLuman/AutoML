<template>
  <div id="app">
    <NavBar v-if="isAuthenticated"/>
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
  }
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