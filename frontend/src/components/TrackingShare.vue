<template>
  <!-- SHARE POPUP -->
  <div v-if="store.share_code!=''" @click="store.share_code=''" class="fixed flex z-20 w-full h-full bg-black top-0 bg-opacity-50 justify-center items-center">
    <div @click.stop.prevent="" class="flex flex-col bg-white rounded-lg z-20 relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:w-full sm:max-w-lg">
      <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
        <div class="sm:flex sm:items-start">
          <div class="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full sm:mx-0 sm:h-10 sm:w-10 bg-green-100">
            <svg class="w-6 h-6 -ml-1 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path d="M7.217 10.907a2.25 2.25 0 100 2.186m0-2.186c.18.324.283.696.283 1.093s-.103.77-.283 1.093m0-2.186l9.566-5.314m-9.566 7.5l9.566 5.314m0 0a2.25 2.25 0 103.935 2.186 2.25 2.25 0 00-3.935-2.186zm0-12.814a2.25 2.25 0 103.933-2.185 2.25 2.25 0 00-3.933 2.185z" stroke-linecap="round" stroke-linejoin="round"></path>
            </svg>
          </div>
          <div class="mt-3 text-center w-full sm:mt-0 sm:ml-4 sm:text-left">
            <h3 class="text-lg font-medium leading-6 text-gray-900">
              <span>Teilen</span>
            </h3>
            <div class="mt-2 text-sm text-gray-500">
              <p>Sie können die Tracking-Daten mittels folgendem Link weitergeben:</p>
            </div>
            <div class="mt-2 text-sm text-gray-700">
              <p>{{ store.share_code }}</p>
            </div>
          </div>
        </div>
      </div>
      <div class="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
        <button type="button" @click="store.share_code=''" class="inline-flex w-full justify-center rounded-md border border-transparent bg-green-500 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2 sm:ml-3 sm:w-auto sm:text-sm">
          Bestätigen
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { store } from '../store'

export default {
  data() {
    return {
      store
    }
  }
}
</script>