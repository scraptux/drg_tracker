<template>
  <div class="bg-white">
    <div v-if="loading==0 && !error" class="pt-6">
      <NavbarBreadcrumb :drg="$route.params.drg" :year="year" :kapnr="kapitel.KapNr"></NavbarBreadcrumb>

      <div class="mx-auto max-w-7xl space-x-2 px-4 py-5 sm:px-6 lg:px-8">
        <h3 class="text-xl font-medium leading-6 text-gray-900">{{ kapitel.KapNr }} - {{kapitel.KapTi}}</h3>
      </div>
      
      <div class="mx-auto max-w-7xl space-x-2 py-5 sm:px-6 lg:px-3 border-y mb-4 border-gray-200">
        <table class="w-full table-auto">
          <tr @click="router.push(`/${$route.params.drg}/version/${year}/gruppe/${gruppe.GrVon}`)"
              :class="(index % 2) ? 'bg-white' : 'bg-gray-50'"
              class="hover:bg-gray-200 hover:cursor-pointer"
              v-for="(gruppe, index) in gruppen" :key="gruppe.GrVon">
            <td class="py-4 px-6 text-sm text-center my-auto font-medium text-gray-500">{{ gruppe.GrVon }} - {{ gruppe.GrBis }}</td>
            <td class="py-4 w-full text-sm my-auto text-gray-900">{{ gruppe.GrTi }}</td>
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
import axios from 'axios'
import router from '@/router'

import LoadingAnimation from '@/components/LoadingAnimation.vue'
import ErrorMessage from '@/components/ErrorMessage.vue';
import NavbarBreadcrumb from '@/components/NavbarBreadcrumb.vue';

export default {
  data() {
    return {
      router: router,
      year: null,
      kapitel: {},
      gruppen: [],
      loading: 1,
      error: false
    };
  },
  async created() {
    try {
      var drg = this.$route.params.drg;
      var year_param = this.$route.params.year;
      var kapitel_param = this.$route.params.kapitel;
      await axios.get(`/api/${drg}/gruppe/?year=${year_param}&kapitel=${kapitel_param}`).then(res => {
        if (!res.data.year || !Number.isInteger(res.data.year)) {
          throw Error("Year is undefined or not of right type");
        }
        this.year = res.data.year;
        if (res.data.kapitel === undefined || res.data.kapitel.length != 1) {
          throw Error("Kapitel is undefined or not of right type");
        }
        this.kapitel = res.data.kapitel[0];
        if (res.data.gruppen === undefined || res.data.gruppen.length == 0) {
          throw Error("Gruppen is undefined or not of right type");
        }
        this.gruppen = res.data.gruppen;
        this.loading--
      })
    } catch (e) {
      this.error = true;
      console.log(e);
    }
  },
  components: { LoadingAnimation, ErrorMessage, NavbarBreadcrumb }
}
</script>