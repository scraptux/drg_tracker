<template>
  <div class="bg-white grid grid-cols-10 h-full">
    <!-- SIDEBAR -->
    <div class="flex flex-col col-span-3 bg-gray-100 border-r border-gray-300 h-full max-h-full overflow-y-auto">
      <TrackingSidebar></TrackingSidebar>
    </div>
    <!-- CONTENT -->
    <div class="col-span-7 h-full h-max-full bg-gray-200 flex flex-col overflow-y-auto">
      <!-- Toolbar -->
      <div class="flex items-center w-full text-gray-600 bg-gray-100 border-b border-gray-300">
        <button @click="save()" class="px-4 py-2 border-r border-gray-300 hover:bg-gray-300 hover:text-gray-800">
          <i class="fa-solid fa-save mr-1"></i>
          Speichern
        </button>
        <div @mouseleave="exportDropdown=0" @mouseenter="exportDropdown=1" class="px-4 py-2 border-r border-gray-300 hover:cursor-pointer hover:bg-gray-300 hover:text-gray-800">
          <button class="w-full justify-center rounded-md">
            <i class="fa-solid fa-download mr-1"></i>
            Exportieren
          </button>
          <div v-if="exportDropdown" class="absolute z-10 mt-2 -mx-4 w-40 origin-top-right rounded-md bg-gray-100 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
            <div class="py-1" role="none">
              <a @click="store.saveToFile('json')" class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-300 hover:text-gray-900 hover:cursor-pointer">JSON</a>
              <a @click="store.saveToFile('csv')" class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-300 hover:text-gray-900 hover:cursor-pointer">CSV</a>
            </div>
          </div>
        </div>
        <button @click="loadFile()" class="px-4 py-2 border-r border-gray-300 hover:bg-gray-300 hover:text-gray-800">
          <i class="fa-solid fa-upload mr-1"></i>
          Importieren
        </button>
        <button @click="store.deleteData()" class="px-4 py-2 border-r border-gray-300 hover:bg-gray-300 hover:text-gray-800">
          <i class="fa-solid fa-trash mr-1"></i>
          Alles entfernen
        </button>
        <button @click="share()" class="px-4 py-2 border-r border-gray-300 hover:bg-gray-300 hover:text-gray-800">
          <i class="fa-solid fa-share-nodes mr-1"></i>
          Teilen
        </button>

        <div class="flex flex-1"></div>

        <div class="flex h-full w-96">
          <span class="my-auto px-3">
            Variable:
          </span>
          <!-- Var Selector -->
          <div class="relative flex-1">
            <button type="button" @click="varDropdown=!varDropdown" class="relative w-full h-full border-x border-gray-300 bg-gray-50 py-2 pl-3 pr-10 text-left shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 sm:text-sm">
              <span class="flex items-center">
                <span class="ml-1 block truncate">{{ store.displayed_var }}</span>
              </span>
              <span class="pointer-events-none absolute inset-y-0 right-0 ml-3 flex items-center pr-2">
                <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M10 3a.75.75 0 01.55.24l3.25 3.5a.75.75 0 11-1.1 1.02L10 4.852 7.3 7.76a.75.75 0 01-1.1-1.02l3.25-3.5A.75.75 0 0110 3zm-3.76 9.2a.75.75 0 011.06.04l2.7 2.908 2.7-2.908a.75.75 0 111.1 1.02l-3.25 3.5a.75.75 0 01-1.1 0l-3.25-3.5a.75.75 0 01.04-1.06z" clip-rule="evenodd" />
                </svg>
              </span>
            </button>
            <!-- Var Dropdown -->
            <ul v-if="varDropdown"
              class="absolute z-10 mt-1 max-h-56 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
              <li v-for="codes, variable in store.tracking_vars" :key="variable" :class="(variable == store.displayed_var) ? 'text-indigo-600' : ''"
                class="text-gray-900 relative select-none pl-3 pr-9 hover:text-white hover:bg-indigo-600 cursor-pointer"
                @click="store.setDisplayedVar(variable)">
                <div class="flex items-center py-2">
                  <span :class="(variable == store.displayed_var) ? 'font-semibold' : 'font-normal'" class="ml-3 block truncate">{{ variable }}</span>
                </div>
                <span v-if="variable == store.displayed_var" class="absolute inset-y-0 right-0 flex items-center pr-4">
                  <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                  </svg>
                </span>
              </li>
            </ul>
          </div>
          <button @click="store.show_prompt='add'" class="flex px-3 py-2 hover:bg-gray-300 hover:text-gray-800">
            <i class="fa-solid fa-add my-auto"></i>
          </button>
          <button @click="store.show_prompt='change'" class="flex px-3 py-2 hover:bg-gray-300 hover:text-gray-800">
            <i class="fa-solid fa-pen my-auto"></i>
          </button>
          <button @click="store.show_prompt='delete'" class="flex px-3 py-2 hover:bg-gray-300 hover:text-gray-800">
            <i class="fa-solid fa-trash my-auto"></i>
          </button>
        </div>
      </div>
      <!-- Tracked-Items -->
      <div v-if="!loading" class="flex flex-1 overflow-y-scroll pb-5">
        <div v-if="codesInDisplayedVar" class="mx-5 my-2 w-full rounded-lg">
          <button @click="store.show_info=key"
              :class="[(index % 2) ? 'bg-white' : 'bg-gray-50',
                       (index == 0) ? 'rounded-t-lg border-t' : '',
                       (index == codesInDisplayedVar-1) ? 'mb-28 rounded-b-lg border-b' : '',
                       ('loading' in item && !item.loading && item.data.status_code == 0) ? 'bg-green-300' : '',
                       ('loading' in item && !item.loading && item.data.status_code == 1) ? 'bg-yellow-200 from-yellow-200' : '',
                       ('loading' in item && !item.loading && item.data.status_code == 2) ? 'bg-orange-300 from-orange-300' : '',
                       ('loading' in item && !item.loading && item.data.status_code == 3) ? 'bg-red-300 from-red-300' : '',
                       ('loading' in item && !item.loading && (item.edit_code == 1 || item.edit_code == 3)) ? 'bg-gradient-to-r to-green-300' : '']"
              class="px-4 py-5 grid grid-cols-12 gap-4 w-full border-x border-b border-gray-300 hover:brightness-95"
              v-for="(item, key, index) in store.tracking_vars[store.displayed_var]" :key="item.Code">
            <dt class="text-sm font-medium col-span-1 text-left text-gray-500">
              {{ (!('loading' in item) || item.loading) ? key : item.data.code.Code }}
            </dt>
            <dd class="text-sm col-span-10 mt-0 text-left text-gray-900">
              <LoadingAnimation :nomargin="true" :height=24 v-if="!('loading' in item) || item.loading"></LoadingAnimation>
              <span v-if="'loading' in item && !item.loading">{{ item.data.code.Titel}}</span>
            </dd>
            <dd class="text-gray-500 col-span-1 flex flex-row justify-end">
              <button @click="store.deleteCode(key)" @click.stop.prevent="" class="aspect-square h-6 mr-2 text-red-400 hover:text-red-800">
                <i class="fa-solid fa-trash"></i>
              </button>
              <div class="aspect-square h-6 text-blue-400 hover:text-blue-800">
                <i class="fa-solid fa-info"></i>
              </div>
            </dd>
          </button>
        </div>
        <div v-if="!codesInDisplayedVar" class="w-full text-center text-gray-500 pt-5">
          <span>Füge Einträge zum Tracken hinzu.</span>
        </div>
      </div>
      <LoadingAnimation v-if="loading"></LoadingAnimation>
      <!-- Year Selection -->
      <div class="absolute z-10 bg-white border border-gray-300 rounded-t-lg h-24 pt-6 px-9" style="width: 50%; left: 40%; bottom: 0px;">
        <div id="timelineslider" class="w-full relative" :class="(store.available_years.length==0)?'hidden':'block'"></div>
        <LoadingAnimation :nomargin="true" :height=50 v-if="store.available_years.length==0"></LoadingAnimation>
      </div>
    </div>
    <!-- OVERLAYS -->
    <TrackingPrompt></TrackingPrompt>
    <TrackingInfo></TrackingInfo>
    <TrackingShare></TrackingShare>
    <TrackingNotification></TrackingNotification>
  </div>
</template>


<script>
import { store } from '../store'

import axios from 'axios'
import noUiSlider from 'nouislider'

import LoadingAnimation from '@/components/LoadingAnimation.vue'
import TrackingSidebar from '@/components/TrackingSidebar.vue'
import TrackingInfo from '@/components/TrackingInfo.vue'
import TrackingPrompt from '../components/TrackingPrompt.vue'
import TrackingShare from '@/components/TrackingShare.vue'
import TrackingNotification from '@/components/TrackingNotification.vue'

export default {
  data() {
    return {
      store,
      loading: true,
      exportDropdown: 0,
      varDropdown: 0,
    }
  },
  async created() {
    try {
      await axios.get(`/api/icd/version`).then(res => {
        store.available_years = res.data
      })
    } catch (e) {
      console.log(e)
    }
    try {
      if ('sharecode' in this.$route.params) {
        let sharecode = this.$route.params.sharecode
        try {
          await axios.get(`/api/share/code/?code=${sharecode}`).then(async res => {
            let data = JSON.parse(res.data.JSON)
            store.tracking_years = data.tracking_years
            store.tracking_vars = data.tracking_vars
            for (let variable in store.tracking_vars) {
              for (let code in store.tracking_vars[variable]) {
                store.tracking_vars[variable][code].loadedFromFile = true
              }
            }
            store.setDisplayedVar(data.displayed_var)
            store.sendNotification("Daten wurden geladen.")
          })
        } catch (e) {
          store.sendNotification("Ungültiger Share-Code!")
          store.loadFromStorage()
        }
        this.$router.push('/track')
      } else {
        store.loadFromStorage()
      }
    } catch (e) {
      store.setTrackingYears([store.available_years[0].Year, store.available_years[store.available_years.length-1].Year])
      store.setSearchYear(store.available_years[store.available_years.length-1].Year)
      store.tracking_vars["Neue Variable"] = {}
      store.setDisplayedVar("Neue Variable")
    }
    this.createSlider()
    this.loading = false
  },
  methods: {
    loadFile() {
      var input = document.createElement('input')
      input.setAttribute('type', 'file')
      input.setAttribute('accept', '.csv,.json')
      input.onchange = e => {
        var file = e.target.files[0]
        if (!file) {
          return
        }
        var reader = new FileReader()
        let vm = store
        reader.onload = function(e) {
          if (file.type == 'application/json') {
            vm.loadFromFileJSON(vm, e)
          } else if (file.type == 'text/csv') {
            vm.loadFromFileCSV(vm, e)
          }
        }
        reader.readAsText(file)
      }
      input.click()
    },
    save() {
      store.saveToStorage()
      store.sendNotification("Daten gespeichert.")
    },
    async share() {
      let data = JSON.stringify(store.saveToFileJSON())
      try {
        await axios.post(`/api/share/code/`, {"JSON": data}).then(res => {
          store.share_code = this.$baseURL+'/track/'+res.data.Code
        })
      } catch (e) {
        console.log(e)
      }
    },
    /*   TRACKING YEARS   */
    createSlider() {
      var range = document.getElementById('timelineslider');
      var values = []
      store.available_years.forEach((year) => {
        values.push(year.Year)
      })
      var format = {
        to: function(value) {
          return values[Math.round(value)];
        },
        from: function(value) {
          return values.indexOf(Number(value));
        }
      }
      noUiSlider.create(range, {
        start: store.tracking_years,
        range: {'min': 0, 'max': values.length-1},
        step: 1,
        margin: 1,
        connect: true,
        format: format,
        pips: {mode: 'steps', format: format, density: 50}
      });
      range.noUiSlider.on('change', function(values, handle) {
        store.setTrackingYears(values)
      })
    },
    
  },
  computed: {
    codesInDisplayedVar() {
      if (store.displayed_var in store.tracking_vars) {
        return Object.keys(store.tracking_vars[store.displayed_var]).length
      }
      return 0
    }
  },
  components: { LoadingAnimation, TrackingSidebar, TrackingInfo, TrackingPrompt, TrackingShare, TrackingNotification }
}
</script>

<style>
.noUi-pips-horizontal {
  height: auto !important;
}
</style>