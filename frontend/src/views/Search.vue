<template>
  <div class="bg-white">
    <div v-if="loading==0" class="pt-6">
      <div class="mx-auto max-w-2xl space-x-2 px-4 pb-5 sm:px-6 lg:max-w-7xl lg:px-8">
        <h3 class="text-xl font-medium leading-6 text-gray-900">Suchergebnisse für "<i class="text-gray-600">{{ $route.params.s }}"</i>:</h3>
      </div>
      <div class="mx-auto max-w-2xl space-x-2 px-4 sm:px-6 lg:max-w-7xl lg:px-8">
        <div class="border-b border-gray-200 mb-4">
          <ul class="flex flex-wrap -mb-px">
            <li class="mr-4">
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
      </div>
      <div class="mx-auto max-w-2xl space-x-2 px-4 sm:px-6 lg:max-w-7xl lg:px-8">
        <div v-if="tab_value == -1" class="text-center text-gray-500">
          Keine Ergebnisse gefunden.
        </div>
        <div v-if="tab_value == 0">
          <router-link :to="`/icd/version/${icd.Year}/track/${icd.CodeOhnePunkt}`"
              :class="(index % 2) ? 'bg-white' : 'bg-gray-50'"
              class="px-4 py-5 sm:grid sm:grid-cols-10 sm:gap-4 sm:px-6 hover:bg-gray-200"
              v-for="(icd, index) in results_icd" :key="icd">
            <dt class="text-sm font-medium text-gray-500">{{ icd.Code }}</dt>
            <dd class="mt-1 text-sm sm:col-span-8 sm:mt-0 text-gray-900">{{ icd.Titel }}</dd>
            <dd class="text-gray-500 col-span-1">
              <div class="float-right flex text-sm">
                <span class="pr-2">Track</span>
                <svg class="w-5 h-5 fill-current" width="200px" height="200px" viewBox="-19.04 0 75.804 75.804" xmlns="http://www.w3.org/2000/svg" fill="#000000" stroke="#000000" stroke-width="0"><g transform="translate(-831.568 -384.448)"> <path d="M833.068,460.252a1.5,1.5,0,0,1-1.061-2.561l33.557-33.56a2.53,2.53,0,0,0,0-3.564l-33.557-33.558a1.5,1.5,0,0,1,2.122-2.121l33.556,33.558a5.53,5.53,0,0,1,0,7.807l-33.557,33.56A1.5,1.5,0,0,1,833.068,460.252Z" fill="#000000"></path> </g></svg>
              </div>
            </dd>
          </router-link>
        </div>
        <div v-if="tab_value == 1">
          <router-link :to="`/ops/version/${ops.Year}/track/${ops.Code}`"
              :class="(index % 2) ? 'bg-white' : 'bg-gray-50'"
              class="px-4 py-5 sm:grid sm:grid-cols-10 sm:gap-4 sm:px-6 hover:bg-gray-200"
              v-for="(ops, index) in results_ops" :key="ops">
            <dt class="text-sm font-medium text-gray-500">{{ ops.Code }}</dt>
            <dd class="mt-1 text-sm sm:col-span-8 sm:mt-0 text-gray-900">{{ ops.Titel }}</dd>
            <dd class="text-gray-500 col-span-1">
              <div class="float-right flex text-sm">
                <span class="pr-2">Track</span>
                <svg class="w-5 h-5 fill-current" width="200px" height="200px" viewBox="-19.04 0 75.804 75.804" xmlns="http://www.w3.org/2000/svg" fill="#000000" stroke="#000000" stroke-width="0"><g transform="translate(-831.568 -384.448)"> <path d="M833.068,460.252a1.5,1.5,0,0,1-1.061-2.561l33.557-33.56a2.53,2.53,0,0,0,0-3.564l-33.557-33.558a1.5,1.5,0,0,1,2.122-2.121l33.556,33.558a5.53,5.53,0,0,1,0,7.807l-33.557,33.56A1.5,1.5,0,0,1,833.068,460.252Z" fill="#000000"></path> </g></svg>
              </div>
            </dd>
          </router-link>
        </div>
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
      tab_value: -1,
      loading: 2,
      results_icd: [],
      results_ops: []
    }
  },
  async created() {
    await this.load()
      
    this.$watch(
      async () => this.$route.params,
      (toParams, previousParams) => {
        this.load()
      }
    )
  },
  methods: {
    tab(i) {
      this.tab_value = i;
    },
    async load() {
      try {
        var s = this.$route.params.s;
        this.tab_value = -1;
        this.loading = 2;
        this.results_icd = [];
        this.results_ops = [];
        await axios.get(`/api/icd/search/?s=${s}`).then(res => {
          this.results_icd = res.data;
          this.loading -= 1;
          if (this.results_icd.length > 0) {
            this.tab_value = 0;
          }
        });
        await axios.get(`/api/ops/search/?s=${s}`).then(res => {
          this.results_ops = res.data;
          this.loading -= 1;
          if (this.results_ops.length > 0 && this.tab_value == -1) {
            this.tab_value = 1;
          } 
        })
      } catch (e) {
        console.log(e);
      }
    }
  },
  components: { LoadingAnimation }
}
</script>