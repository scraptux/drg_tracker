<template>
  <div class="bg-white">
    <div v-if="loading==0 && !error" class="pt-6">
      <nav aria-label="Breadcrumb">
        <ol role="list" class="mx-auto flex max-w-7xl items-center space-x-2 px-4 sm:px-6 lg:px-8">
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
              <router-link :to="`/ops/version/${year}`" class="mr-2 text-sm font-medium text-gray-900">
                {{ year }}
              </router-link>
              <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
                <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
              </svg>
            </div>
          </li>
          <li>
            <div class="flex items-center">
              <router-link :to="`/ops/version/${year}/kapitel/${kapitel.KapNr}`" class="mr-2 text-sm font-medium text-gray-900">
                {{ kapitel.KapNr }}
              </router-link>
              <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
                <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
              </svg>
            </div>
          </li>
          <li>
            <div class="flex items-center">
              <router-link :to="`/ops/version/${year}/gruppe/${gruppe.GrVon}`" class="mr-2 text-sm font-medium text-gray-900">
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

      <div class="mx-auto max-w-7xl space-x-2 px-4 py-5 sm:px-6 lg:px-8">
        <h3 class="text-xl font-medium leading-6 text-gray-900">{{ dreisteller.DCode }} - {{ dreisteller.DTi }}</h3>
      </div>
      
      <div class="mx-auto max-w-7xl space-x-2 py-5 sm:px-6 lg:px-3 border-y mb-4 border-gray-200">
        <table class="w-full table-auto">
          <tr @click="router.push(`/ops/version/${year}/code/${kode.Code}`)"
              :class="(index % 2) ? 'bg-white' : 'bg-gray-50'"
              class="hover:bg-gray-200 hover:cursor-pointer"
              v-for="(kode, index) in kodes" :key="kode.id">
            <td class="py-4 px-6 text-sm my-auto font-medium text-gray-500">{{ kode.Code }}</td>
            <td class="py-4 w-full text-sm my-auto text-gray-900">{{ kode.Titel }}</td>
            <td class="py-4 px-6 my-auto text-gray-500">
              <svg class="float-right w-5 h-5 fill-current" width="200px" height="200px" viewBox="-19.04 0 75.804 75.804" xmlns="http://www.w3.org/2000/svg" fill="#000000" stroke="#000000" stroke-width="0"><g transform="translate(-831.568 -384.448)"> <path d="M833.068,460.252a1.5,1.5,0,0,1-1.061-2.561l33.557-33.56a2.53,2.53,0,0,0,0-3.564l-33.557-33.558a1.5,1.5,0,0,1,2.122-2.121l33.556,33.558a5.53,5.53,0,0,1,0,7.807l-33.557,33.56A1.5,1.5,0,0,1,833.068,460.252Z" fill="#000000"></path> </g></svg>
            </td>
          </tr>
        </table>
      </div>
    </div>
    <LoadingAnimation v-if="loading!=0 && !error"></LoadingAnimation>
    <ErrorMessage v-if="error"></ErrorMessage>
  </div>
</template>

<script>
import axios from 'axios';
import router from '@/router';

import LoadingAnimation from '@/components/LoadingAnimation.vue';
import ErrorMessage from '@/components/ErrorMessage.vue';

export default {
  data() {
    return {
      router: router,
      year: {},
      kapitel: {},
      gruppe: {},
      dreisteller: {},
      kodes: [],
      loading: 1,
      error: false
    };
  },
  async created() {
    try {
      var drg = 'ops';
      var year_param = this.$route.params.year
      var dcode_param = this.$route.params.dcode
      await axios.get(`/api/${drg}/kode/?year=${year_param}&dcode=${dcode_param}`).then(async res => {
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
        if (res.data.dcode === undefined || res.data.dcode.length != 1) {
          throw Error("DCode is undefined or not of right type");
        }
        this.dreisteller = res.data.dcode[0];
        if (res.data.kodes === undefined || res.data.kodes.length == 0) {
          throw Error("Kodes is undefined or not of right type");
        }
        this.kodes = res.data.kodes;
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