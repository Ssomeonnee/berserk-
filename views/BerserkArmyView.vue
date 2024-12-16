<script setup>

import {computed, ref, onBeforeMount} from 'vue'
import axios from 'axios';
import _ from 'lodash';

const berserkArmy = ref ([])
const berserkGeography = ref ({})
const berserkArmyToAdd = ref ({})
const berserkArmyToUpdate = ref ({})

async function fetchBerserkArmy() {
  const r = await axios.get("/api/berserk_army/");
  berserkArmy.value = r.data;
}

async function fetchBerserkGeography() {
  const r = await axios.get("/api/berserk_geography/");
  berserkGeography.value = r.data;
  
}

onBeforeMount(async()=>{       //обработка первой загрузки страницы
  await fetchBerserkArmy()
  await fetchBerserkGeography()
})


async function onBerserkArmyAdd(){
  await axios.post("/api/berserk_army/", berserkArmyToAdd.value);
  fetchBerserkArmy()
  berserkArmyToAdd.value = {}
}

async function onRemoveClick(army){
  await axios.delete(`/api/berserk_army/${army.id}/`);
  fetchBerserkArmy()
}

async function onBerserkArmyEditClick(army) {
  berserkArmyToUpdate.value = { ...army, geography: army.geography.id };
}

async function onUpdateBerserkArmy() {
  await axios.put(`/api/berserk_army/${berserkArmyToUpdate.value.id}/`, {
    ...berserkArmyToUpdate.value,
  });
  await fetchBerserkArmy()
}

</script>

<template>

<!-- Modal -->
<form>
  <div class="modal fade" id="editStudentModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">
              Редактировать
            </h1>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col">
                <div class="form-floating" style="margin-bottom: 10px;">
                  <input
                    type="text"
                    class="form-control"
                    v-model="berserkArmyToUpdate.name"/>
                  <label for="floatingInput">Название</label>
                </div>
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    v-model="berserkArmyToUpdate.description"/>
                  <label for="floatingInput">Описание</label>
                </div>
              </div>
              <div class="col-auto">
                <div class="form-floating" style="margin-bottom: 10px;">
                  <select class="form-select" v-model="berserkArmyToUpdate.geography">
                    <option :value="g.id" v-for="g in berserkGeography">
                      {{ g.name }}
                    </option>
                  </select>
                  <label for="floatingInput">География</label>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Закрыть
            </button>
            <button
              data-bs-dismiss="modal"
              type="button"
              class="btn btn-submit"
              @click="onUpdateBerserkArmy"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
  </div>
</form>

<div class="container-fluid">
<div class="p-2">
  <form @submit.prevent.stop="onBerserkArmyAdd">
    <div class="row">
      <div class="col">
        <div>
          <div class="form-floating" style="margin-bottom: 10px;">
            <input type="text" class="form-control" v-model="berserkArmyToAdd.name" required/>
            <label for="floatingInput">Назвние</label>
          </div>
          <div class="form-floating" style="margin-bottom: 10px;">
            <input type="text" class="form-control" v-model="berserkArmyToAdd.description" required/>
            <label for="floatingInput">Описание</label>
          </div>
        </div>
      </div>
      <div class="col-auto">
        <div class="form-floating" style="margin-bottom: 10px;">
          <select name="" id="" class="form-select" v-model="berserkArmyToAdd.geography" required>
            <option :value="g.id" v-for="g in berserkGeography">{{ g.name }}</option>
          </select>
          <label for="floatingInput">Армия</label>
        </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-submit">Добавить</button>
      </div>
    </div>
  </form>


    <div>
        <div v-for="item in berserkArmy" class="item-item">
          <div>{{ item.name }}</div> 
          <div>{{ item.geography.name }}</div> 
          <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;  grid-column: 3 / 5;">{{ item.description }}</div> 
          <button  class="btn btn-update"
          @click="onBerserkArmyEditClick(item)"
          data-bs-toggle="modal"
          data-bs-target="#editStudentModal"><i class="bi bi-pencil"></i></button>
          <button class="btn btn-remove" @click="onRemoveClick(item)"><i class="bi bi-x"></i></button>
        </div>
    </div>
</div>
</div>



</template>

<style lang="scss" scoped>

@import "bootstrap/scss/bootstrap";

.form-control{
  border-color: $orange-300;
}

.form-select{
  border-color: $orange-300;
}

.btn-submit {
  background-color: $orange-400; // Используем основной цвет
  color: white; // Цвет текста
  border: none;
  padding: 7px 10px;
  &:hover {
    background-color: darken($orange-400, 10%); // Затемняем цвет при наведении
  }
}

.btn-update {
  background-color: $orange-600; // Используем основной цвет
  color: white; // Цвет текста
  border: none;
  padding: 7px 12px;
  &:hover {
    background-color: darken($orange-600, 10%); // Затемняем цвет при наведении
  }
}

.btn-remove {
  background-color: $orange-700; // Используем основной цвет
  color: white; // Цвет текста
  border: none;
  padding: 7px 12px;
  &:hover {
    background-color: darken($orange-700, 10%); // Затемняем цвет при наведении
  }
}

.item-item{
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid $orange-300;
  border-radius: 8px;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr auto auto;
  align-items: center;
  align-content: center;
  justify-content: space-between;
  gap: 16px;
  background-color: $orange-100;
}
</style>
