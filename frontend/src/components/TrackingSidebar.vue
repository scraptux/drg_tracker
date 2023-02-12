<template>
  <!-- Search Bar -->
  <div class="flex items-center py-2 px-2">
    <div class="relative text-gray-400 mt-2 mx-auto flex-1">
      <input class="bg-gray-300 rounded-md text-sm text-gray-600 h-10 w-full pl-10 focus:outline-none" type="search" name="search" placeholder="Suchen" v-model="searchText" @keyup.enter="search()">
      <button type="submit" class="absolute left-0 top-0 mr-2" @click="search()">
        <svg class="text-gray-500 h-4 w-4 mt-3 ml-3 fill-current" xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="Capa_1" x="0px" y="0px"
          viewBox="0 0 56.966 56.966" style="enable-background:new 0 0 56.966 56.966;" xml:space="preserve"
          width="512px" height="512px">
          <path d="M55.146,51.887L41.588,37.786c3.486-4.144,5.396-9.358,5.396-14.786c0-12.682-10.318-23-23-23s-23,10.318-23,23  s10.318,23,23,23c4.761,0,9.298-1.436,13.177-4.162l13.661,14.208c0.571,0.593,1.339,0.92,2.162,0.92  c0.779,0,1.518-0.297,2.079-0.837C56.255,54.982,56.293,53.08,55.146,51.887z M23.984,6c9.374,0,17,7.626,17,17s-7.626,17-17,17  s-17-7.626-17-17S14.61,6,23.984,6z" />
        </svg>
      </button>
    </div>
    <!-- Year Selection -->
    <div class="relative w-1/6 ml-2 mt-2" v-if="store.available_years.length!=0">
      <button type="button" @click="searchDropdown=!searchDropdown" class="relative w-full h-full border-x border-gray-300 rounded-md bg-gray-50 py-2 pl-3 pr-10 text-left shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 sm:text-sm">
        <span class="flex items-center">
          <span class="ml-1 block truncate">{{ store.search_year }}</span>
        </span>
        <span class="pointer-events-none absolute inset-y-0 right-0 ml-3 flex items-center pr-2">
          <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M10 3a.75.75 0 01.55.24l3.25 3.5a.75.75 0 11-1.1 1.02L10 4.852 7.3 7.76a.75.75 0 01-1.1-1.02l3.25-3.5A.75.75 0 0110 3zm-3.76 9.2a.75.75 0 011.06.04l2.7 2.908 2.7-2.908a.75.75 0 111.1 1.02l-3.25 3.5a.75.75 0 01-1.1 0l-3.25-3.5a.75.75 0 01.04-1.06z" clip-rule="evenodd" />
          </svg>
        </span>
      </button>
      <!-- Dropdown -->
      <ul v-if="searchDropdown"
        class="absolute z-10 mt-1 max-h-56 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
        <li v-for="year in store.available_years.slice().reverse()" :key="year.Year" :class="(year.Year == store.search_year) ? 'text-indigo-600' : ''"
          class="text-gray-900 relative select-none pl-3 pr-9 hover:text-white hover:bg-indigo-600 cursor-pointer"
          @click="store.setSearchYear(year.Year)">
          <div class="flex items-center py-2" v-if="store.tracking_years[0] <= year.Year && year.Year <= store.tracking_years[1]">
            <span :class="(year.Year == store.search_year) ? 'font-semibold' : 'font-normal'" class="ml-2 block truncate">{{ year.Year }}</span>
          </div>
          <span v-if="year.Year == store.search_year" class="absolute inset-y-0 right-0 flex items-center pr-4">
            <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
            </svg>
          </span>
        </li>
      </ul>
    </div>
  </div>
  <!-- Tabs -->
  <div class="border-b border-gray-300">
    <ul class="flex flex-wrap -mb-px">
      <li class="mx-4">
        <button @click="tab(0)" :disabled="results_icd.length <= 0"
          class="inline-block rounded-t-lg py-4 px-2 text-sm font-medium text-center border-transparent border-b-2"
          :class="[(tab_value == 0 && results_icd.length > 0) ? 'text-indigo-600 border-indigo-600' : 'text-gray-400',
                   (tab_value != 0 && results_icd.length > 0) ? 'text-gray-500 hover:text-gray-600 hover:border-gray-300' : 'text-gray-400']"
          type="button">
          ICD-10
        </button>
      </li>
      <li class="mr-4">
        <button @click="tab(1)" :disabled="results_ops.length <= 0"
          class="inline-block rounded-t-lg py-4 px-2 text-sm font-medium text-center border-transparent border-b-2"
          :class="[(tab_value == 1 && results_ops.length > 0) ? 'text-indigo-600 border-indigo-600' : 'text-gray-400',
                   (tab_value != 1 && results_ops.length > 0) ? 'text-gray-500 hover:text-gray-600 hover:border-gray-300' : 'text-gray-400']"
          type="button">
          OPS
        </button>
      </li>
    </ul>
  </div>
  <!-- Search results -->
  <div v-if="loading==0" class="w-full overflow-y-scroll flex flex-col flex-1">
    <div v-if="tab_value == -2" class="text-gray-500 mt-4 mx-auto">
      Bitte die Suchanfrage spezifizieren.
    </div>
    <div v-if="tab_value == -1" class="text-gray-500 mt-4 mx-auto">
      Keine Ergebnisse gefunden.
    </div>
    <div v-if="tab_value == 0" class="bg-white">
      <button @click="add('icd', icd.CodeOhnePunkt)"
        :class="[(index % 2) ? 'bg-white' : 'bg-gray-50',
                 (icd.CodeOhnePunkt in store.tracking_vars[store.displayed_var]) ? 'opacity-50' : 'hover:bg-gray-200']"
        :disabled="icd.CodeOhnePunkt in store.tracking_vars[store.displayed_var]"
        class="px-4 py-5 grid grid-cols-12 gap-4 w-full"
        v-for="(icd, index) in results_icd" :key="icd">
        <dt class="text-sm font-medium col-span-2 text-left text-gray-500" :class="(icd.CodeOhnePunkt in store.tracking_vars[store.displayed_var]) ? 'text-green-500' : ''">{{ icd.Code }}</dt>
        <dd class="text-sm col-span-9 mt-0 text-left text-gray-900" :class="(icd.CodeOhnePunkt in store.tracking_vars[store.displayed_var]) ? 'text-green-600' : ''">{{ icd.Titel }}</dd>
        <dd class="text-gray-500 col-span-1" :class="(icd.CodeOhnePunkt in store.tracking_vars[store.displayed_var]) ? 'text-green-400' : ''">
          <div class="float-right text-medium">
            <i :class="(icd.CodeOhnePunkt in store.tracking_vars[store.displayed_var]) ? 'fa-check': 'fa-plus'" class="fa-solid"></i>
          </div>
        </dd>
      </button>
    </div>
    <div v-if="tab_value == 1">
      <button @click="add('ops', ops.Code)"
        :class="[(index % 2) ? 'bg-white' : 'bg-gray-50',
                 (ops.Code in store.tracking_vars[store.displayed_var]) ? 'opacity-50' : 'hover:bg-gray-200']"
        :disabled="ops.Code in store.tracking_vars[store.displayed_var]"
        class="px-4 py-5 grid grid-cols-12 gap-4 w-full"
        v-for="(ops, index) in results_ops" :key="ops">
        <dt class="text-sm font-medium col-span-2 text-left text-gray-500" :class="(ops.Code in store.tracking_vars[store.displayed_var]) ? 'text-green-500' : ''">{{ ops.Code }}</dt>
        <dd class="text-sm col-span-9 mt-0 text-left text-gray-900" :class="(ops.Code in store.tracking_vars[store.displayed_var]) ? 'text-green-600' : ''">{{ ops.Titel }}</dd>
        <dd class="text-gray-400 col-span-1" :class="(ops.Code in store.tracking_vars[store.displayed_var]) ? 'text-green-400' : ''">
          <div class="float-right text-medium">
            <i :class="(ops.Code in store.tracking_vars[store.displayed_var]) ? 'fa-check': 'fa-plus'" class="fa-solid"></i>
          </div>
        </dd>
      </button>
    </div>
  </div>
  <div v-if="loading!=0" class="flex flex-1 w-full">
    <LoadingAnimation></LoadingAnimation>
  </div>
  <!-- Variable chooser -->
</template>


<script>
import axios from 'axios'
import { store } from '../store'

import LoadingAnimation from '@/components/LoadingAnimation.vue'

export default {
  name: 'TrackingSidebar',
  props: ['available_years'],
  watch: {

  },
  data() {
    return {
      store,
      searchText: "",
      searchDropdown: 0,
      loading: 0,
      tab_value: -1,
      results_icd: [],
      results_ops: [],
    }
  },
  methods: {
    async search() {
      if (this.searchText.length < 3) {
        this.tab_value = -2;
        this.results_icd = [];
        this.results_ops = [];
        return;
      }
      try {
        this.tab_value = -1;
        this.loading = 2;
        this.results_icd = [];
        this.results_ops = [];
        await axios.get(`/api/icd/search/?s=${this.searchText}&year=${store.search_year}`).then(res => {
          this.results_icd = res.data;
          this.loading -= 1;
          if (this.results_icd.length > 0) {
            this.tab_value = 0;
          }
        });
        await axios.get(`/api/ops/search/?s=${this.searchText}&year=${store.search_year}`).then(res => {
          this.results_ops = res.data;
          this.loading -= 1;
          if (this.results_ops.length > 0 && this.tab_value == -1) {
            this.tab_value = 1;
          } 
        })
      } catch (e) {
        console.log(e);
      }
    },
    tab(i) {
      this.tab_value = i;
    },
    add(drg, code) {
      store.addCode(drg, code)
    }
  },
  components: { LoadingAnimation }
}
</script>