<template>
  <nav class="bg-gray-800">
    <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
      <div class="relative flex h-16 items-center justify-between">
        <!-- Logo + Navigation -->
        <div class="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
          <router-link :to="`/`" class="flex flex-shrink-0 items-center">
            <img class="h-8 w-auto" :src="logoSVG">
          </router-link>
          <div class="ml-6">
            <div class="flex space-x-4">
              <!-- Current: "bg-gray-900 text-white", Default: "text-gray-300 hover:bg-gray-700 hover:text-white" -->
              <router-link :to="`/icd/`" :class="($route.path.slice(0,4) === '/icd')?'bg-gray-900 text-white':'text-gray-300 hover:bg-gray-700 hover:text-white'" class="px-3 py-2 rounded-md text-sm font-medium">ICD-Code</router-link>
              <router-link :to="`/ops/`" :class="($route.path.slice(0,4) === '/ops')?'bg-gray-900 text-white':'text-gray-300 hover:bg-gray-700 hover:text-white'" class="px-3 py-2 rounded-md text-sm font-medium">OPS-Code</router-link>
              <router-link :to="`/track`" :class="($route.path.slice(0,6) === '/track')?'bg-gray-900 text-white':'text-gray-300 hover:bg-gray-700 hover:text-white'" class="px-3 py-2 rounded-md text-sm font-medium">Code-Tracking</router-link>
            </div>
          </div>
        </div>
        <!-- Search Bar -->
        <div class="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
          <div class="relative mx-auto text-gray-400">
            <input class="bg-gray-700 rounded-md text-sm h-10 w-80 pl-10 focus:outline-none" type="search" name="search" placeholder="Suchen" v-model="searchText" @keyup.enter="search()">
            <button type="submit" class="absolute left-0 top-0 mr-2" @click="search()">
              <svg class="text-gray-400 h-4 w-4 mt-3 ml-3 fill-current" xmlns="http://www.w3.org/2000/svg"
                xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="Capa_1" x="0px" y="0px"
                viewBox="0 0 56.966 56.966" style="enable-background:new 0 0 56.966 56.966;" xml:space="preserve"
                width="512px" height="512px">
                <path d="M55.146,51.887L41.588,37.786c3.486-4.144,5.396-9.358,5.396-14.786c0-12.682-10.318-23-23-23s-23,10.318-23,23  s10.318,23,23,23c4.761,0,9.298-1.436,13.177-4.162l13.661,14.208c0.571,0.593,1.339,0.92,2.162,0.92  c0.779,0,1.518-0.297,2.079-0.837C56.255,54.982,56.293,53.08,55.146,51.887z M23.984,6c9.374,0,17,7.626,17,17s-7.626,17-17,17  s-17-7.626-17-17S14.61,6,23.984,6z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>
  
  <router-view></router-view>
</template>

<script>
export default {
  data() {
    return {
      searchText: "",
      logoSVG: require('./assets/logo.svg')
    }
  },
  methods: {
    search() {
      this.$router.push(`/search/${this.searchText}`)
    }
  }
}
</script>

<style>
.position-relative.hover:hover {
  background-color: var(--bs-light);
}
.link {
        fill: none;
        stroke: #ccc;
        stroke-width: 5px;
    }
</style>
