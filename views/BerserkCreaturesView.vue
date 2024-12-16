<script setup>

import {onMounted, ref, onBeforeMount} from 'vue'
import axios from 'axios';
import _ from 'lodash';

const berserkCreature = ref ([])
const berserkCreatureToAdd = ref ({})
const berserkCreatureToUpdate = ref ({})
const berserkCreaturePictureRef1 = ref([])
const berserkCreaturePictureRef2 = ref([])
const berserkCreatureAddImageUrls = ref([])
const berserkCreatureUpdateImageUrls = ref([])
const berserkCreatureDeleteImageUrls = ref([])
const album = ref ([])
const selectedPictures = ref([])
const currentIndex = ref(0)

async function fetchBerserkCreature() {
  const r = await axios.get("/api/berserk_creatures/");
  berserkCreature.value = r.data;
}

async function fetchAlbum() {
  const r = await axios.get("/api/album/");
  album.value = r.data;
}

onBeforeMount(async()=>{       //обработка первой загрузки страницы
  await fetchAlbum()
  await fetchBerserkCreature()
})


async function onBerserkCreatureAdd() {
    // Сначала добавляем существо
    const response = await axios.post("/api/berserk_creatures/", berserkCreatureToAdd.value);
    const newCreatureId = response.data.id;
    
    // Проверяем, есть ли файлы
    if (berserkCreaturePictureRef2.value.files) {
        const files = berserkCreaturePictureRef2.value.files;

        // Итерация по каждому файлу и отправка его отдельно
        for (let i = 0; i < files.length; i++) {
            const formDataAlbum = new FormData();

            // Добавляем ID существа в formData
            formDataAlbum.append('creature', newCreatureId);
            // Добавляем текущее изображение
            formDataAlbum.append('picture', files[i]);

            // Отправляем POST запрос для каждого изображения
            await axios.post("/api/album/", formDataAlbum, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
        }
    }

    await fetchAlbum()
    await fetchBerserkCreature();

    berserkCreatureToAdd.value = {}
    berserkCreatureAddImageUrls.value = []
    berserkCreaturePictureRef2.value.value = []
}

async function onRemoveClick(character){
  await axios.delete(`/api/berserk_creatures/${character.id}/`);
  await fetchAlbum()
  await fetchBerserkCreature();
}

async function onBerserkCreatureEditClick(creature) {
  berserkCreatureToUpdate.value = { ...creature };

  console.log('Editing creature:', creature);

  if (album.value.some(it => it.creature.id === creature.id))
  {
    berserkCreatureDeleteImageUrls.value = album.value
    .filter(item => item.creature.id === creature.id) 
    .map(item => item.picture);
  }
}

async function onUpdateBerserkCreature() {
  await axios.put(`/api/berserk_creatures/${berserkCreatureToUpdate.value.id}/`, {
    ...berserkCreatureToUpdate.value,
  });

  if (berserkCreaturePictureRef1.value.files) {
        const files = berserkCreaturePictureRef1.value.files;

        // Итерация по каждому файлу и отправка его отдельно
        for (let i = 0; i < files.length; i++) {
            const formDataAlbum = new FormData();

            // Добавляем ID существа в formData
            formDataAlbum.append('creature', berserkCreatureToUpdate.value.id);
            // Добавляем текущее изображение
            formDataAlbum.append('picture', files[i]);

            // Отправляем POST запрос для каждого изображения
            await axios.post("/api/album/", formDataAlbum, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
        }
  }

  await fetchAlbum()
  await fetchBerserkCreature();
}

async function berserkCreatureAddPictureChange(){
  console.log('Загрузка изображений...');
  
  berserkCreatureAddImageUrls.value = [];

  const files = berserkCreaturePictureRef2.value.files;

  if (files.length === 0) {
        console.error('Файлы не выбраны.');
        return;
  }
  
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const imageUrl = URL.createObjectURL(file);
    console.log('Добавляю изображение:', imageUrl);
    berserkCreatureAddImageUrls.value.push(imageUrl);
  }

  console.log('Все добавленные изображения:', berserkCreatureAddImageUrls.value);
  console.log('Все добавленные изображения:', berserkCreaturePictureRef2.value.files.length);
}

async function berserkCreatureUpdatePictureChange(){

  berserkCreatureUpdateImageUrls.value = [];

  const files = berserkCreaturePictureRef1.value.files;

  if (files.length === 0) {
        console.error('Файлы не выбраны.');
        return;
  }
  
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const imageUrl = URL.createObjectURL(file);
    console.log('Добавляю изображение:', imageUrl);
    berserkCreatureUpdateImageUrls.value.push(imageUrl);
  }
}

async function deleteImage(imageURL) {
  console.log('Album Value:', album.value);
  console.log('Berserk Creature to Update:', berserkCreatureToUpdate.value);

  // Находим необходимое изображение
  const image = album.value.find(item => 
    item.creature.id === berserkCreatureToUpdate.value.id && 
    item.picture === imageURL);
  
  if (image) {
    console.log('Image ID to delete:', image.id);

    // Выполняем запрос на удаление
    await axios.delete(`/api/album/${image.id}/`);

    // Обновляем массив изображений, чтобы удалить удаленное изображение
    berserkCreatureDeleteImageUrls.value = berserkCreatureDeleteImageUrls.value.filter(url => url !== imageURL);
    
    // Обновляем список изображений
    getImagesToDelete(berserkCreatureToUpdate);
    await fetchAlbum();
  } else {
    console.error('Image not found');
  }
}

async function onPictureClick(creature){
   selectedPictures.value = album.value
    .filter(item => item.creature.id === creature.id) 
    .map(item => item.picture);
}

onMounted(() => {
  const photoModal = document.getElementById('photoModal');
  photoModal.addEventListener('hide.bs.modal', resetIndex);
});

async function nextPicture() {
  if (currentIndex.value < selectedPictures.value.length - 1) {
    currentIndex.value++;
  }
}
async function prevPicture() {
  if (currentIndex.value > 0) {
    currentIndex.value--;
  }
}
async function resetIndex() {
    currentIndex.value = 0;
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
              <div class="col" style="text-align: center;" >
                <div class="form-floating" style="margin-bottom: 10px;">
                  <input
                    type="text"
                    class="form-control"
                    v-model="berserkCreatureToUpdate.name"/>
                  <label for="floatingInput">Название</label>
                </div>
                <div class="form-floating" style="margin-bottom: 10px;">
                  <input
                    type="text"
                    class="form-control"
                    v-model="berserkCreatureToUpdate.description"/>
                  <label for="floatingInput">Описание</label>
                </div>
                <div class="image-scroll-container" style="margin-bottom: 10px; max-width: 400px; max-height: 300px; margin-left: 30px;">
                  <div v-for="(imageUrl, index) in berserkCreatureDeleteImageUrls" :key="index" style="margin-right: 15px; margin-top: 10px; margin-bottom: 10px; position: relative;">
                    <img :src="imageUrl" style="max-width: 350px; max-height: 300px;" alt="">
                    <button @click="deleteImage(imageUrl)" class="btn btn-remove" style="position: absolute; top: 10px; right: 10px; z-index: 10;"><i class="bi bi-x"></i></button>
                  </div>
                </div>
                <div class="form-floating" style="margin-bottom: 10px;">
                  <input type="file" 
                        class="form-control" 
                        ref="berserkCreaturePictureRef1" 
                        @change="berserkCreatureUpdatePictureChange" multiple="" >
                  <label for="floatingInput">Добавить картинки</label>
                </div>
                <div class="image-scroll-container" style="margin-bottom: 10px; max-width: 400px; max-height: 300px; margin-left: 30px;">
                  <div v-for="(imageUrl, index) in berserkCreatureUpdateImageUrls" :key="index" style="margin-right: 15px; margin-top: 10px; margin-bottom: 10px;">
                    <img :src="imageUrl" style="max-width: 350px; max-height: 300px;" alt="">
                </div>
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
              @click="onUpdateBerserkCreature"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
  </div>


<div class="container-fluid">
<div class="p-2">
  <form @submit.prevent.stop="onBerserkCreatureAdd">
    <div class="row">
      <div class="col">
        <div>
          <div class="form-floating" style="margin-bottom: 10px;">
            <input type="text" class="form-control" v-model="berserkCreatureToAdd.name" required/>
            <label for="floatingInput">Название</label>
          </div>
          <div class="form-floating">
            <input type="text" class="form-control" v-model="berserkCreatureToAdd.description" required/>
            <label for="floatingInput">Описание</label>
          </div>
        </div>  
      </div>
      <div class="col-auto">
        <div style="margin-bottom: 10px; align-content: center;" >
          <input 
            type="file" 
            class="form-control" 
            ref="berserkCreaturePictureRef2" 
            @change="berserkCreatureAddPictureChange" 
            multiple="">
        </div>
        <div style="text-align: center; max-width: 350px; max-height: 300px;" class="image-scroll-container">
          <div v-for="(imageUrl, index) in berserkCreatureAddImageUrls" :key="index" style="margin-right: 15px; margin-top: 10px; margin-bottom: 10px;">
            <img :src="imageUrl" style="max-width: 350px; max-height: 300px;" alt="">
          </div>
        </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-submit">Добавить</button>
      </div>
    </div>
   </form>

  <div>
      <div v-for="item in berserkCreature" class="item-item">
        <div>{{ item.name }}</div> 
        <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; grid-column: 2 / 4;">{{ item.description }}</div> 
        <div class="image-container">
          <button 
            data-bs-toggle="modal" data-bs-target="#photoModal"
            class="btn btn-light"
            @click="onPictureClick(item)" 
            v-if="album.some(it => it.creature.id === item.id)">
            <i class="bi bi-images"></i>
        </button>
        </div>
        <div class="buttons-container"> 
          <button  class="btn btn-update"
          @click="onBerserkCreatureEditClick(item)"
          data-bs-toggle="modal"
          data-bs-target="#editStudentModal"><i class="bi bi-pencil"></i></button>
          <button class="btn btn-remove" @click="onRemoveClick(item)"><i class="bi bi-x"></i></button>
        </div>
      </div>
  </div>

  <div class="modal fade" id="photoModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" @hide.bs.modal="resetIndex">
    <div class="modal-dialog" style="display: flex; justify-content: center; align-items: center; height: 100%; width: auto; margin-top: 20px; margin-bottom: 20px;">
        <div class="modal-content" style="border: none; background: transparent;">
            <div class="modal-body" style="padding: 0; display: flex; justify-content: center; align-items: center;">
                <button class="btn btn-light" @click="prevPicture" :disabled="currentIndex === 0" style="margin-right: 10px;"><i class="bi bi-caret-left"></i></button>
                <img :src="selectedPictures[currentIndex]" style="max-width: 100%; height: auto; display: block;" alt="">
                <button class="btn btn-light" @click="nextPicture" :disabled="currentIndex === selectedPictures.length - 1" style="margin-left: 10px;"><i class="bi bi-caret-right"></i></button>
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
  border-color: $red-300;
}

.form-select{
  border-color: $red-300;
}

.btn-submit {
  background-color: $red-400; // Используем основной цвет
  color: white; // Цвет текста
  border: none;
  padding: 7px 10px;
  &:hover {
    background-color: darken($red-400, 10%); // Затемняем цвет при наведении
  }
}

.btn-update {
  background-color: $red-600; // Используем основной цвет
  color: white; // Цвет текста
  border: none;
  padding: 7px 12px;
  &:hover {
    background-color: darken($red-600, 10%); // Затемняем цвет при наведении
  }
}

.btn-remove {
  background-color: $red-700; // Используем основной цвет
  color: white; // Цвет текста
  border: none;
  padding: 7px 12px;
  &:hover {
    background-color: darken($red-700, 10%); // Затемняем цвет при наведении
  }
}

.item-item{
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid $red-300;
  border-radius: 8px;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr auto;
  align-items: center;
  align-content: center;
  justify-content: space-between;
  gap: 16px;
  background-color: $red-100;
}
.image-scroll-container {
    display: flex; /* Гладкая горизонтальная полоса */
    overflow-x: auto; /* Горизонтальная прокрутка при переполнении */
    align-items: center;
    align-content: center;
}
.image-container {
  grid-column: 4; /* Занимает 5-ю и 6-ю колонки */
  display: flex;
  justify-content: end; /* Выравнивание изображения по центру */
  align-items: center; 
}

.buttons-container {
  grid-column: 5; /* Занимает 6-ю колонку */
  display: flex;
  justify-content: flex-end; /* Кнопки выравниваются вправо */
  column-gap: 16px;
}
</style>
