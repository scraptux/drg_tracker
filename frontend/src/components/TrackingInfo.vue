<template>
  <!-- INFO POPUP -->
  <div v-if="store.show_info!=''" @click="closeInfo()" class="fixed flex z-20 w-full h-full bg-black top-0 bg-opacity-50 justify-center items-center">
    <div @click.stop.prevent="" class="flex flex-col w-10/12 bg-white rounded-lg z-20" style="max-height: calc( 500% / 6 )">
      <!-- Leave Button -->
      <button @click="closeInfo()"
        class="absolute ml-auto aspect-square h-6 text-gray-600 rounded-full hover:bg-gray-300"
        style="margin-left: calc( (500%/6) - 26px ); margin-top: 2px;">
        <i class="fa-solid fa-x"></i>
      </button>
      <!-- Title -->
      <ol class="pt-4 flex items-center space-x-2 px-6">
        <li>
          <div class="flex items-center">
            <router-link :to="`/${store.tracking_vars[store.displayed_var][store.show_info].drg}`" class="mr-2 text-sm font-medium text-gray-900">
              <span v-if="store.tracking_vars[store.displayed_var][store.show_info].drg=='icd'">ICD-10</span>
              <span v-if="store.tracking_vars[store.displayed_var][store.show_info].drg=='ops'">OPS</span>
            </router-link>
            <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
              <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
            </svg>
          </div>
        </li>
        <li>
          <div class="flex items-center">
            <router-link :to="`/${store.tracking_vars[store.displayed_var][store.show_info].drg}/version/${store.tracking_vars[store.displayed_var][store.show_info].year}`" class="mr-2 text-sm font-medium text-gray-900">
              {{ store.tracking_vars[store.displayed_var][store.show_info].year }}
            </router-link>
            <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
              <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
            </svg>
          </div>
        </li>
        <li>
          <div class="flex items-center">
            <router-link :to="`/${store.tracking_vars[store.displayed_var][store.show_info].drg}/version/${store.tracking_vars[store.displayed_var][store.show_info].year}/kapitel/${store.tracking_vars[store.displayed_var][store.show_info].data.code.KapNr}`" class="mr-2 text-sm font-medium text-gray-900">
              {{ store.tracking_vars[store.displayed_var][store.show_info].data.code.KapNr }}
            </router-link>
            <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
              <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
            </svg>
          </div>
        </li>
        <li>
          <div class="flex items-center">
            <router-link :to="`/${store.tracking_vars[store.displayed_var][store.show_info].drg}/version/${store.tracking_vars[store.displayed_var][store.show_info].year}/gruppe/${store.tracking_vars[store.displayed_var][store.show_info].data.code.GrVon}`" class="mr-2 text-sm font-medium text-gray-900">
              {{ store.tracking_vars[store.displayed_var][store.show_info].data.code.GrVon }} - {{ store.tracking_vars[store.displayed_var][store.show_info].data.code.GrBis }}
            </router-link>
            <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
              <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
            </svg>
          </div>
        </li>
        <li v-if="store.tracking_vars[store.displayed_var][store.show_info].drg == 'ops'">
          <div class="flex items-center">
            <router-link :to="`/${store.tracking_vars[store.displayed_var][store.show_info].drg}/version/${store.tracking_vars[store.displayed_var][store.show_info].year}/dreisteller/${store.tracking_vars[store.displayed_var][store.show_info].data.code.DCode}`" class="mr-2 text-sm font-medium text-gray-900">
              {{ store.tracking_vars[store.displayed_var][store.show_info].data.code.DCode }}
            </router-link>
            <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
              <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
            </svg>
          </div>
        </li>
        <li>
          <div class="flex items-center">
            <router-link :to="`/${store.tracking_vars[store.displayed_var][store.show_info].drg}/version/${store.tracking_vars[store.displayed_var][store.show_info].year}/code/${store.tracking_vars[store.displayed_var][store.show_info].data.code.GruppeCodeNorm}`" class="mr-2 text-sm font-medium text-gray-900">
              {{ store.tracking_vars[store.displayed_var][store.show_info].data.code.GruppeCode }}
            </router-link>
            <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
              <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
            </svg>
          </div>
        </li>
        <li class="text-sm">
          <p class="font-medium text-gray-500">{{ store.tracking_vars[store.displayed_var][store.show_info].data.code.Code }}</p>
        </li>
      </ol>
      <div class="flex flex-row justify-end mx-4 space-x-2 px-2 py-5 border-b border-gray-300">
        <h3 class="text-xl flex-1 font-medium leading-6 text-gray-900">{{ store.tracking_vars[store.displayed_var][store.show_info].data.code.Code }} - {{ store.tracking_vars[store.displayed_var][store.show_info].data.code.Titel }}</h3>
        
        <button @click="editEditData()"
          v-if="store.tracking_vars[store.displayed_var][store.show_info].data.status_code!=0 && (store.tracking_vars[store.displayed_var][store.show_info].edit_code<=1 || store.tracking_vars[store.displayed_var][store.show_info].edit_code==3)"
          height="38px" class="flex self-end justify-center rounded-md border border-transparent bg-yellow-500 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:ring-offset-2">
          <span class="pr-2">Bearbeiten</span>
          <i class="fa-solid fa-pen text-sm"></i>
        </button>
        <button @click="resetEditData()"
          v-if="store.tracking_vars[store.displayed_var][store.show_info].data.status_code!=0 && store.tracking_vars[store.displayed_var][store.show_info].edit_code==2"
          height="38px" class="flex self-end justify-center rounded-md border border-transparent bg-red-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2">
          <span class="pr-2">Zurücksetzen</span>
          <i class="fa-solid fa-x text-sm"></i>
        </button>
        <button @click="saveEditData()"
          v-if="store.tracking_vars[store.displayed_var][store.show_info].data.status_code!=0 && (store.tracking_vars[store.displayed_var][store.show_info].edit_code==0 || store.tracking_vars[store.displayed_var][store.show_info].edit_code==2)"
          height="38px" class="flex self-end justify-center rounded-md border border-transparent bg-green-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2">
          <span v-if="store.tracking_vars[store.displayed_var][store.show_info].edit_code==0" class="pr-2">Ohne Änderung übernehmen</span>
          <span v-if="store.tracking_vars[store.displayed_var][store.show_info].edit_code==2" class="pr-2">Speichern</span>
          <i class="fa-solid fa-check text-sm"></i>
        </button>

        <span v-if="store.tracking_vars[store.displayed_var][store.show_info].edit_code==3" class="flex self-end justify-center rounded-md border border-green-500 py-2 px-4 text-sm font-medium text-green-500 shadow-sm">
          <span class="pr-2">Gespeichert</span>
          <i class="fa-solid fa-check text-sm"></i>
        </span>
        <span v-if="store.tracking_vars[store.displayed_var][store.show_info].edit_code==1" class="flex self-end justify-center rounded-md border border-green-500 py-2 px-4 text-sm font-medium text-green-500 shadow-sm">
          <span class="pr-2">Ohne Änderung übernommen</span>
          <i class="fa-solid fa-check text-sm"></i>
        </span>
        <span v-if="store.tracking_vars[store.displayed_var][store.show_info].data.status_code==0" class="flex self-end justify-center rounded-md border border-green-500 py-1 px-2 text-sm font-medium text-green-500 shadow-sm">
          Keine Probleme gefunden
        </span>
      </div>
      <!-- Info Content -->
      <div class="flex-1 py-4 overflow-y-scroll">
        <!-- Code Editing -->
        <div v-if="store.tracking_vars[store.displayed_var][store.show_info].edit_code>=2" class="mx-4 px-2 pb-5 border-b border-gray-300" :class="(store.tracking_vars[store.displayed_var][store.show_info].edit_code==3)?'opacity-60':''">
          <span v-if="store.tracking_vars[store.displayed_var][store.show_info].edit_code==2" class="text-sm font-medium">Codes zum Einbeziehen auswählen:</span>
          <span v-if="store.tracking_vars[store.displayed_var][store.show_info].edit_code==3" class="text-sm font-medium">Ausgewählte Codes:</span>
          <table class="table w-full mt-2 text-center">
            <tbody>
              <tr class="bg-gray-200 border-b border-gray-300">
                <td></td>
                <td v-for="year in (store.tracking_years[1]-store.tracking_years[0]+1)" :key="year" class="py-2 border-l border-gray-300">
                  <span>{{ year+store.tracking_years[0]-1 }}</span>
                </td>
              </tr>
              <tr v-for="(val, code) in store.tracking_vars[store.displayed_var][store.show_info].edit_data" :key="code" class="border-b border-gray-300">
                <td class="text-left w-16 py-2 border-r border-gray-300">{{ code }}</td>
                <td v-for="year in val" :key="year" class="border-l border-gray-300" :class="[(year.checked)?'bg-green-400':'bg-red-400',(store.tracking_vars[store.displayed_var][store.show_info].edit_code==2)?'cursor-pointer':'']" @click="year.checked=!year.checked">
                  <i v-if="year.checked" class="fa-solid fa-check text-lg"></i>
                  <i v-if="!year.checked" class="fa-solid fa-x text-sm"></i>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <!-- Info SVG -->
        <TrackingSVG class="pt-4" :data="store.tracking_vars[store.displayed_var][store.show_info].data"></TrackingSVG>
      </div>
    </div>
  </div>
</template>

<script>
import { store } from '../store'

import TrackingSVG from '@/components/TrackingSVG.vue'

export default {
  data() {
    return {
      store
    }
  },
  methods: {
    resetEditData() {
      store.resetEditData(store.displayed_var, store.show_info)
    },
    editEditData() {
      store.tracking_vars[store.displayed_var][store.show_info].edit_code = 2
    },
    saveEditData() {
      if (store.tracking_vars[store.displayed_var][store.show_info].edit_code == 0) {
        store.tracking_vars[store.displayed_var][store.show_info].edit_code = 1
      } else if (store.tracking_vars[store.displayed_var][store.show_info].edit_code == 2) {
        store.tracking_vars[store.displayed_var][store.show_info].edit_code = 3
      }
    },
    closeInfo() {
      store.show_info = ""
    },
  },
  components: { TrackingSVG }
}
</script>