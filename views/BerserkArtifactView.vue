<script setup>

import {computed, ref, onBeforeMount} from 'vue'
import axios from 'axios';
import _ from 'lodash';

const berserkArtifact = ref ([])
const berserkCreatures = ref ({})
const berserkCharacters = ref ({})
const berserkArtifactToAdd = ref ({})
const berserkArtifactToUpdate = ref ({})
const berserkArtifactPictureRef1 = ref()
const berserkArtifactPictureRef2 = ref()
const berserkArtifactAddImageUrl = ref()
const berserkArtifactUpdateImageUrl = ref()
const selectedPicture = ref()


async function fetchBerserkCharacters() {
  const r = await axios.get("/api/berserk_characters/");
  berserkCharacters.value = r.data;
  
}

async function fetchBerserkCreatures() {
  const r = await axios.get("/api/berserk_creatures/");
  berserkCreatures.value = r.data;
  
}

async function fetchBerserkArtifact() {
  const r = await axios.get("/api/berserk_artifact/");
  berserkArtifact.value = r.data;
  
}

onBeforeMount(async()=>{       //обработка первой загрузки страницы
  await fetchBerserkArtifact()
  await fetchBerserkCreatures()
  await fetchBerserkCharacters()
})


async function onBerserkArtifactAdd(){
  const formData = new FormData();

  if(berserkArtifactPictureRef2.value.files[0]){
    formData.append('picture', berserkArtifactPictureRef2.value.files[0]);
  }

  formData.set('name', berserkArtifactToAdd.value.name)
  formData.set('description',  berserkArtifactToAdd.value.description)
  if (berserkArtifactToAdd.value.owner) {
    formData.set('owner', berserkArtifactToAdd.value.owner);
  }
  if (berserkArtifactToAdd.value.harm_to) {
      formData.set('harm_to', berserkArtifactToAdd.value.harm_to);
  }
  if (berserkArtifactToAdd.value.inventor) {
      formData.set('inventor', berserkArtifactToAdd.value.inventor);
  }

  await axios.post("/api/berserk_artifact/", formData, {
    headers: {
      'Content-Type' : 'multipart/form-data'
    }
  });
  await fetchBerserkArtifact();

  berserkArtifactToAdd.value = {}
  berserkArtifactAddImageUrl.value = ''
  berserkArtifactPictureRef2.value.value = ''
}

async function berserkArtifactAddPictureChange(){
  berserkArtifactAddImageUrl.value = URL.createObjectURL(berserkArtifactPictureRef2.value.files[0])
}

async function berserkArtifactUpdatePictureChange(){
  berserkArtifactUpdateImageUrl.value = URL.createObjectURL(berserkArtifactPictureRef1.value.files[0])
}

async function onRemoveClick(character){
  await axios.delete(`/api/berserk_artifact/${character.id}/`);
  await fetchBerserkArtifact();
}

async function onBerserkArtifactEditClick(artifact) {
  berserkArtifactToUpdate.value = { ...artifact, owner: artifact.owner.id, harm_to: artifact.harm_to.id, inventor: artifact.inventor.id};

  if (artifact.picture)
  {
    berserkArtifactUpdateImageUrl.value = artifact.picture
  }

}

async function onUpdateBerserkArtifact() {

  const formData = new FormData();
  
    if(berserkArtifactPictureRef1.value.files[0]){
      formData.append('picture', berserkArtifactPictureRef1.value.files[0])
    }
    
    formData.set('name', berserkArtifactToAdd.value.name)
    formData.set('description',  berserkArtifactToUpdate.value.description)

    if (berserkArtifactToAdd.value.owner) {
      formData.set('owner', berserkArtifactToUpdate.value.owner);
    }

    if (berserkArtifactToAdd.value.harm_to) {
      formData.set('harm_to', berserkArtifactToUpdate.value.harm_to);
    }

    if (berserkArtifactToAdd.value.inventor) {
      formData.set('inventor', berserkArtifactToUpdate.value.inventor);
    }
    await axios.put(`/api/berserk_artifact/${berserkArtifactToUpdate.value.id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    berserkArtifactUpdateImageUrl.value = null
    berserkArtifactPictureRef1.value.value = null

    await fetchBerserkArtifact();
}

async function onPictureClick(character){
   selectedPicture.value = character.picture
}

</script>

<template>

<!-- Modal -->

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
                    v-model="berserkArtifactToUpdate.name"/>
                  <label for="floatingInput">Название</label>
                </div>
                <div class="form-floating" style="margin-bottom: 10px;">
                  <input
                    type="text"
                    class="form-control"
                    v-model="berserkArtifactToUpdate.description"/>
                  <label for="floatingInput">Описание</label>
                </div>
                <div class="form-floating" style="margin-bottom: 10px;">
                  <input type="file" 
                  class="form-control" 
                  ref="berserkArtifactPictureRef1" 
                  @change="berserkArtifactUpdatePictureChange">
                  <label for="floatingInput">Фото</label>
                </div>
              </div>
              <div class="col-auto">
                <div class="form-floating" style="margin-bottom: 10px;">
                  <select class="form-select" v-model="berserkArtifactToUpdate.owner">
                    <option :value="c.id" v-for="c in berserkCharacters">
                      {{ c.name }}
                    </option>
                  </select>
                  <label for="floatingInput">Владелец</label>
                </div>
                <div class="form-floating" style="margin-bottom: 10px;">
                  <select class="form-select" v-model="berserkArtifactToUpdate.harm_to">
                    <option :value="a.id" v-for="a in berserkCreatures">
                      {{ a.name }}
                    </option>
                  </select>
                  <label for="floatingInput">Вредит</label>
                </div>
                <div class="form-floating" style="margin-bottom: 10px;">
                  <select class="form-select" v-model="berserkArtifactToUpdate.inventor">
                    <option :value="a.id" v-for="a in berserkCharacters">
                      {{ a.name }}
                    </option>
                  </select>
                  <label for="floatingInput">Создатель</label>
                </div>
                <div class="form-floating">
                  <img :src="berserkArtifactUpdateImageUrl" style="max-width: 200px; max-height: 300px;" alt="">
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
              @click="onUpdateBerserkArtifact"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
  </div>


<div class="container-fluid">
<div class="p-2">
  <form @submit.prevent.stop="onBerserkArtifactAdd">
    <div class="row">
      <div class="col">
        <div>
          <div class="form-floating" style="margin-bottom: 10px;">
            <input type="text" class="form-control" v-model="berserkArtifactToAdd.name" required/>
            <label for="floatingInput">Название</label>
          </div>
          <div class="form-floating" style="margin-bottom: 10px;">
            <input type="text" class="form-control" v-model="berserkArtifactToAdd.description" required/>
            <label for="floatingInput">Описание</label>
          </div>
        </div>
      </div>
      <div class="col-auto">
        <div class="form-floating" style="margin-bottom: 10px;">
          <select name="" id="" class="form-select" v-model="berserkArtifactToAdd.owner">
            <option :value="c.id" v-for="c in berserkCharacters">{{ c.name }}</option>
          </select>
          <label for="floatingInput">Владелец</label>
        </div>
        <div class="form-floating" style="margin-bottom: 10px;">
          <select name="" id="" class="form-select" v-model="berserkArtifactToAdd.harm_to">
            <option :value="h.id" v-for="h in berserkCreatures">{{ h.name }}</option>
          </select>
          <label for="floatingInput">Вредит</label>
        </div>
        <div class="form-floating">
          <select name="" id="" class="form-select" v-model="berserkArtifactToAdd.inventor">
            <option :value="i.id" v-for="i in berserkCharacters">{{ i.name }}</option>
          </select>
          <label for="floatingInput">Создатель</label>
        </div>
      </div>
      <div class="col-auto">
        <div style="margin-bottom: 10px;">
          <input type="file" class="form-control" ref="berserkArtifactPictureRef2" @change="berserkArtifactAddPictureChange">
        </div>
       <div style="text-align: center; height: 160px;">
        <img :src="berserkArtifactAddImageUrl" style="max-width: 160px; max-height: 160px;" alt="">
       </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-submit">Добавить</button>
      </div>
    </div>
  </form>

    <div>
        <div v-for="item in berserkArtifact" class="item-item">
          <div>{{ item.name }}</div> 
          <div v-if="item.harm_to">Вредит: {{ item.harm_to.name }}</div> 
          <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;  grid-column: 3 / 5;">{{ item.description }}</div> 
          <div v-show="item.picture" data-bs-toggle="modal" data-bs-target="#photoModal" class="image-container"><img :src="item.picture" @click="onPictureClick(item)" style="max-height: 60px;" alt=""></div>
          <div class="buttons-container"> 
            <button  class="btn btn-update"
            @click="onBerserkArtifactEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editStudentModal"><i class="bi bi-pencil"></i></button>
            <button class="btn btn-remove" @click="onRemoveClick(item)"><i class="bi bi-x"></i></button>
          </div>
        </div>
    </div>

    <div class="modal fade" id="photoModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog" style="display: flex; justify-content: center; align-items: center; height: 100%; width: auto; margin-top: 20px; margin-bottom: 20px;" >
      <div class="modal-content" style="border: none; background: transparent;">
        
        <div class="modal-body" style="padding: 0; display: flex; justify-content: center; align-items: center;">
          <img :src="selectedPicture" style="max-width: 100%; height: 100%; display: block;" alt="">
        </div>
        
      </div>
    </div>
</div>
</div>
</div>



</template>

<style lang="scss" scoped>

@import "bootstrap/scss/bootstrap";

.form-control{
  border-color: $purple-300;
}

.form-select{
  border-color: $purple-300;
}

.btn-submit {
  background-color: $purple-400; // Используем основной цвет
  color: white; // Цвет текста
  border: none;
  padding: 7px 10px;
  &:hover {
    background-color: darken($purple-400, 10%); // Затемняем цвет при наведении
  }
}

.btn-update {
  background-color: $purple-600; // Используем основной цвет
  color: white; // Цвет текста
  border: none;
  padding: 7px 12px;
  &:hover {
    background-color: darken($purple-600, 10%); // Затемняем цвет при наведении
  }
}

.btn-remove {
  background-color: $purple-700; // Используем основной цвет
  color: white; // Цвет текста
  border: none;
  padding: 7px 12px;
  &:hover {
    background-color: darken($purple-700, 10%); // Затемняем цвет при наведении
  }
}

.item-item{
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid $purple-300;
  border-radius: 8px;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr 1fr auto;
  align-items: center;
  align-content: center;
  justify-content: space-between;
  gap: 16px;
  background-color: $purple-100;
}

.image-container {
  grid-column: 5; /* Занимает 5-ю и 6-ю колонки */
  display: flex;
  justify-content: end; /* Выравнивание изображения по центру */
  align-items: center; 
}

.buttons-container {
  grid-column: 6; /* Занимает 6-ю колонку */
  display: flex;
  justify-content: flex-end; /* Кнопки выравниваются вправо */
  column-gap: 16px;
}
</style>
