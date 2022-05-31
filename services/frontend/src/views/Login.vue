<template>
  <section>
    <div class="container-fluid mb-4 mt-5">
      <div class="row justify-content-center h3">ВХОД</div>
    </div>
    <form @submit.prevent="submit">
      <div class="mb-3">
        <label for="username" class="form-label">Username:</label>
        <input type="text" name="username" v-model="user.username" class="form-control" />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password:</label>
        <input type="password" name="password" v-model="user.password" class="form-control" />
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </section>
</template>

<script>
import { mapActions } from 'vuex';
export default {
  name: 'Login',
  data() {
    return {
      user: {
        username: '',
        password:'',
      }
    };
  },
  methods: {
    ...mapActions(['logIn']),
    async submit() {
      await this.logIn(this.user);
      this.$router.push('/dashboard');
    }
  }
}
</script>

<style>
section {
    width: 1ax;
    height: 200px;
    position: absolute;
    margin: auto;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0; 
}

.row {
  color: rgb(210,206,196);
}
</style>