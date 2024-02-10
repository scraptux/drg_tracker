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
          <li>
            <div class="flex items-center">
              <router-link :to="`/${$route.params.drg}/version/${year}/code/${($route.params.drg == 'ops') ? kode_gruppe.Code : kode_gruppe.CodeOhnePunkt}`"
                class="mr-2 text-sm font-medium text-gray-900">
                {{ kode_gruppe.Code }}
              </router-link>
              <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
                <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
              </svg>
            </div>
          </li>
          <li class="text-sm">
            <p class="font-medium text-gray-500">{{ kode.Code }}</p>
          </li>
        </ol>
      </nav>

      <div class="mx-auto max-w-7xl space-x-2 px-4 py-5 sm:px-6 lg:px-8">
        <h3 class="text-xl font-medium leading-6 text-gray-900">{{ kode.Code }} - {{ kode.Titel }}</h3>
      </div>

      <div class="mx-auto max-w-2xl space-x-2 px-4 pt-5 pb-14 sm:px-6 lg:max-w-7xl lg:px-8 border-y border-gray-200">
        <div id="timelineslider"></div>
      </div>

      <div class="mx-auto max-w-7xl pt-5">
        <TrackingSVG :drg="$route.params.drg" :code="$route.params.code" :year="$route.params.year" :years="years"></TrackingSVG>
      </div>

    </div>
    <LoadingAnimation v-if="loading!=0 && !error"></LoadingAnimation>
    <ErrorMessage v-if="error"></ErrorMessage>
  </div>
</template>

<script>
import axios from 'axios'
import noUiSlider from 'nouislider'

import LoadingAnimation from '@/components/LoadingAnimation.vue'
import TrackingSVG from '@/components/TrackingSVG.vue'
import ErrorMessage from '@/components/ErrorMessage.vue'

export default {
  data() {
    return {
      year: null,
      available_years: [],
      kapitel: {},
      gruppe: {},
      dkode: {},
      kode_gruppe: {},
      kode: {},
      loading: 2,
      error: false,

      years: [],
    };
  },
  async created() {
    try {
      var drg = this.$route.params.drg
      var year_param = this.$route.params.year
      var code_param = this.$route.params.code
      await axios.get(`/api/${drg}/version`).then(res => {
        this.years = [res.data[0], res.data[res.data.length-1]]
        this.available_years = res.data
        this.loading--
      })
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
        this.kode = res.data.kodes[0];
        this.kode_gruppe = {
          'Code': (drg == 'ops') ? this.kode.Code.slice(0,5) : this.kode.Code.slice(0,3)
        };
        if (drg == 'ops') {
          if (res.data.dcode === undefined || res.data.dcode.length != 1) {
            throw Error("DCode is undefined or not of right type");
          }
          this.dkode = res.data.dcode[0];
        } else {
          this.kode_gruppe['CodeOhnePunkt'] = this.kode.CodeOhnePunkt.slice(0,3);
        }
        this.loading--;
      }).then(v => {
        this.createSlider();
      })
    } catch (e) {
      this.error = true;
      console.log(e);
    }
  },
  methods: {
    reloadSVG(years) {
      this.years = years
    },
    createSlider() {
      var range = document.getElementById('timelineslider');
      var values = []
      this.available_years.forEach((year) => {
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
        start: [values[0], values[values.length-1]],
        range: {'min': 0, 'max': values.length-1},
        step: 1,
        margin: 1,
        connect: true,
        format: format,
        pips: {mode: 'steps', format: format, density: 50}
      });
      var reloadSVG = this.reloadSVG
      range.noUiSlider.on('change', function(values, handle) {
        //var start = years.map(e => e.Year).indexOf(values[0]);
        //var stop = years.map(e => e.Year).indexOf(values[1]);
        reloadSVG([values[0], values[1]]);
      })
    }
  },
  components: { LoadingAnimation, TrackingSVG, ErrorMessage }
}
</script>