<script setup>

import {ref, watch} from 'vue'
import axios from 'axios';
import { useRouter } from 'vue-router'; 
import useUserProfileStore from '@/stores/userProfileStore';

const name = ref();
const isInvalid = ref(false);
const password = ref();
const router = useRouter();
const result = ref(false);
const userProfileStore = useUserProfileStore();

async function register_in() {
      const params = {
        username: name.value,
        password: password.value,
      };

      try {
        const r = await axios.post("/api/register/", JSON.stringify(params), { 
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
        }
      } catch (error) {
        console.error("Ошибка при авторизации:", error);
        isInvalid.value = true
        
      }
    }

</script>

<template>

<div class="container" style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh;">

  <div class="alert alert-success" role="alert" v-if="isInvalid" style="width: 60%;">
    Имя пользователя уже занято :(
  </div>

 
    <form class="item-item" @submit.prevent="register_in" style="width: 60%;">
    <h5 style="text-align: center;">Регистрация</h5>
    <div class="mb-3">
      <label class="form-label">Логин</label>
      <input type="text" class="form-control" aria-describedby="emailHelp" v-model="name" required>
      <div id="emailHelp" class="form-text">Придумайте логин</div>
    </div>
    <div class="mb-3">
      <label for="exampleInputPassword1" class="form-label">Пароль</label>
      <input type="password" class="form-control" v-model="password" required>
      <div id="emailHelp" class="form-text">Придумайте пароль</div>
    </div>
    <div style="text-align: center;">
      <button type="submit" class="btn btn-submit" style="width: 40%;">Зарегистрироваться</button>
    </div>
    </form>
  
</div>

</template>

<style lang="scss" scoped>

@import "bootstrap/scss/bootstrap";

.text-registration{
  color: $blue-600;
}

.item-item{
  border: 2px solid $blue-600;
  border-radius: 8px;
  gap: 16px;
  padding: 40px;
}

.btn-submit {
  background-color: $blue-600; // Используем основной цвет
  color: white; // Цвет текста
  border: none;
  padding: 7px 10px;
  &:hover {
    background-color: darken($blue-600, 10%); // Затемняем цвет при наведении
  }
}

.form-control{
  border-color: $blue-600;
}

.form-control:focus {
  border-color: $blue-600;
  box-shadow: 0 0 0 0.35rem rgba($blue-300, 0.5); 
}

</style>