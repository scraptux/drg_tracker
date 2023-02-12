<template>
  <div class="bg-white">
    <div v-if="loading==0" class="pt-6">
      <nav aria-label="Breadcrumb">
        <ol role="list" class="mx-auto flex max-w-2xl items-center space-x-2 px-4 sm:px-6 lg:max-w-7xl lg:px-8">
          <li>
            <div class="flex items-center">
              <router-link :to="`/ops`" class="mr-2 text-sm font-medium text-gray-900">OPS</router-link>
              <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
                <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
              </svg>
            </div>
          </li>
          <li>
            <div class="flex items-center">
              <router-link :to="`/ops/version/${year.Year}`" class="mr-2 text-sm font-medium text-gray-900">
                {{ year.Year }}
              </router-link>
              <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
                <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
              </svg>
            </div>
          </li>
          <li>
            <div class="flex items-center">
              <router-link :to="`/ops/version/${year.Year}/kapitel/${kapitel.KapNr}`" class="mr-2 text-sm font-medium text-gray-900">
                {{ kapitel.KapNr }}
              </router-link>
              <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
                <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
              </svg>
            </div>
          </li>
          <li>
            <div class="flex items-center">
              <router-link :to="`/ops/version/${year.Year}/gruppe/${gruppe.GrVon}`" class="mr-2 text-sm font-medium text-gray-900">
                {{ gruppe.GrVon }}-{{ gruppe.GrBis }}
              </router-link>
              <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
                <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
              </svg>
            </div>
          </li>
          <li class="text-sm">
            <p class="font-medium text-gray-500">{{ dreisteller.DCode }} - {{ dreisteller.DTi }}</p>
          </li>
        </ol>
      </nav>

      <div class="mx-auto max-w-2xl space-x-2 px-4 py-5 sm:px-6 lg:max-w-7xl lg:px-8">
        <h3 class="text-xl font-medium leading-6 text-gray-900">{{ dreisteller.DCode }} - {{ dreisteller.DTi }}</h3>
        <!-- <p class="mt-1 max-w-2xl text-sm text-gray-500">Personal details and application.</p> -->
      </div>
      
      <div class="mx-auto max-w-2xl space-x-2 px-4 py-5 sm:px-6 lg:max-w-7xl lg:px-3 border-y mb-4 border-gray-200">
        <dl>
          <router-link :to="`/ops/version/${year.Year}/code/${kode.Code}`"
              :class="(index % 2) ? 'bg-white' : 'bg-gray-50'"
              class="px-4 py-5 sm:grid sm:grid-cols-10 sm:gap-4 sm:px-6 hover:bg-gray-200"
              v-for="(kode, index) in kodes" :key="kode.id">
            <dt class="text-sm font-medium text-gray-500">{{ kode.Code }}</dt>
            <dd class="mt-1 text-sm text-gray-900 sm:col-span-8 sm:mt-0">{{ kode.Titel }}</dd>
            <dd class="text-gray-500 col-span-1">
              <svg class="float-right w-5 h-5 fill-current" width="200px" height="200px" viewBox="-19.04 0 75.804 75.804" xmlns="http://www.w3.org/2000/svg" fill="#000000" stroke="#000000" stroke-width="0"><g transform="translate(-831.568 -384.448)"> <path d="M833.068,460.252a1.5,1.5,0,0,1-1.061-2.561l33.557-33.56a2.53,2.53,0,0,0,0-3.564l-33.557-33.558a1.5,1.5,0,0,1,2.122-2.121l33.556,33.558a5.53,5.53,0,0,1,0,7.807l-33.557,33.56A1.5,1.5,0,0,1,833.068,460.252Z" fill="#000000"></path> </g></svg>
            </dd>
          </router-link>
        </dl>
      </div>
    </div>
    <LoadingAnimation v-if="loading!=0"></LoadingAnimation>
  </div>
</template>

<script>
import axios from 'axios'

import LoadingAnimation from '@/components/LoadingAnimation.vue'

export default {
  data() {
    return {
      year: {},
      kapitel: {},
      gruppe: {},
      dreisteller: {},
      kodes: [],
      loading: 5
    };
  },
  async created() {
    try {
      var drg = 'ops';
      var year_param = this.$route.params.year
      var dcode_param = this.$route.params.dcode
      await axios.get(`/api/${drg}/version/${year_param}`).then(res => {
        this.year = res.data
        this.loading--
      })
      await axios.get(`/api/${drg}/kode/?year=${year_param}&dcode=${dcode_param}`).then(async res => {
        this.kodes = res.data
        this.loading--
        await axios.get(`/api/${drg}/dreisteller/?year=${year_param}&did=${this.kodes[0].DCode}`).then(res => {
          this.dreisteller = res.data[0]
          this.loading--
        })
        await axios.get(`/api/${drg}/gruppe/?year=${year_param}&grid=${this.kodes[0].GrVon}`).then(res => {
          this.gruppe = res.data[0]
          this.loading--
        })
        await axios.get(`/api/${drg}/kapitel/?year=${year_param}&kapid=${this.kodes[0].KapNr}`).then(res => {
          this.kapitel = res.data[0]
          this.loading--
        })
      })
    } catch (e) {
      console.log(e);
    }
  },
  components: { LoadingAnimation }
}
</script>