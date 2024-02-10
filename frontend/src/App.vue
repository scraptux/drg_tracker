<template>
  <nav class="bg-gray-800">
    <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
      <div class="relative flex h-16 items-center justify-between">
        <!-- Logo + Navigation -->
        <div class="flex items-stretch justify-start">
          <div @click="navDropdown=1" class="lg:hidden px-3 py-2 fill-white">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 my-2 mr-2" viewBox="0 0 50 50"><path d="M 5 8 A 2.0002 2.0002 0 1 0 5 12 L 45 12 A 2.0002 2.0002 0 1 0 45 8 L 5 8 z M 5 23 A 2.0002 2.0002 0 1 0 5 27 L 45 27 A 2.0002 2.0002 0 1 0 45 23 L 5 23 z M 5 38 A 2.0002 2.0002 0 1 0 5 42 L 45 42 A 2.0002 2.0002 0 1 0 45 38 L 5 38 z"></path></svg>
          </div>
          <div v-if="navDropdown" @click="navDropdown=0" class="backdrop-blur-sm fixed w-full h-full z-40">
            <div class="absolute left-0 z-40 mt-2 w-56 origin-top-right rounded-md bg-gray-900 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none" role="menu" aria-orientation="vertical" aria-labelledby="menu-button" tabindex="-1">
              <div class="py-1" role="none">
                <router-link :to="`/icd`" @click="navDropdown=0" class="text-white block px-4 py-2 text-sm" role="menuitem" tabindex="-1" id="menu-item-1">ICD-Code</router-link>
                <router-link :to="`/ops`" @click="navDropdown=0" class="text-white block px-4 py-2 text-sm" role="menuitem" tabindex="-1" id="menu-item-1">OPS-Code</router-link>
              </div>
            </div>
          </div>

          <router-link :to="`/`" class="flex flex-shrink-0 items-center">
            <img class="h-8 w-auto" :src="logoSVG">
          </router-link>
          <div class="ml-6">
            <div class="hidden lg:flex space-x-4">
              <!-- Current: "bg-gray-900 text-white", Default: "text-gray-300 hover:bg-gray-700 hover:text-white" -->
              <router-link :to="`/icd`" :class="($route.path.slice(0,4) === '/icd')?'bg-gray-900 text-white':'text-gray-300 hover:bg-gray-700 hover:text-white'" class="px-3 py-2 rounded-md text-sm font-medium">ICD-Code</router-link>
              <router-link :to="`/ops`" :class="($route.path.slice(0,4) === '/ops')?'bg-gray-900 text-white':'text-gray-300 hover:bg-gray-700 hover:text-white'" class="px-3 py-2 rounded-md text-sm font-medium">OPS-Code</router-link>
              <router-link :to="`/track`" :class="($route.path.slice(0,6) === '/track')?'bg-gray-900 text-white':'text-gray-300 hover:bg-gray-700 hover:text-white'" class="px-3 py-2 rounded-md text-sm font-medium">Code-Tracking</router-link>
            </div>
          </div>
        </div>
        <!-- Search Bar -->
        <div class="absolute inset-y-0 right-0 flex flex-1 items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
          <div class="relative text-gray-400 ml-auto">
            <input class="bg-gray-700 rounded-md text-sm h-10 w-56 sm:w-64 md:w-80 pl-10 focus:outline-none" type="search" name="search" placeholder="Suchen" v-model="searchText" @keyup.enter="search()">
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
      logoSVG: require('./assets/logo.svg'),
      navDropdown: 0
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
