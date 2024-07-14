<template>
  <div class="bg-white grid grid-cols-10 h-full">
    <!-- SIDEBAR -->
    <div class="flex flex-col col-span-3 bg-gray-100 border-r border-gray-300 h-full max-h-full overflow-y-auto">
      <TrackingSidebar></TrackingSidebar>
    </div>
    <!-- CONTENT -->
    <div class="col-span-7 h-full h-max-full bg-gray-200 flex flex-col overflow-y-auto">
      <!-- Toolbar -->
      <div v-if="store.tracker && !store.tracker.loading" class="flex items-center w-full text-gray-600 bg-gray-100 border-b border-gray-300">
        <div @mouseleave="exportDropdown=0" @mouseenter="exportDropdown=1" class="px-4 py-2 border-r border-gray-300 hover:cursor-pointer hover:bg-gray-300 hover:text-gray-800">
          <button class="w-full justify-center rounded-md">
            <i class="fa-solid fa-download mr-1"></i>
            Exportieren
          </button>
          <div v-if="exportDropdown" class="absolute z-10 mt-2 -mx-4 w-40 origin-top-right rounded-md bg-gray-100 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
            <div class="py-1" role="none">
              <a @click="store.saveToFile('json')" class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-300 hover:text-gray-900 hover:cursor-pointer">JSON</a>
              <!--a @click="store.saveToFile('csv')" class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-300 hover:text-gray-900 hover:cursor-pointer">CSV</a-->
              <a @click="store.saveToFile('sas')" class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-300 hover:text-gray-900 hover:cursor-pointer">SAS</a>
            </div>
          </div>
        </div>
        <button @click="loadFile()" class="px-4 py-2 border-r border-gray-300 hover:bg-gray-300 hover:text-gray-800">
          <i class="fa-solid fa-upload mr-1"></i>
          Importieren
        </button>
        <button @click="reset()" class="px-4 py-2 border-r border-gray-300 hover:bg-gray-300 hover:text-gray-800">
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
                <span class="ml-1 block truncate">{{ store.tracker.displayedVar }}</span>
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
              <li v-for="variable in store.tracker.vars" :key="variable" :class="(variable.name == store.tracker.displayedVar) ? 'text-indigo-600' : ''"
                class="text-gray-900 relative select-none pl-3 pr-9 hover:text-white hover:bg-indigo-600 cursor-pointer"
                @click="setDisplayedVar(variable.name)">
                <div class="flex items-center py-2">
                  <span :class="(variable.name == store.tracker.displayedVar) ? 'font-semibold' : 'font-normal'" class="ml-3 block truncate">{{ variable.name }}</span>
                </div>
                <span v-if="variable.name == store.tracker.displayedVar" class="absolute inset-y-0 right-0 flex items-center pr-4">
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
      <div v-if="store.tracker && !store.tracker.loading" class="flex flex-1 overflow-y-scroll pb-5">
        <div v-if="codesInDisplayedVar" class="mx-5 my-2 w-full rounded-lg">
          <button @click="store.show_info=code.code"
              :class="[(!code.data && index % 2) ? 'bg-white' : 'bg-gray-50',
                       (index == 0) ? 'rounded-t-lg border-t' : '',
                       (index == codesInDisplayedVar-1) ? 'mb-28 rounded-b-lg border-b' : '',
                       (code.data && code.data.code_data.status_code == 0) ? 'bg-green-300' : '',
                       (code.data && code.data.code_data.status_code == 1) ? 'bg-yellow-200 from-yellow-200' : '',
                       (code.data && code.data.code_data.status_code == 2) ? 'bg-orange-300 from-orange-300' : '',
                       (code.data && code.data.code_data.status_code == 3) ? 'bg-red-300 from-red-300' : '',
                       (code.data && (code.data.edit_status == 1 || code.data.edit_status == 3)) ? 'bg-gradient-to-r to-green-300' : '']"
              class="px-4 py-5 grid grid-cols-12 gap-4 w-full border-x border-b border-gray-300 hover:brightness-95"
              v-for="(code, index) in store.tracker.getDisplayedVar().codes" :key="code">
            <dt class="text-sm font-medium col-span-1 text-left text-gray-500">
              {{ !code.data ? code.code : code.data.code_data.code.Code }}
            </dt>
            <dd class="text-sm col-span-10 mt-0 text-left text-gray-900">
              <LoadingAnimation :nomargin="true" :height=24 v-if="!code.data"></LoadingAnimation>
              <span v-if="code.data">{{ code.data.code_data.code.Titel}}</span>
            </dd>
            <dd class="text-gray-500 col-span-1 flex flex-row justify-end">
              <button @click="store.tracker.delCode(code.code)" @click.stop.prevent="" class="aspect-square h-6 mr-2 text-red-400 hover:text-red-800">
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
      <LoadingAnimation v-if="!store.tracker || store.tracker.loading"></LoadingAnimation>
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
    await store.getAvailableYears();
    if ('sharecode' in this.$route.params) {
      let sharecode = this.$route.params.sharecode;
      try {
        await axios.get(`/api/share/code/?code=${sharecode}`).then(res => {
          // TODO check validity
          store.loadFromJson(JSON.parse(res.data.JSON));
        });
      } catch (e) {
        store.sendNotification("Ungültiger Share-Code!");
        console.log(e);
      }
    }

    this.createSlider();
  },
  methods: {
    loadFile() {
      var input = document.createElement('input')
      input.setAttribute('type', 'file')
      input.setAttribute('accept', '.json')
      input.onchange = e => {
        var file = e.target.files[0]
        if (!file) {
          return
        }
        var reader = new FileReader()
        let vm = store
        reader.onload = function(e) {
          if (file.type == 'application/json') {
            vm.loadFromJson(e.target.result)
          }
        }
        reader.readAsText(file)
      }
      input.click()
    },
    reset() {
      store.tracker.clearData(store.available_years[0], store.available_years[store.available_years.length-1]);
      store.tracker.save();
    },
    setDisplayedVar(name) {  // NEW
      store.tracker.setDisplayedVar(name);
      this.varDropdown = 0;
    },
    async share() {
      let data = JSON.stringify(store.saveToJson())
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
        values.push(year)
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
        start: [store.tracker.ystart, store.tracker.ystop],
        range: {'min': 0, 'max': values.length-1},
        step: 1,
        margin: 1,
        connect: true,
        format: format,
        pips: {mode: 'steps', format: format, density: 50}
      });
      range.noUiSlider.on('change', function(values, handle) {
        store.tracker.setYears(values[0], values[1]);
      })
    },
    
  },
  computed: {
    codesInDisplayedVar() {
      return store.tracker.getDisplayedVar().codes.length;
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