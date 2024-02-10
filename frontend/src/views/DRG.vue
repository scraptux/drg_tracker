<template>
  <div class="bg-white">
    <div v-if="loading==0 && !error" class="pt-6">
      <nav aria-label="Breadcrumb">
        <ol role="list" class="mx-auto flex max-w-7xl items-center space-x-2 px-4 sm:px-6 lg:px-8">
          <li class="text-sm">
            <p class="font-medium text-gray-500">
              <span v-if="$route.params.drg=='icd'">ICD-10</span>
              <span v-if="$route.params.drg=='ops'">OPS</span>
            </p>
          </li>
        </ol>
      </nav>

      <div class="mx-auto max-w-7xl space-x-2 px-4 py-5 sm:px-6 lg:px-8">
        <h3 class="text-xl font-medium leading-6 text-gray-900">Versionen</h3>
      </div>
      
      <div class="mx-auto max-w-7xl space-x-2 py-5 sm:px-6 lg:px-3 border-y mb-4 border-gray-200">
        <dl>
          <router-link :to="`/${$route.params.drg}/version/${year}`"
              :class="(index % 2) ? 'bg-white' : 'bg-gray-50'"
              class="py-5 grid grid-cols-10 gap-4 px-6 hover:bg-gray-200"
              v-for="(year, index) in years.slice().reverse()" :key="year">
            <dt class="text-sm my-auto text-center font-medium text-gray-500">{{ $route.params.drg.toUpperCase() }}</dt>
            <dd class="text-sm my-auto text-gray-900 col-span-8">{{ year }}</dd>
            <dd class="my-auto text-gray-500 col-span-1">
              <svg class="float-right w-5 h-5 fill-current" width="200px" height="200px" viewBox="-19.04 0 75.804 75.804" xmlns="http://www.w3.org/2000/svg" fill="#000000" stroke="#000000" stroke-width="0"><g transform="translate(-831.568 -384.448)"> <path d="M833.068,460.252a1.5,1.5,0,0,1-1.061-2.561l33.557-33.56a2.53,2.53,0,0,0,0-3.564l-33.557-33.558a1.5,1.5,0,0,1,2.122-2.121l33.556,33.558a5.53,5.53,0,0,1,0,7.807l-33.557,33.56A1.5,1.5,0,0,1,833.068,460.252Z" fill="#000000"></path> </g></svg>
            </dd>
          </router-link>
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
import ErrorMessage from '@/components/ErrorMessage.vue'

export default {
  data() {
    return {
      years: null,
      loading: 1,
      error: false
    };
  },
  async created() {
    var drg = this.$route.params.drg;
    await axios.get(`/api/${drg}/version/`).then(res => {
      this.years = res.data;
      this.loading--;
    }).catch(err => {
      this.error = true;
      console.log(err)
    });
  },
  components: { LoadingAnimation, ErrorMessage }
}
</script>