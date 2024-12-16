<script setup>

import {computed, ref, onBeforeMount} from 'vue'
import axios from 'axios';
import _ from 'lodash';

const berserkGeography = ref ([])
const berserkGeographyToAdd = ref ({})
const berserkGeographyToUpdate = ref ({})

async function fetchBerserkGeography() {
  const r = await axios.get("/api/berserk_geography/");
  berserkGeography.value = r.data;
}

onBeforeMount(async()=>{       //обработка первой загрузки страницы
  await fetchBerserkGeography()
})


async function onBerserkGeographyAdd(){
  await axios.post("/api/berserk_geography/", berserkGeographyToAdd.value);
  await fetchBerserkGeography();
  berserkGeographyToAdd.value = {}
}

async function onRemoveClick(character){
  await axios.delete(`/api/berserk_geography/${character.id}/`);
  await fetchBerserkGeography();
}

async function onBerserkGeographyEditClick(character) {
  berserkGeographyToUpdate.value = { ...character };
}

async function onUpdateBerserkGeography() {
  await axios.put(`/api/berserk_geography/${berserkGeographyToUpdate.value.id}/`, {
    ...berserkGeographyToUpdate.value,
  });
  await fetchBerserkGeography();
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
                    v-model="berserkGeographyToUpdate.name"/>
                  <label for="floatingInput">Название</label>
                </div>
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    v-model="berserkGeographyToUpdate.description"/>
                  <label for="floatingInput">Описание</label>
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
              @click="onUpdateBerserkGeography"
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
<form @submit.prevent.stop="onBerserkGeographyAdd">
  <div class="row">
    <div class="col">
      <div>
        <div class="form-floating" style="margin-bottom: 10px;">
          <input type="text" class="form-control" v-model="berserkGeographyToAdd.name" required/>
          <label for="floatingInput">Название</label>
        </div>
        <div class="form-floating">
          <input type="text" class="form-control" v-model="berserkGeographyToAdd.description" required/>
          <label for="floatingInput">Описание</label>
        </div>
      </div>
    </div>
    <div class="col-auto">
      <button class="btn btn-submit">Добавить</button>
    </div>
  </div>
</form>

  <div>
      <div v-for="item in berserkGeography" class="item-item">
        <div>{{ item.name }}</div> 
        <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;  grid-column: 2 / 4;">{{ item.description }}</div> 
        <button  class="btn btn-update"
        @click="onBerserkGeographyEditClick(item)"
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
  border-color: $green-300;
}

.form-select{
  border-color: $green-300;
}

.btn-submit {
  background-color: $green-400; // Используем основной цвет
  color: white; // Цвет текста
  border: none;
  padding: 7px 10px;
  &:hover {
    background-color: darken($green-400, 10%); // Затемняем цвет при наведении
  }
}

.btn-update {
  background-color: $green-600; // Используем основной цвет
  color: white; // Цвет текста
  border: none;
  padding: 7px 12px;
  &:hover {
    background-color: darken($green-600, 10%); // Затемняем цвет при наведении
  }
}

.btn-remove {
  background-color: $green-700; // Используем основной цвет
  color: white; // Цвет текста
  border: none;
  padding: 7px 12px;
  &:hover {
    background-color: darken($green-700, 10%); // Затемняем цвет при наведении
  }
}

.item-item{
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid $green-300;
  border-radius: 8px;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr auto auto;
  align-items: center;
  align-content: center;
  justify-content: space-between;
  gap: 16px;
  background-color: $green-100;
}
</style>
