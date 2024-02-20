<template>
  <nav aria-label="Breadcrumb">
    <ol role="list" class="mx-auto flex items-center space-x-2">
      <li v-if="drg">
        <div v-if="!year && !clickable">
          <p class="text-sm font-medium uppercase text-gray-500">
            <span v-if="drg=='icd'">ICD-10</span>
            <span v-if="drg=='ops'">OPS</span>
          </p>
        </div>
        <div v-if="year || clickable" class="flex items-center">
          <router-link :to="`/${drg}`" class="mr-2 text-sm font-medium text-gray-900">
            <span v-if="drg=='icd'">ICD-10</span>
            <span v-if="drg=='ops'">OPS</span>
          </router-link>
          <svg v-if="year" width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
            <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
          </svg>
        </div>
      </li>
      <li v-if="year">
        <div v-if="!kapnr && !clickable">
          <p class="text-sm font-medium uppercase text-gray-500">{{ year }}</p>
        </div>
        <div v-if="kapnr || clickable" class="flex items-center">
          <router-link :to="`/${drg}/version/${year}`" class="mr-2 text-sm font-medium text-gray-900">
            {{ year }}
          </router-link>
          <svg v-if="kapnr" width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
            <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
          </svg>
        </div>
      </li>
      <li v-if="kapnr">
        <div v-if="!grvon && !clickable">
          <p class="text-sm font-medium uppercase text-gray-500">{{ kapnr }}</p>
        </div>
        <div v-if="grvon || clickable" class="flex items-center">
          <router-link :to="`/${drg}/version/${year}/kapitel/${kapnr}`" class="mr-2 text-sm font-medium text-gray-900">
            {{ kapnr }}
          </router-link>
          <svg v-if="grvon" width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
            <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
          </svg>
        </div>
      </li>
      <li v-if="grvon">
        <div v-if="!(dcode || code) && !clickable">
          <p class="text-sm font-medium uppercase text-gray-500">{{ grvon }}</p>
        </div>
        <div v-if="(dcode || code) || clickable" class="flex items-center">
          <router-link :to="`/${drg}/version/${year}/gruppe/${grvon}`" class="mr-2 text-sm font-medium text-gray-900">
            {{ grvon }}
          </router-link>
          <svg v-if="dcode || code" width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
            <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
          </svg>
        </div>
      </li>
      <li v-if="drg=='ops' && dcode">
        <div v-if="!code && !clickable">
          <p class="text-sm font-medium uppercase text-gray-500">{{ dcode }}</p>
        </div>
        <div v-if="code || clickable" class="flex items-center">
          <router-link :to="`/${drg}/version/${year}/dreisteller/${dcode}`" class="mr-2 text-sm font-medium text-gray-900">
            {{ dcode }}
          </router-link>
          <svg v-if="code" width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
            <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
          </svg>
        </div>
      </li>
      <li v-if="code" class="text-sm">
        <div v-if="!clickable">
          <p class="text-sm font-medium uppercase text-gray-500">{{ code }}</p>
        </div>
        <div v-if="clickable" class="flex items-center">
          <router-link :to="`/${drg}/version/${year}/code/${code.replace('-','').replace('.','')}`" class="mr-2 text-sm font-medium text-gray-900">
            {{ code }}
          </router-link>
        </div>
      </li>
    </ol>
  </nav>
</template>

<script>
export default {
  name: 'NavbarBreadcrumb',
  props: [ 'drg', 'year', 'kapnr', 'grvon', 'dcode', 'code', 'clickable' ]
}
</script>