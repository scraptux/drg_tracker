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
      <div class="pt-4 flex items-center space-x-2 px-6">
        <NavbarBreadcrumb
          :drg="store.tracker.getDisplayedVar().getCode(store.show_info).drg"
          :year="store.tracker.ysearch"
          :kapnr="store.tracker.getDisplayedVar().getCode(store.show_info).data.code_data.code.KapNr"
          :grvon="store.tracker.getDisplayedVar().getCode(store.show_info).data.code_data.code.GrVon"
          :dcode="store.tracker.getDisplayedVar().getCode(store.show_info).data.code_data.code.DCode"
          :code="store.tracker.getDisplayedVar().getCode(store.show_info).data.code_data.code.Code.length > 3 ? store.tracker.getDisplayedVar().getCode(store.show_info).data.code_data.code.Code : null"
          :clickable="true"
        ></NavbarBreadcrumb>
      </div>
      <div class="flex flex-row justify-end mx-4 space-x-2 px-2 py-5 border-b border-gray-300">
        <h3 class="text-xl flex-1 font-medium leading-6 text-gray-900">{{ store.tracker.getDisplayedVar().getCode(store.show_info).data.code_data.code.Code }} - {{ store.tracker.getDisplayedVar().getCode(store.show_info).data.code_data.code.Titel }}</h3>
        
        <button @click="editEditData()"
          v-if="store.tracker.getDisplayedVar().getCode(store.show_info).data.code_data.status_code!=0 && (store.tracker.getDisplayedVar().getCode(store.show_info).data.edit_status<=1 || store.tracker.getDisplayedVar().getCode(store.show_info).data.edit_status==3)"
          height="38px" class="flex self-end justify-center rounded-md border border-transparent bg-yellow-500 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:ring-offset-2">
          <span class="pr-2">Bearbeiten</span>
          <i class="fa-solid fa-pen text-sm"></i>
        </button>
        <button @click="resetEditData()"
          v-if="store.tracker.getDisplayedVar().getCode(store.show_info).data.code_data.status_code!=0 && store.tracker.getDisplayedVar().getCode(store.show_info).data.edit_status==2"
          height="38px" class="flex self-end justify-center rounded-md border border-transparent bg-red-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2">
          <span class="pr-2">Zurücksetzen</span>
          <i class="fa-solid fa-x text-sm"></i>
        </button>
        <button @click="saveEditData()"
          v-if="store.tracker.getDisplayedVar().getCode(store.show_info).data.code_data.status_code!=0 && (store.tracker.getDisplayedVar().getCode(store.show_info).data.edit_status==0 || store.tracker.getDisplayedVar().getCode(store.show_info).data.edit_status==2)"
          height="38px" class="flex self-end justify-center rounded-md border border-transparent bg-green-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2">
          <span v-if="store.tracker.getDisplayedVar().getCode(store.show_info).data.edit_status==0" class="pr-2">Ohne Änderung übernehmen</span>
          <span v-if="store.tracker.getDisplayedVar().getCode(store.show_info).data.edit_status==2" class="pr-2">Speichern</span>
          <i class="fa-solid fa-check text-sm"></i>
        </button>

        <span v-if="store.tracker.getDisplayedVar().getCode(store.show_info).data.edit_status==3" class="flex self-end justify-center rounded-md border border-green-500 py-2 px-4 text-sm font-medium text-green-500 shadow-sm">
          <span class="pr-2">Gespeichert</span>
          <i class="fa-solid fa-check text-sm"></i>
        </span>
        <span v-if="store.tracker.getDisplayedVar().getCode(store.show_info).data.edit_status==1" class="flex self-end justify-center rounded-md border border-green-500 py-2 px-4 text-sm font-medium text-green-500 shadow-sm">
          <span class="pr-2">Ohne Änderung übernommen</span>
          <i class="fa-solid fa-check text-sm"></i>
        </span>
        <span v-if="store.tracker.getDisplayedVar().getCode(store.show_info).data.code_data.status_code==0" class="flex self-end justify-center rounded-md border border-green-500 py-1 px-2 text-sm font-medium text-green-500 shadow-sm">
          Keine Probleme gefunden
        </span>
      </div>
      <!-- Info Content -->
      <div class="flex-1 py-4 overflow-y-scroll">
        <!-- Code Editing -->
        <div v-if="store.tracker.getDisplayedVar().getCode(store.show_info).data.edit_status>=2" class="mx-4 px-2 pb-5 border-b border-gray-300" :class="(store.tracker.getDisplayedVar().getCode(store.show_info).data.edit_status==3)?'opacity-60':''">
          <span v-if="store.tracker.getDisplayedVar().getCode(store.show_info).data.edit_status==2" class="text-sm font-medium">Codes zum Einbeziehen auswählen:</span>
          <span v-if="store.tracker.getDisplayedVar().getCode(store.show_info).data.edit_status==3" class="text-sm font-medium">Ausgewählte Codes:</span>
          <table class="table w-full mt-2 text-center">
            <tbody>
              <tr class="bg-gray-200 border-b border-gray-300">
                <td></td>
                <td v-for="year in store.tracker.getDisplayedVar().getCode(store.show_info).data.uniqueYears()" :key="year" class="py-2 border-l border-gray-300">
                  <span>{{ year }}</span>
                </td>
              </tr>
              <tr v-for="val in store.tracker.getDisplayedVar().getCode(store.show_info).data.byCode()" :key="val" class="border-b border-gray-300">
                <td class="text-left w-16 py-2 border-r border-gray-300">{{ val[0].code }}</td>
                <td v-for="year in val" :key="year" class="border-l border-gray-300" :class="[(year.selected)?'bg-green-400':'bg-red-400',(store.tracker.getDisplayedVar().getCode(store.show_info).data.edit_status==2)?'cursor-pointer':'']" @click="year.toggleSelected()">
                  <i v-if="year.selected" class="fa-solid fa-check text-lg"></i>
                  <i v-if="!year.selected" class="fa-solid fa-x text-sm"></i>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <!-- Info SVG -->
        <TrackingSVG class="pt-4" :data="store.tracker.getDisplayedVar().getCode(store.show_info).data.code_data"></TrackingSVG>
      </div>
    </div>
  </div>
</template>

<script>
import { store } from '../store'

import TrackingSVG from '@/components/TrackingSVG.vue'
import NavbarBreadcrumb from './NavbarBreadcrumb.vue'

export default {
  data() {
    return {
      store
    }
  },
  methods: {
    resetEditData() {
      store.tracker.getDisplayedVar().getCode(store.show_info).data.resetEditData();
    },
    editEditData() {
      store.tracker.getDisplayedVar().getCode(store.show_info).data.edit_status = 2;
    },
    saveEditData() {
      store.tracker.saveEditData(store.show_info);
    },
    closeInfo() {
      store.show_info = ""
    },
  },
  components: { NavbarBreadcrumb, TrackingSVG }
}
</script>