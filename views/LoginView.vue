<script setup>

import {ref, watch} from 'vue'
import axios from 'axios';
import { useRouter } from 'vue-router'; 
import useUserProfileStore from '@/stores/userProfileStore';

const login = ref();
const isInvalid = ref(false);
const password = ref();
const router = useRouter();
const result = ref(false);
const userProfileStore = useUserProfileStore();

async function log_in() {
      const params = {
        username: login.value,
        password: password.value,
      };

      try {
        const r = await axios.post("/api/login/", JSON.stringify(params), { 
          headers: {
            'Content-Type': 'application/json' 
          }
        });

        result.value = r.data.success;

        if (result.value) {
          await userProfileStore.fetchUserProfile();
          router.push('/');
        } else {
          isInvalid.value = true
          console.error(r.data.error);
          alert(r.data.error || 'Неверный логин или пароль');
        }
      } catch (error) {
        console.error("Ошибка при авторизации:", error);
        isInvalid.value = true
        // Обработка ошибок
      }
    }

    async function register() {
      router.push('/register');
    }

</script>

<template>

<div class="container" style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh;">

  <div class="alert alert-success" role="alert" v-if="isInvalid" style="width: 60%;">
    Вы ввели неверный логин или пароль :(
  </div>

 
    <form class="item-item" @submit.prevent="log_in" style="width: 60%;">
    <h5 style="text-align: center;">Авторизация</h5>
    <div class="mb-3">
      <label class="form-label">Логин</label>
      <input type="text" class="form-control" aria-describedby="emailHelp" v-model="login" required>
      <div id="emailHelp" class="form-text">Введите логин и пароль</div>
    </div>
    <div class="mb-3">
      <label for="exampleInputPassword1" class="form-label">Пароль</label>
      <input type="password" class="form-control" v-model="password" required>
      <div id="emailHelp" class="form-text">Введите логин и пароль</div>
    </div>
    <div style="text-align: center;">
      <button type="submit" class="btn btn-submit" style="width: 20%;">Войти</button>
    </div>
    </form>
  
  <div style="margin-top: 10px;">
    <a href="#" @click="register" class="text-registration">Зарегистрироваться</a>
  </div>
</div>

</template>

<style lang="scss" scoped>

@import "bootstrap/scss/bootstrap";

.text-registration{
  color: $green-600;
}

.item-item{
  border: 2px solid $teal-600;
  border-radius: 8px;
  gap: 16px;
  padding: 40px;
}

.btn-submit {
  background-color: $teal-700; // Используем основной цвет
  color: white; // Цвет текста
  border: none;
  padding: 7px 10px;
  &:hover {
    background-color: darken($teal-700, 10%); // Затемняем цвет при наведении
  }
}

.form-control{
  border-color: $teal-600;
}

.form-control:focus {
  border-color: $teal-600;
  box-shadow: 0 0 0 0.35rem rgba($teal-300, 0.5); 
}

</style>