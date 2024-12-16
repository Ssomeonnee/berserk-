<script setup>

import {computed, ref, onBeforeMount, onMounted, watch} from 'vue'
import axios from 'axios';
import _ from 'lodash';
import {storeToRefs} from "pinia"
import useUserProfileStore from '@/stores/userProfileStore';
import bootstrap from 'bootstrap/dist/js/bootstrap';
import { useRouter } from 'vue-router'; 
import * as XLSX from 'xlsx';

const userProfileStore = useUserProfileStore();
const {
  isAuthorized,
  isSuperUser,
  username
} = storeToRefs(userProfileStore)

const users = ref ({})
const berserkCharacters = ref ([])
const berserkCreatures = ref ({})
const berserkArmy = ref ({})
const berserkCharacterToAdd = ref ({})
const berserkCharacterToUpdate = ref ({})
const berserkCharacterToRemove = ref ({})
const berserkCharacterPictureRef1 = ref()
const berserkCharacterPictureRef2 = ref()
const berserkCharacterAddImageUrl = ref()
const berserkCharacterUpdateImageUrl = ref()
const selectedPicture = ref(null)
const selectedUserId = ref(null)
const selectedCreatureId = ref(null)
const selectedArmyId = ref(null)
const isWithPicture = ref(false)
const isWithoutPicture = ref(false)
const stats = ref({})
//const isAuthorized = ref(false);
//const isSuperUser = ref(false);
const alert403 = ref(false);
const loading = ref(true)

const otpCode = ref('');
const isLoading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const otpStatus = ref(false)
const otpMessage = ref()
//const editModal = ref();
//const otpModal = ref();
const router = useRouter();

const berserkCreaturesById = computed(()=>{
  return _.keyBy(berserkCreatures.value, x=> x.id)
})

//async function fetchUserProfile() {
 // const r = await axios.get("/api/user-profile/info/");

  //isAuthorized.value = r.data.is_authenticated
 // isSuperUser.value = r.data.is_superuser
  
 // console.log(isAuthorized.value)
 // console.log(isSuperUser.value)

 // if (isSuperUser.value==true)
 //   fetchUsers()
//}

async function fetchUsers() {
  const r = await axios.get("/api/users/");
  users.value = r.data
  console.log(users.value)
}

async function fetchBerserkArmy() {
  const r = await axios.get("/api/berserk_army/");
  berserkArmy.value = r.data;
  
}

async function fetchBerserkCreatures() {
  const r = await axios.get("/api/berserk_creatures/");
  berserkCreatures.value = r.data;
  
}

async function fetchStats(selectedUserId, selectedCreatureId, selectedArmyId, isWithPicture, isWithoutPicture) {
  const params = {};
  if (selectedUserId.value) {
    params.user = selectedUserId.value;
  }
  if (selectedCreatureId.value) {
    params.creature = selectedCreatureId.value;
  }
  if (selectedArmyId.value) {
    params.army = selectedArmyId.value;
  }
  if (isWithPicture.value) {
    params.with_picture = isWithPicture.value; 
  }
  if (isWithoutPicture.value) { 
    params.without_picture = isWithoutPicture.value; 
  }
  const r = await axios.get("/api/berserk_characters/stats/", { params });
  stats.value = r.data;
}

async function fetchBerserkCharacters(selectedUserId, selectedCreatureId, selectedArmyId, isWithPicture, isWithoutPicture) {
  
  loading.value = true;

  const r = await axios.get("/api/berserk_characters/");
  let filteredData = r.data; // Начинаем с исходных данных

  if (selectedUserId.value != null) {
    filteredData = filteredData.filter(it => it.user === selectedUserId.value);
  }
  if (selectedCreatureId.value != null) {
    filteredData = filteredData.filter(it => it.creature.id === selectedCreatureId.value);
  }
  if (selectedArmyId.value != null) {
    filteredData = filteredData.filter(it => it.army.id === selectedArmyId.value);
  }
  if (isWithPicture.value) {
    filteredData = filteredData.filter(it => it.picture !== null);
  }
  if (isWithoutPicture.value) {
    filteredData = filteredData.filter(it => it.picture === null);
  }

  berserkCharacters.value = filteredData; 

  console.log(selectedUserId.value);
  console.log(selectedCreatureId.value);
  console.log(berserkCharacters.value);
  fetchStats(selectedUserId, selectedCreatureId, selectedArmyId, isWithPicture, isWithoutPicture)

  loading.value = false;
}

onBeforeMount(async()=>{
  //обработка первой загрузки страницы
  //await fetchUserProfile()
  console.log(isAuthorized.value)
  fetchBerserkCreatures()
  fetchBerserkCharacters(selectedUserId, selectedCreatureId, selectedArmyId, isWithPicture, isWithoutPicture)
  fetchBerserkArmy()
  // console.log(isSuperUser.value)
  // console.log(isAuthorized.value)
  // if (isSuperUser.value==true)
  //   fetchUsers()
})

//watch(isAuthorized, (newValue) => {
   //   if (!newValue) {
   //     router.push('/login/');
    //  }
  //  });
    
watch(isSuperUser, () => {
  if (isSuperUser.value) {
    console.log(isSuperUser.value)
    fetchUsers()
  }
}, {
  immediate: true
})

async function handleUserChange(){
  await fetchBerserkCharacters(selectedUserId, selectedCreatureId, selectedArmyId, isWithPicture, isWithoutPicture)
}

async function handleCreatureChange(){
  await fetchBerserkCharacters(selectedUserId, selectedCreatureId, selectedArmyId, isWithPicture, isWithoutPicture)
}

async function handleArmyChange(){
  await fetchBerserkCharacters(selectedUserId, selectedCreatureId, selectedArmyId, isWithPicture, isWithoutPicture)
}

async function onBerserkCharacterAdd(){
 
 try{

  const formData = new FormData();

  if(berserkCharacterPictureRef2.value.files[0]){
    formData.append('picture', berserkCharacterPictureRef2.value.files[0]);
  }
  
  formData.set('name', berserkCharacterToAdd.value.name)
  formData.set('jap_name', berserkCharacterToAdd.value.jap_name)
  formData.set('eng_name', berserkCharacterToAdd.value.eng_name)
  formData.set('creature', berserkCharacterToAdd.value.creature)
  formData.set('qoute', berserkCharacterToAdd.value.qoute)
  formData.set('description', berserkCharacterToAdd.value.description)
  formData.set('army', berserkCharacterToAdd.value.army)
 
  await axios.post("/api/berserk_characters/", formData, {
    headers: {
      'Content-Type' : 'multipart/form-data'
    }
  });

  await fetchBerserkCharacters(selectedUserId, selectedCreatureId, selectedArmyId, isWithPicture, isWithoutPicture);
 }
 catch (error)
 {
  if (error.response && error.response.status === 403) {
    alert403.value = true
  }
 }

  berserkCharacterToAdd.value = {}
  berserkCharacterAddImageUrl.value = ''
  berserkCharacterPictureRef2.value.value = ''
}

async function berserkCharacterAddPictureChange(){
  berserkCharacterAddImageUrl.value = URL.createObjectURL(berserkCharacterPictureRef2.value.files[0])
}

async function berserkCharacterUpdatePictureChange(){
  berserkCharacterUpdateImageUrl.value = URL.createObjectURL(berserkCharacterPictureRef1.value.files[0])
}

async function removeCharacter(character){
  await axios.delete(`/api/berserk_characters/${character.id}/`);
  await fetchBerserkCharacters(selectedUserId, selectedCreatureId, selectedArmyId, isWithPicture, isWithoutPicture);
}

async function onRemoveClick(character){
  
  berserkCharacterToRemove.value = { ...character, creature: character.creature.id, army: character.army.id };

  if (! await getOtpStatus()){
    const otpModal = new bootstrap.Modal(document.getElementById('otpModalRemove'));
    otpModal.show();
  }  
  else {
    removeCharacter(character)
  }
}

async function verifyOtpRemoveClick() {
  if (await verifyOtp()){
    const otpModalElement = document.getElementById('otpModalRemove');
    const closeButton = otpModalElement.querySelector('.btn-close');
    closeButton.click();

    removeCharacter(berserkCharacterToRemove.value)
  }
}

async function verifyOtpEditClick() {
  if (await verifyOtp()){
    const otpModalElement = document.getElementById('otpModal');
    const closeButton = otpModalElement.querySelector('.btn-close');
    closeButton.click();

    const editModal = new bootstrap.Modal(document.getElementById('editModal'));
    editModal.show();
  }
}

async function verifyOtp() {
    const response = await axios.post('/api/user-profile/otp-login/', { otp_key: otpCode.value });

    if (response.data.success) {
      console.log("OTP код успешно проверен!")
      otpMessage.value = '';
      return true;
    } else {
      otpMessage.value = 'Неверный OTP код, попробуйте снова.';
      console.log("Неверный OTP код, попробуйте снова.");
      return false;
    }
}

async function getOtpStatus(){
  otpCode.value = '';
  const r = await axios.get("/api/user-profile/otp-status/");
  console.log(r.data.otp_good)
  return r.data.otp_good
}

async function onBerserkCharacterEditClick(character) {
  
  berserkCharacterToUpdate.value = { ...character, creature: character.creature.id, army: character.army.id };

  if (character.picture)
  {
    berserkCharacterUpdateImageUrl.value = character.picture
  }
  
  if (! await getOtpStatus()){
    const otpModal = new bootstrap.Modal(document.getElementById('otpModal'));
    otpModal.show();
  }
  else {
    const editModal = new bootstrap.Modal(document.getElementById('editModal'));
    editModal.show();
  }
}

async function onUpdateBerserkCharacter() {

  const formData = new FormData();
    if(berserkCharacterPictureRef1.value.files[0]){
      formData.append('picture', berserkCharacterPictureRef1.value.files[0])
    }
    //console.log(artistToEdit.value);
    
    formData.set('name', berserkCharacterToUpdate.value.name)
    formData.set('jap_name', berserkCharacterToUpdate.value.jap_name)
    formData.set('eng_name', berserkCharacterToUpdate.value.eng_name)
    formData.set('creature', berserkCharacterToUpdate.value.creature)
    formData.set('qoute', berserkCharacterToUpdate.value.qoute)
    formData.set('description', berserkCharacterToUpdate.value.description)
    formData.set('army', berserkCharacterToUpdate.value.army)
    await axios.put(`/api/berserk_characters/${berserkCharacterToUpdate.value.id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    berserkCharacterPictureRef1.value.value = null; // Сброс файла
    berserkCharacterUpdateImageUrl.value = null; // Сброс URL изображения

  await fetchBerserkCharacters(selectedUserId, selectedCreatureId, selectedArmyId, isWithPicture, isWithoutPicture);
}

async function onPictureClick(character){
   selectedPicture.value = character.picture
}

async function toggleCheckbox(checkboxId, otherCheckboxId) {
      const checkbox = document.getElementById(`inlineCheckbox${checkboxId}`);
      const otherCheckbox = document.getElementById(`inlineCheckbox${otherCheckboxId}`);

      if (checkbox.checked) {
        otherCheckbox.disabled = true;

        if (checkboxId==1){
        isWithoutPicture.value = true;
        isWithPicture.value = false;
        }
        else{
          isWithoutPicture.value = false;
          isWithPicture.value = true;
        }
      } else {
        otherCheckbox.disabled = false;
        isWithoutPicture.value = false;
        isWithPicture.value = false;
      }
      
      await fetchBerserkCharacters(selectedUserId, selectedCreatureId, selectedArmyId, isWithPicture, isWithoutPicture)
}

async function exportExcel()
{
  try {
    // Данные уже отфильтрованы в fetchBerserkCharacters
    const dataToExport = berserkCharacters.value;

    // Заголовки столбцов
    const headers = [
      "Имя",             
      "Японское имя",    
      "Английское имя",  
      "Цитата",          
      "Существо",        
      "Армия",           
      "Описание",        
      "Есть картинка" 
    ];
    
    const worksheetData = [];
    
    if (selectedUserId.value != null) {
      const user = users.value.find(user => user.id === selectedUserId.value);
      worksheetData.push(["Пользователь " + user.username]);
      console.log(user.username)
    }

    worksheetData.push(headers);

    dataToExport.forEach(item => {
        worksheetData.push([
            item.name,
            item.jap_name,
            item.eng_name,
            item.qoute,
            item.creature.name, 
            item.army.name,   
            item.description,
            item.picture ? 'Да' : 'Нет', 
        ]);
    });

    
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.aoa_to_sheet(worksheetData); 
    XLSX.utils.book_append_sheet(wb, ws, 'Лист1'); //

   
    const excelBuffer = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });
    const blob = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'berserk_characters.xlsx');
    document.body.appendChild(link);
    link.click();

  } catch (error) {
    console.error("Ошибка при экспорте в Excel:", error);
  }
}


</script>

<template>

<!-- Modal -->

  <div class="modal fade" id="editModal" tabindex="-1">
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
                    v-model="berserkCharacterToUpdate.name">
                  <label for="floatingInput">Имя</label>
                </div>
                <div class="form-floating" style="margin-bottom: 10px;">
                  <input
                    type="text"
                    class="form-control"
                    v-model="berserkCharacterToUpdate.jap_name"/>
                  <label for="floatingInput">Японское имя</label>
                </div>
                <div class="form-floating" style="margin-bottom: 10px;">
                  <input
                    type="text"
                    class="form-control"
                    v-model="berserkCharacterToUpdate.eng_name"/>
                  <label for="floatingInput">Английское имя</label>
                </div>
                <div class="form-floating" style="margin-bottom: 10px;">
                  <input
                    type="text"
                    class="form-control"
                    v-model="berserkCharacterToUpdate.qoute"/>
                  <label for="floatingInput">Цитата</label>
                </div>
                <div class="form-floating" style="margin-bottom: 10px;">
                  <input
                    type="text"
                    class="form-control"
                    v-model="berserkCharacterToUpdate.description"/>
                  <label for="floatingInput">Описание</label>
                </div>
                <div class="form-floating" style="margin-bottom: 10px;">
                  <input type="file" 
                  class="form-control" 
                  ref="berserkCharacterPictureRef1" 
                  @change="berserkCharacterUpdatePictureChange">
                </div>
                
              </div>
              <div class="col-auto">
                <div class="form-floating" style="margin-bottom: 10px;">
                  <select class="form-select" v-model="berserkCharacterToUpdate.creature">
                    <option :value="c.id" v-for="c in berserkCreatures">
                      {{ c.name }}
                    </option>
                  </select>
                  <label for="floatingInput">Существо</label>
                </div>
                <div class="form-floating" style="margin-bottom: 10px;">
                  <select class="form-select" v-model="berserkCharacterToUpdate.army">
                    <option :value="a.id" v-for="a in berserkArmy">
                      {{ a.name }}
                    </option>
                  </select>
                  <label for="floatingInput">Армия</label>
                </div>
                <div class="form-floating">
                  <img :src="berserkCharacterUpdateImageUrl" style="max-width: 200px; max-height: 300px;" alt="">
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
              @click="onUpdateBerserkCharacter"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
  </div>

  <div class="modal fade" id="otpModal" tabindex="-1" aria-labelledby="editStudentModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="editStudentModalLabel">Введите код верификации</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
               <input
                    type="text"
                    class="form-control"
                    v-model="otpCode"/>
                <div>{{ otpMessage }}</div>    
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-submit" @click="verifyOtpEditClick">Подтвердить</button>
            </div>
          </div>
        </div>
  </div>

  <div class="modal fade" id="otpModalRemove" tabindex="-1" aria-labelledby="editStudentModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="editStudentModalLabel">Введите код верификации</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
               <input
                    type="text"
                    class="form-control"
                    v-model="otpCode"/>
                <div>{{ otpMessage }}</div>    
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-submit" @click="verifyOtpRemoveClick()">Подтвердить</button>
            </div>
          </div>
        </div>
  </div>
 
<div class="container-fluid">
<div class="p-2">

  <div class="alert alert-cst" role="alert" v-if="isAuthorized===false">
    Вы должны быть авторизованы для работы со страницей.
  </div>
  <div class="alert alert-cst-403" role="alert" v-if="alert403===true">
    Вы должны быть авторизованы для выполнения этого действия.
  </div>

  <form @submit.prevent.stop="onBerserkCharacterAdd">
    <div class="row">
      <div class="col-md-3">
        <div>
          <div class="form-floating" style="margin-bottom: 10px;">
            <input type="text" class="form-control" v-model="berserkCharacterToAdd.name" required/>
            <label for="floatingInput">Имя</label>
          </div>
          <div class="form-floating" style="margin-bottom: 10px;">
            <input type="text" class="form-control" v-model="berserkCharacterToAdd.jap_name" required/>
            <label for="floatingInput">Имя на японском</label>
          </div>
          <div class="form-floating" style="margin-bottom: 10px;">
            <input type="text" class="form-control" v-model="berserkCharacterToAdd.eng_name" required/>
            <label for="floatingInput">Имя на английском</label>
          </div>
          <div class="form-floating" style="margin-bottom: 10px;">
            <input type="text" class="form-control" v-model="berserkCharacterToAdd.qoute" required/>
            <label for="floatingInput">Цитата</label>
          </div>
        </div>
      </div>
      <div class="col-auto">
        <div class="form-floating" style="margin-bottom: 10px;">
          <select name="" id="" class="form-select" v-model="berserkCharacterToAdd.creature" required>
            <option :value="c.id" v-for="c in berserkCreatures">{{ c.name }}</option>
          </select>
          <label for="floatingInput">Существо</label>
        </div>
        <div class="form-floating" style="margin-bottom: 10px;">
          <select name="" id="" class="form-select" v-model="berserkCharacterToAdd.army">
            <option :value="a.id" v-for="a in berserkArmy">{{ a.name }}</option>
          </select>
          <label for="floatingInput">Армия</label>
        </div>
        <div class="form-floating" style="margin-bottom: 10px;">
          <textarea class="form-control" style="height: auto;" v-model="berserkCharacterToAdd.description" rows="5" required></textarea> 
          <label for="floatingInput">Описание</label>
        </div>
        
      </div>
      <div class="col">
        <div class="d-flex justify-content-end" style="width: 100%; margin-bottom: 10px;"> 
          <button class="btn btn-submit">Добавить</button>
        </div> 
        <div style="margin-bottom: 10px;">
          <input type="file" class="form-control" ref="berserkCharacterPictureRef2" @change="berserkCharacterAddPictureChange">
        </div>
        <div style="text-align: center; margin-bottom: 10px;">
          <img :src="berserkCharacterAddImageUrl" style="max-width: 250px; max-height: 200px;" alt="">
        </div> 
      </div> 
    </div>
   </form>

 



   <div class="form-floating" v-if="isSuperUser===true">
        <select name="" id="" class="form-select" v-model="selectedUserId" @change="handleUserChange">
          <option :value="null"></option>
          <option :key="u.id" :value="u.id" v-for="u in users">{{ u.username }}</option>
        </select>
        <label for="floatingInput">Выберете пользователя</label>
      </div>

      <div v-if="isSuperUser===true">
        <div class="header-item">
          Статистика по таблице
        </div>
        <div style="display: flex; flex-direction: row;">
          <div style="width: 40%;">
            <div class="item-stat" style="margin-right: 10px; margin-bottom: 16px;">Всего записей: {{ stats.count }}</div>
            <div class="item-stat" style="margin-right: 10px;">Всего записей с картинкой: {{ stats.count_with_image }}</div>
          </div>
          <div style="width: 100%;">
            <div style="display: flex; flex-direction: row; ">
              <div class="text-stat" style="width: 33%;">Популярное существо(ва)</div>
              <div style="flex-grow: 1;"> 
                <select name="" id="" class="form-select item-stat"> 
                  <option :key="u.id" :value="u.id" v-for="u in stats.most_common_creature">{{ u }}</option>
                </select>
              </div>
            </div>
            <div style="display: flex; flex-direction: row;">
              <div class="text-stat" style="width: 33%;">Популярная армия(ии)</div>
              <div style="flex-grow: 1;">
                <select name="" id="" class="form-select item-stat">
                  <option :key="u.id" :value="u.id" v-for="u in stats.most_common_creature">{{ u }}</option>
                </select>
              </div>
            </div>
          </div> 
        </div>
      </div>
      
      <div v-if="isAuthorized===true">
        <div class="header-item">
          Фильтры
        </div>
        <div style="display: flex; flex-direction: row;"> 
          <div style="width: 18%;">
            <div class="form-check form-check-inline filter-item" >
              <input class="form-check-input" type="checkbox" id="inlineCheckbox1" value="option1" @change="toggleCheckbox(1, 2)">
              <label class="form-check-label" for="inlineCheckbox1">Без картинок</label>
            </div>
            <div class="form-check form-check-inline filter-item">
              <input class="form-check-input" type="checkbox" id="inlineCheckbox2" value="option2" @change="toggleCheckbox(2, 1)">
              <label class="form-check-label" for="inlineCheckbox2">С картинкой</label>
            </div>
          </div>
          <div class="filter-item" style="margin-right: 16px; flex-grow: 1;">
            <select name="" id="" class="form-select" v-model="selectedCreatureId" @change="handleCreatureChange">
              <option :value="null">Выберете существо</option>
              <option :key="u.id" :value="u.id" v-for="u in berserkCreatures">{{ u.name }}</option>
            </select>
          </div>
          <div class="filter-item" style="flex-grow: 1;">
            <select name="" id="" class="form-select" v-model="selectedArmyId" @change="handleArmyChange">
              <option :value="null">Выберете армию</option>
              <option :key="u.id" :value="u.id" v-for="u in berserkArmy">{{ u.name }}</option>
            </select>
          </div>
        </div>
      </div>


   <div v-if="loading===true" style="width: 100%; text-align: center; margin-top: 20px;">
      <div style="margin-bottom: 10px;">
        Загрузка...
      </div>  
      <div>
        <img src="C:\Users\Admin\Desktop\веб\client\src\assets\behelit.gif" alt="">
      </div>
   </div>
  <div v-if="loading===false">
      
    
      <div class="d-flex justify-content-end" style="width: 100%;">
        <a href="#" @click="exportExcel" class="text-export">Экспорт в Excel</a>
      </div>

    <div>
      <div v-if="berserkCharacters.length === 0" style="width: 100%; text-align: center; margin-top: 20px;">
        <p>Нет записей</p> 
      </div>
      <div v-else>
      <div v-for="item in berserkCharacters" class="item-item">
        <div>{{ item.name }}</div>
        <div class="extranames-text">{{ item.eng_name }}</div>
        <div class="extranames-text">{{ item.jap_name }}</div>
        <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; grid-column: 4 / 6;">{{ item.description }}</div> 
        <div v-show="item.picture" data-bs-toggle="modal" data-bs-target="#photoModal" class="image-container">
          <img :src="item.picture" @click="onPictureClick(item)" style="max-height: 60px;" alt="">
        </div>
        <div class="buttons-container"> 
          <button class="btn btn-update"
              @click="onBerserkCharacterEditClick(item)"
              data-bs-toggle="modal"
              data-bs-target="#editStudentModal"><i class="bi bi-pencil"></i></button>
          <button class="btn btn-remove" @click="onRemoveClick(item)"><i class="bi bi-x"></i></button>
        </div>
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
   
</div>



</template>

<style lang="scss" scoped>

@import "bootstrap/scss/bootstrap";

.header-item{
  text-align: center; 
  background-color: rgba($pink-200, 0.7);
  margin-top: 10px;
  border-radius: 10px;
}

.filter-item{
  align-items: center;
  align-content: center;
  justify-content: space-between;
  gap: 16px;
}
.alert-cst {
    background-color: $pink-100; 
    color: $pink-400; 
    border-color: $pink-400; 
}

.alert-cst-403 {
    background-color: $pink-200; 
    color: $pink-400; 
    border-color: $pink-400; 
}

.extranames-text{
  color: $pink-600;
}

.form-control{
  border-color: $pink-300;
}

.form-control:focus {
  border-color: $pink-300;
  box-shadow: 0 0 0 0.35rem rgba($pink-100, 0.5); 
} 

.form-select{
  border-color: $pink-300;
}

.form-select:focus {
  border-color: $pink-300;
  box-shadow: 0 0 0 0.35rem rgba($pink-100, 0.5); 
} 

.form-check{
  border-color: $pink-300;
}

.form-check-input{
  border-color: $pink-300;
}

.form-check-input:checked {
  border-color: $pink-300; 
  background-color: $pink-500; /* Дополнительный стиль для фона */
}

.form-check-input:focus {
  border-color: $pink-300;
  box-shadow: 0 0 0 0.35rem rgba($pink-100, 0.5); 
} 

.btn-submit {
  background-color: $pink-400; // Используем основной цвет
  color: white; // Цвет текста
  border: none;
  padding: 7px 10px;
  &:hover {
    background-color: darken($pink-400, 10%); // Затемняем цвет при наведении
  }
}

.btn-update {
  background-color: $pink-600; // Используем основной цвет
  color: white; // Цвет текста
  border: none;
  padding: 7px 12px;
  &:hover {
    background-color: darken($pink-600, 10%); // Затемняем цвет при наведении
  }
}

.btn-remove {
  background-color: $pink-700; // Используем основной цвет
  color: white; // Цвет текста
  border: none;
  padding: 7px 12px;
  &:hover {
    background-color: darken($pink-700, 10%); // Затемняем цвет при наведении
  }
}

.item-item{
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid $pink-300;
  border-radius: 8px;
  display: grid;
  grid-template-columns: repeat(7, 1fr) auto;
  align-items: center;
  align-content: center;
  justify-content: space-between;
  gap: 16px;
  background-color: $pink-100;
}

.text-stat{
  padding: 0.5rem;
  margin: 0.5rem 0;
  align-items: center;
  align-content: center;
  justify-content: space-between;
  gap: 16px;
}
.item-stat{
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid $pink-300;
  border-radius: 8px;
  align-items: center;
  align-content: center;
  justify-content: space-between;
  gap: 16px;
}

.text-export{
  color: $pink-700;
}

.image-container {
  grid-column: 6 / 7; /* Занимает 5-ю и 6-ю колонки */
  display: flex;
  justify-content: end; /* Выравнивание изображения по центру */
  align-items: center; 
}

.buttons-container {
  grid-column: 7; /* Занимает 6-ю колонку */
  display: flex;
  justify-content: flex-end; /* Кнопки выравниваются вправо */
  column-gap: 16px;
}
</style>
