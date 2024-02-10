<template>
  <div class="bg-white">
    <div v-if="loading==0 && !error" class="pt-6">
      <nav aria-label="Breadcrumb">
        <ol role="list" class="mx-auto flex max-w-7xl items-center space-x-2 px-4 sm:px-6 lg:px-8">
          <li>
            <div class="flex items-center">
              <router-link :to="`/${$route.params.drg}`" class="mr-2 text-sm font-medium text-gray-900">
                <span v-if="$route.params.drg=='icd'">ICD-10</span>
                <span v-if="$route.params.drg=='ops'">OPS</span>
              </router-link>
              <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
                <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
              </svg>
            </div>
          </li>
          <li>
            <div class="flex items-center">
              <router-link :to="`/${$route.params.drg}/version/${year}`" class="mr-2 text-sm font-medium text-gray-900">
                {{ year }}
              </router-link>
              <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
                <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
              </svg>
            </div>
          </li>
          <li>
            <div class="flex items-center">
              <router-link :to="`/${$route.params.drg}/version/${year}/kapitel/${kapitel.KapNr}`" class="mr-2 text-sm font-medium text-gray-900">
                {{ kapitel.KapNr }}
              </router-link>
              <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
                <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
              </svg>
            </div>
          </li>
          <li>
            <div class="flex items-center">
              <router-link :to="`/${$route.params.drg}/version/${year}/gruppe/${gruppe.GrVon}`" class="mr-2 text-sm font-medium text-gray-900">
                {{ gruppe.GrVon }} - {{ gruppe.GrBis }}
              </router-link>
              <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
                <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
              </svg>
            </div>
          </li>
          <li v-if="$route.params.drg == 'ops'">
            <div class="flex items-center">
              <router-link :to="`/${$route.params.drg}/version/${year}/dreisteller/${dkode.DCode}`" class="mr-2 text-sm font-medium text-gray-900">
                {{ dkode.DCode }}
              </router-link>
              <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
                <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
              </svg>
            </div>
          </li>
          <li class="text-sm">
            <p class="font-medium text-gray-500">{{ kode_gruppe.Code }} - {{ kode_gruppe.Titel }}</p>
          </li>
        </ol>
      </nav>

      <div class="mx-auto max-w-7xl space-x-2 px-4 py-5 sm:px-6 lg:px-8 flex space-x-4 grid grid-cols-10">
        <div class="col-span-9">
          <h3 class="text-xl font-medium leading-6 text-gray-900 py-1.5 my-px">
            {{ ($route.params.drg=='icd') ? kode_gruppe.NormCode : kode_gruppe.Code }} - {{ kode_gruppe.Titel }}
          </h3>
        </div>
        <div class="col-span-1">
          <router-link :to="($route.params.drg=='icd')?`/icd/version/${year}/track/${kode_gruppe.CodeOhnePunkt}`:`/ops/version/${year}/track/${kode_gruppe.Code}`"
            class="float-right inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
            Track
          </router-link>
        </div>
      </div>
      
      <div class="mx-auto max-w-7xl space-x-2 py-5 sm:px-6 lg:px-3 border-y mb-4 border-gray-200">
        <dl v-if="kodes.length > 0">
          <router-link :to="($route.params.drg=='icd')?`/icd/version/${year}/track/${kode.CodeOhnePunkt}`:`/ops/version/${year}/track/${kode.Code}`"
              :class="(index % 2) ? 'bg-white' : 'bg-gray-50'"
              class="py-5 grid grid-cols-10 gap-4 px-6 hover:bg-gray-200"
              v-for="(kode, index) in kodes" :key="kode.id">
            <dt :class="(kode.Ebene > ebene_lowest) ? 'text-gray-400 pl-2':'text-gray-500'" class="text-sm my-auto font-medium">{{ kode.Code }}</dt>
            <dd :class="(kode.Ebene > ebene_lowest) ? 'text-gray-500 pl-2':'text-gray-900'" class="text-sm my-auto col-span-8">{{ kode.Titel }}</dd>
            <dd class="my-auto text-gray-500 col-span-1">
              <div class="float-right flex text-sm">
                <span class="pr-2">Track</span>
                <svg class="w-5 h-5 fill-current" width="200px" height="200px" viewBox="-19.04 0 75.804 75.804" xmlns="http://www.w3.org/2000/svg" fill="#000000" stroke="#000000" stroke-width="0"><g transform="translate(-831.568 -384.448)"> <path d="M833.068,460.252a1.5,1.5,0,0,1-1.061-2.561l33.557-33.56a2.53,2.53,0,0,0,0-3.564l-33.557-33.558a1.5,1.5,0,0,1,2.122-2.121l33.556,33.558a5.53,5.53,0,0,1,0,7.807l-33.557,33.56A1.5,1.5,0,0,1,833.068,460.252Z" fill="#000000"></path> </g></svg>
              </div>
            </dd>
          </router-link>
        </dl>
        <dl v-if="kodes.length <= 0" class="text-center text-gray-500">
          Keine Codes gefunden.
        </dl>
      </div>
    </div>
    <LoadingAnimation v-if="loading!=0 && !error"></LoadingAnimation>
    <ErrorMessage v-if="error"></ErrorMessage>
  </div>
</template>

<script>
import axios from 'axios'

import LoadingAnimation from '@/components/LoadingAnimation.vue'
import ErrorMessage from '@/components/ErrorMessage.vue';

export default {
  data() {
    return {
      year: {},
      kapitel: {},
      gruppe: {},
      kode_gruppe: {},
      dkode: {},
      kodes: [],
      ebene_lowest: 5,
      loading: 1,
      error: false
    };
  },
  async created() {
    try {
      var drg = this.$route.params.drg
      this.ebene_lowest = drg == 'icd' ? 4 : 5
      var year_param = this.$route.params.year
      var code_param = this.$route.params.code
      await axios.get(`/api/${drg}/kode/?year=${year_param}&codeexact=${code_param}&codestart=${code_param}`).then(async res => {
        if (!res.data.year || !Number.isInteger(res.data.year)) {
          throw Error("Year is undefined or not of right type");
        }
        this.year = res.data.year;
        if (res.data.kapitel === undefined || res.data.kapitel.length != 1) {
          throw Error("Kapitel is undefined or not of right type");
        }
        this.kapitel = res.data.kapitel[0];
        if (res.data.gruppe === undefined || res.data.gruppe.length != 1) {
          throw Error("Gruppe is undefined or not of right type");
        }
        this.gruppe = res.data.gruppe[0];
        if (res.data.kodes === undefined || res.data.kodes.length == 0) {
          throw Error("Kodes is undefined or not of right type");
        }
        this.kode_gruppe = res.data.kodes[0];
        if (drg == 'ops') {
          if (res.data.dcode === undefined || res.data.dcode.length != 1) {
            throw Error("DCode is undefined or not of right type");
          }
          this.dkode = res.data.dcode[0];
        }
        this.kodes = res.data.kodes_start;
        this.loading--;
      })
    } catch (e) {
      this.error = true;
      console.log(e);
    }
  },
  components: { LoadingAnimation, ErrorMessage }
}
</script>