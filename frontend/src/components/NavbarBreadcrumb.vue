<template>
  <nav aria-label="Breadcrumb">
    <ol role="list" class="mx-auto flex max-w-7xl items-center space-x-2 px-4 sm:px-6 lg:px-8">
      <li>
        <div v-if="drg && !year">
          <p class="text-sm font-medium uppercase text-gray-500">
            <span v-if="drg=='icd'">ICD-10</span>
            <span v-if="drg=='ops'">OPS</span>
          </p>
        </div>
        <div v-if="drg && year" class="flex items-center">
          <router-link :to="`/${drg}`" class="mr-2 text-sm font-medium text-gray-900">
            <span v-if="drg=='icd'">ICD-10</span>
            <span v-if="drg=='ops'">OPS</span>
          </router-link>
          <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
            <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
          </svg>
        </div>
      </li>
      <li>
        <div v-if="year && !kapnr">
          <p class="text-sm font-medium uppercase text-gray-500">{{ year }}</p>
        </div>
        <div v-if="year && kapnr" class="flex items-center">
          <router-link :to="`/${drg}/version/${year}`" class="mr-2 text-sm font-medium text-gray-900">
            {{ year }}
          </router-link>
          <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
            <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
          </svg>
        </div>
      </li>
      <li>
        <div v-if="kapnr && !grvon">
          <p class="text-sm font-medium uppercase text-gray-500">{{ kapnr }}</p>
        </div>
        <div v-if="kapnr && grvon" class="flex items-center">
          <router-link :to="`/${drg}/version/${year}/kapitel/${kapnr}`" class="mr-2 text-sm font-medium text-gray-900">
            {{ kapnr }}
          </router-link>
          <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
            <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
          </svg>
        </div>
      </li>
      <li>
        <div v-if="grvon && !(dcode || code)">
          <p class="text-sm font-medium uppercase text-gray-500">{{ grvon }}</p>
        </div>
        <div v-if="grvon && (dcode || code)" class="flex items-center">
          <router-link :to="`/${drg}/version/${year}/gruppe/${grvon}`" class="mr-2 text-sm font-medium text-gray-900">
            {{ grvon }}
          </router-link>
          <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
            <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
          </svg>
        </div>
      </li>
      <li>
        <div v-if="dcode && !code">
          <p class="text-sm font-medium uppercase text-gray-500">{{ dcode }}</p>
        </div>
        <div v-if="dcode && code" class="flex items-center">
          <router-link :to="`/${drg}/version/${year}/dreisteller/${dcode}`" class="mr-2 text-sm font-medium text-gray-900">
            {{ dcode }}
          </router-link>
          <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
            <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
          </svg>
        </div>
      </li>
      <li v-if="code" class="text-sm">
        <p class="font-medium text-gray-500">{{ code }}</p>
      </li>
    </ol>
  </nav>
</template>

<script>
export default {
  name: 'NavbarBreadcrumb',
  props: [ 'drg', 'year', 'kapnr', 'grvon', 'dcode', 'code' ]
}
</script>