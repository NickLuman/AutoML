<template>
    <div class="container-main">
      <div class="row justify-content-center">
        <div class="col mb-5">
          <h1>ВХОД</h1>
        </div>
      </div>
      <form @submit.prevent="submit">
      <div class="row justify-content-center">
        <div class="col-9 mb-4">
          <div class="input-group">
            <div class="input-group-prepend">
              <span class="input-group-text" id="">
                <UserIcon/>
              </span>
            </div>
            <input type="text" name="username" v-model="user.username" placeholder="логин" class="form-control" />
          </div>
        </div>
      </div>
      <div class="row justify-content-center">
        <div class="col-9 mb-4">
          <div class="input-group">
            <div class="input-group-prepend">
              <span class="input-group-text" id="">
                <LockIcon/>
              </span>
            </div>
            <input type="password" name="password" v-model="user.password" placeholder="пароль" class="form-control" />
          </div>
        </div>
      </div>
      <div class="row justify-content-center">
        <div>
          <button type="submit" class="btn btn-submit col-9">Войти</button>
        </div>
      </div>
      <div class="row justify-content-center">
        <input type="button" class="btn btn-register col-4" onclick="location.href='/register';" value="Зарегистрироваться" />
      </div>
    </form>
  </div>
</template>

<script>
import LockIcon from '@/components/icons/LockIcon.vue'
import UserIcon from '@/components/icons/UserIcon.vue'
import { mapActions } from 'vuex';
export default {
  components: {
    LockIcon,
    UserIcon
  },
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
.container-main {
  margin: 10% 25% 10% 25%;
  padding: 5% 0% 5% 0%;
  border: 1px solid rgb(119,119,118); 
}

.btn-submit {
  background-color: rgb(223, 198, 147); 
  font-size: 1.5rem;
}

.btn-submit:hover {
  color: rgb(100,100,100);
  box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
}

.form-control, .input-group-text {
  background-color: rgb(31,32,41); 
  border: 1px solid rgb(119,119,118);
  color: white;
}

.form-control:focus, .input-group-text:focus {
  background-color: rgb(31,32,41); 
  border: 1px solid rgb(119,119,118);
  color: white;
}

.btn-register {
  margin-top: 3%;
  font-size: 0.9rem;
  border: 1px solid rgb(119,119,118);
  color: rgb(119,119,118);
}

.btn-register:hover {
  color: rgb(180,180,180);
  border: 1px solid rgb(180,180,180);
}

h1 {
  color: rgb(210,206,196);
}
</style>