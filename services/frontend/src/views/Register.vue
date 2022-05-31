<template>
    <div class="container-main">
      <div class="row justify-content-center">
        <div class="col mb-5">
          <h1>ЗАРЕГИСТРИРОВАТЬСЯ</h1>
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
                <LetterIcon/>
              </span>
            </div>
            <input type="text" name="email" v-model="user.email" placeholder="электронная почта" class="form-control" />
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
        <div class="col-9 mb-4">
          <div class="input-group">
            <div class="input-group-prepend">
              <span class="input-group-text" id="">
                <LockIcon/>
              </span>
            </div>
            <input type="password" name="password" v-model="user.repeatPassword" placeholder="повторите пароль" class="form-control" />
          </div>
        </div>
      </div>
      <div class="row justify-content-center">
        <div>
          <button type="submit" class="btn btn-submit col-9">Зарегистрироваться</button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import LockIcon from '@/components/icons/LockIcon.vue'
import UserIcon from '@/components/icons/UserIcon.vue'
import LetterIcon from '@/components/icons/LetterIcon.vue'
export default {
  components: {
    LockIcon,
    UserIcon,
    LetterIcon
  },
  name: 'Register',
  data() {
    return {
      user: {
        username: '',
        email: '',
        password: '',
      },
    };
  },
  methods: {
    ...mapActions(['register']),
    async submit() {
      try {
        await this.register(this.user);
      } catch (error) {
        throw error.message();
      }
    },
    validate: function() {
        if (this.user.password != this.user.repeatPassword) {
          alert("Пароли не совпадают")
          return
        }
    }
  },
};
</script>

<style>
.container-main {
  margin: 10% 25% 10% 25%;
  padding: 5% 0% 7% 0%;
  border: 1px solid rgb(119,119,118); 
}

.btn-submit {
  background-color: rgb(223, 198, 147); 
  font-size: 1.5rem;
}

.btn-submit:hover {
  box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
  color: rgb(100,100,100);
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

h1 {
  color: rgb(210,206,196);
}
</style>