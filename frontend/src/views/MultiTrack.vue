<template>
  <div class="bg-white grid grid-cols-10 h-full">
    <!-- SIDEBAR -->
    <div class="flex flex-col col-span-3 bg-gray-100 border-r border-gray-300 h-full max-h-full overflow-y-auto">
      <!-- Search Bar -->
      <div class="flex items-center py-2 px-2">
        <div class="relative text-gray-400 mt-2 mx-auto flex-1">
          <input class="bg-gray-300 rounded-md text-sm text-gray-600 h-10 w-full pl-10 focus:outline-none" type="search" name="search" placeholder="Suchen" v-model="searchText" @keyup.enter="search()">
          <button type="submit" class="absolute left-0 top-0 mr-2" @click="search()">
            <svg class="text-gray-500 h-4 w-4 mt-3 ml-3 fill-current" xmlns="http://www.w3.org/2000/svg"
              xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="Capa_1" x="0px" y="0px"
              viewBox="0 0 56.966 56.966" style="enable-background:new 0 0 56.966 56.966;" xml:space="preserve"
              width="512px" height="512px">
              <path d="M55.146,51.887L41.588,37.786c3.486-4.144,5.396-9.358,5.396-14.786c0-12.682-10.318-23-23-23s-23,10.318-23,23  s10.318,23,23,23c4.761,0,9.298-1.436,13.177-4.162l13.661,14.208c0.571,0.593,1.339,0.92,2.162,0.92  c0.779,0,1.518-0.297,2.079-0.837C56.255,54.982,56.293,53.08,55.146,51.887z M23.984,6c9.374,0,17,7.626,17,17s-7.626,17-17,17  s-17-7.626-17-17S14.61,6,23.984,6z" />
            </svg>
          </button>
        </div>
        <!-- Year Selection -->
        <div class="relative w-1/6 ml-2 mt-2" v-if="available_years_loaded">
          <button type="button" @click="searchDropdown=!searchDropdown" class="relative w-full h-full border-x border-gray-300 rounded-md bg-gray-50 py-2 pl-3 pr-10 text-left shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 sm:text-sm">
            <span class="flex items-center">
              <span class="ml-1 block truncate">{{ searchYear }}</span>
            </span>
            <span class="pointer-events-none absolute inset-y-0 right-0 ml-3 flex items-center pr-2">
              <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M10 3a.75.75 0 01.55.24l3.25 3.5a.75.75 0 11-1.1 1.02L10 4.852 7.3 7.76a.75.75 0 01-1.1-1.02l3.25-3.5A.75.75 0 0110 3zm-3.76 9.2a.75.75 0 011.06.04l2.7 2.908 2.7-2.908a.75.75 0 111.1 1.02l-3.25 3.5a.75.75 0 01-1.1 0l-3.25-3.5a.75.75 0 01.04-1.06z" clip-rule="evenodd" />
              </svg>
            </span>
          </button>
          <!-- Dropdown -->
          <ul v-if="searchDropdown"
            class="absolute z-10 mt-1 max-h-56 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
            <li v-for="year in available_years.slice().reverse()" :key="year.Year" :class="(year.Year == displayed_var) ? 'text-indigo-600' : ''"
              class="text-gray-900 relative select-none pl-3 pr-9 hover:text-white hover:bg-indigo-600 cursor-pointer"
              @click="searchYear=year.Year">
              <div class="flex items-center py-2" v-if="this.tracking_years[0] <= year.Year && year.Year <= this.tracking_years[1]">
                <span :class="(year.Year == searchYear) ? 'font-semibold' : 'font-normal'" class="ml-2 block truncate">{{ year.Year }}</span>
              </div>
              <span v-if="year.Year == searchYear" class="absolute inset-y-0 right-0 flex items-center pr-4">
                <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                </svg>
              </span>
            </li>
          </ul>
        </div>
      </div>
      <!-- Tabs -->
      <div class="border-b border-gray-300">
        <ul class="flex flex-wrap -mb-px">
          <li class="mx-4">
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
      <!-- Search results -->
      <div v-if="loading==0" class="w-full overflow-y-scroll flex flex-col flex-1">
        <div v-if="tab_value == -2" class="text-gray-500 mt-4 mx-auto">
          Bitte die Suchanfrage spezifizieren.
        </div>
        <div v-if="tab_value == -1" class="text-gray-500 mt-4 mx-auto">
          Keine Ergebnisse gefunden.
        </div>
        <div v-if="tab_value == 0" class="bg-white">
          <button @click="add('icd', icd.CodeOhnePunkt)"
              :class="[(index % 2) ? 'bg-white' : 'bg-gray-50',
                       (icd.CodeOhnePunkt in tracking_items) ? 'opacity-50' : 'hover:bg-gray-200']"
              :disabled="icd.CodeOhnePunkt in tracking_items"
              class="px-4 py-5 grid grid-cols-12 gap-4 w-full"
              v-for="(icd, index) in results_icd" :key="icd">
            <dt class="text-sm font-medium col-span-2 text-left text-gray-500" :class="(icd.CodeOhnePunkt in tracking_items) ? 'text-green-500' : ''">{{ icd.Code }}</dt>
            <dd class="text-sm col-span-9 mt-0 text-left text-gray-900" :class="(icd.CodeOhnePunkt in tracking_items) ? 'text-green-600' : ''">{{ icd.Titel }}</dd>
            <dd class="text-gray-500 col-span-1" :class="(icd.CodeOhnePunkt in tracking_items) ? 'text-green-400' : ''">
              <div class="float-right text-medium">
                <i :class="(icd.CodeOhnePunkt in tracking_items) ? 'fa-check': 'fa-plus'" class="fa-solid"></i>
              </div>
            </dd>
          </button>
        </div>
        <div v-if="tab_value == 1">
          <button @click="add('ops', ops.Code)"
              :class="[(index % 2) ? 'bg-white' : 'bg-gray-50',
                       (ops.Code in tracking_items) ? 'opacity-50' : 'hover:bg-gray-200']"
              :disabled="ops.Code in tracking_items"
              class="px-4 py-5 grid grid-cols-12 gap-4 w-full"
              v-for="(ops, index) in results_ops" :key="ops">
            <dt class="text-sm font-medium col-span-2 text-left text-gray-500" :class="(ops.Code in tracking_items) ? 'text-green-500' : ''">{{ ops.Code }}</dt>
            <dd class="text-sm col-span-9 mt-0 text-left text-gray-900" :class="(ops.Code in tracking_items) ? 'text-green-600' : ''">{{ ops.Titel }}</dd>
            <dd class="text-gray-400 col-span-1" :class="(ops.Code in tracking_items) ? 'text-green-400' : ''">
              <div class="float-right text-medium">
                <i :class="(ops.Code in tracking_items) ? 'fa-check': 'fa-plus'" class="fa-solid"></i>
              </div>
            </dd>
          </button>
        </div>
      </div>
      <div v-if="loading!=0" class="flex flex-1 w-full">
        <LoadingAnimation></LoadingAnimation>
      </div>
      <!-- Variable chooser -->
      
    </div>
    <!-- CONTENT -->
    <div class="col-span-7 h-full h-max-full bg-gray-200 flex flex-col overflow-y-auto">
      <!-- Toolbar -->
      <div class="flex items-center w-full text-gray-600 bg-gray-100 border-b border-gray-300">
        <button @click="save()" class="px-4 py-2 border-r border-gray-300 hover:bg-gray-300 hover:text-gray-800">
          <i class="fa-solid fa-save mr-1"></i>
          Speichern
        </button>
        <div @mouseleave="exportDropdown=0" @mouseenter="exportDropdown=1" class="px-4 py-2 border-r border-gray-300 hover:cursor-pointer hover:bg-gray-300 hover:text-gray-800">
          <button class="w-full justify-center rounded-md">
            <i class="fa-solid fa-download mr-1"></i>
            Exportieren
          </button>
          <div v-if="exportDropdown" class="absolute z-10 mt-2 -mx-4 w-40 origin-top-right rounded-md bg-gray-100 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
            <div class="py-1" role="none">
              <a @click="exportFile('json')" class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-300 hover:text-gray-900 hover:cursor-pointer">JSON</a>
              <a @click="exportFile('csv')" class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-300 hover:text-gray-900 hover:cursor-pointer">CSV</a>
            </div>
          </div>
        </div>
        <button @click="load()" class="px-4 py-2 border-r border-gray-300 hover:bg-gray-300 hover:text-gray-800">
          <i class="fa-solid fa-upload mr-1"></i>
          Importieren
        </button>
        <button @click="delAll()" class="px-4 py-2 border-r border-gray-300 hover:bg-gray-300 hover:text-gray-800">
          <i class="fa-solid fa-trash mr-1"></i>
          Alles entfernen
        </button>
        <button @click="share()" class="px-4 py-2 border-r border-gray-300 hover:bg-gray-300 hover:text-gray-800">
          <i class="fa-solid fa-share-nodes mr-1"></i>
          Teilen
        </button>

        <div class="flex flex-1"></div>

        <div class="flex h-full w-96">
          <span class="my-auto px-3">
            Variable:
          </span>
          <!-- Var Selector -->
          <div class="relative flex-1">
            <button type="button" @click="varDropdown=!varDropdown" class="relative w-full h-full border-x border-gray-300 bg-gray-50 py-2 pl-3 pr-10 text-left shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 sm:text-sm">
              <span class="flex items-center">
                <span class="ml-1 block truncate">{{ displayed_var }}</span>
              </span>
              <span class="pointer-events-none absolute inset-y-0 right-0 ml-3 flex items-center pr-2">
                <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M10 3a.75.75 0 01.55.24l3.25 3.5a.75.75 0 11-1.1 1.02L10 4.852 7.3 7.76a.75.75 0 01-1.1-1.02l3.25-3.5A.75.75 0 0110 3zm-3.76 9.2a.75.75 0 011.06.04l2.7 2.908 2.7-2.908a.75.75 0 111.1 1.02l-3.25 3.5a.75.75 0 01-1.1 0l-3.25-3.5a.75.75 0 01.04-1.06z" clip-rule="evenodd" />
                </svg>
              </span>
            </button>
            <!-- Var Dropdown -->
            <ul v-if="varDropdown"
              class="absolute z-10 mt-1 max-h-56 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
              <li v-for="codes, variable in tracking_vars" :key="variable" :class="(variable == displayed_var) ? 'text-indigo-600' : ''"
                class="text-gray-900 relative select-none pl-3 pr-9 hover:text-white hover:bg-indigo-600 cursor-pointer"
                @click="changeToVar(variable)">
                <div class="flex items-center py-2" v-if="variable != ''">
                  <span :class="(variable == displayed_var) ? 'font-semibold' : 'font-normal'" class="ml-3 block truncate">{{ variable }}</span>
                </div>
                <span v-if="variable == displayed_var" class="absolute inset-y-0 right-0 flex items-center pr-4">
                  <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                  </svg>
                </span>
              </li>
            </ul>
          </div>
          <button @click="addPrompt=1" class="flex px-3 py-2 hover:bg-gray-300 hover:text-gray-800">
            <i class="fa-solid fa-add my-auto"></i>
          </button>
          <button @click="changePrompt=1" class="flex px-3 py-2 hover:bg-gray-300 hover:text-gray-800">
            <i class="fa-solid fa-pen my-auto"></i>
          </button>
          <button @click="deletePrompt=1" class="flex px-3 py-2 hover:bg-gray-300 hover:text-gray-800">
            <i class="fa-solid fa-trash my-auto"></i>
          </button>
        </div>
      </div>
      <!-- Tracked-Items -->
      <div class="flex flex-1 overflow-y-scroll pb-5">
        <div v-if="Object.keys(tracking_items).length!=0" class="mx-5 my-2 w-full rounded-lg">
          <button @click="openInfo(key)"
              :class="[(index % 2) ? 'bg-white' : 'bg-gray-50',
                       (index == 0) ? 'rounded-t-lg border-t' : '',
                       (index == Object.keys(tracking_items).length-1) ? 'mb-28 rounded-b-lg border-b' : '',
                       (!item.loading && item.data.status_code == 0) ? 'bg-green-200 hover:bg-green-100' : '',
                       (!item.loading && (item.edit_code == 1 || item.edit_code == 3)) ? 'bg-green-100 hover:bg-green-50' : '',
                       (!item.loading && item.data.status_code == 1 && (item.edit_code == 0 || item.edit_code == 2)) ? 'bg-yellow-200 hover:bg-yellow-100' : '',
                       (!item.loading && item.data.status_code == 2 && (item.edit_code == 0 || item.edit_code == 2)) ? 'bg-orange-200 hover:bg-orange-100' : '',
                       (!item.loading && item.data.status_code == 3 && (item.edit_code == 0 || item.edit_code == 2)) ? 'bg-red-200 hover:bg-red-100' : '']"
              class="px-4 py-5 grid grid-cols-12 gap-4 w-full border-x border-b border-gray-300"
              v-for="(item, key, index) in tracking_items" :key="item.Code">
            <dt class="text-sm font-medium col-span-1 text-left text-gray-500">
              {{ (item.loading) ? key : item.data.code.Code }}
            </dt>
            <dd class="text-sm col-span-10 mt-0 text-left text-gray-900">
              <LoadingAnimation :nomargin="true" :height=24 v-if="item.loading"></LoadingAnimation>
              <span v-if="!item.loading">{{ item.data.code.Titel }}</span>
            </dd>
            <dd class="text-gray-500 col-span-1 flex flex-row justify-end">
              <button @click="del(key)" @click.stop.prevent="" class="aspect-square h-6 mr-2 text-red-400 hover:text-red-800">
                <i class="fa-solid fa-trash"></i>
              </button>
              <div class="aspect-square h-6 text-blue-400 hover:text-blue-800">
                <i class="fa-solid fa-info"></i>
              </div>
            </dd>
          </button>
        </div>
        <div v-if="Object.keys(tracking_items).length==0" class="w-full text-center text-gray-500 pt-5">
          <span>Füge Einträge zum Tracken hinzu.</span>
        </div>
      </div>
      <!-- Year Selection -->
      <div class="absolute z-10 bg-white border border-gray-300 rounded-t-lg h-24 pt-6 px-9" style="width: 50%; left: 40%; bottom: 0px;">
        <div v-if="available_years_loaded" id="timelineslider" class="w-full relative"></div>
        <LoadingAnimation :nomargin="true" :height=50 v-if="!available_years_loaded"></LoadingAnimation>
      </div>
    </div>
    <!-- PROMPT POPUP -->
    <div v-if="deletePrompt!=0 || changePrompt!=0 || addPrompt!=0" @click="closePrompt()" class="fixed flex z-20 w-full h-full bg-black top-0 bg-opacity-50 justify-center items-center">
      <div @click.stop.prevent="" class="flex flex-col bg-white rounded-lg z-20 relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:w-full sm:max-w-lg">

          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full sm:mx-0 sm:h-10 sm:w-10"
                :class="[(deletePrompt!=0)?'bg-red-100':'',(changePrompt!=0)?'bg-yellow-100':'',(addPrompt!=0)?'bg-green-100':'']">
                <!-- Heroicon name: outline/exclamation-triangle -->
                <svg v-if="deletePrompt!=0" class="h-6 w-6 text-red-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 10.5v3.75m-9.303 3.376C1.83 19.126 2.914 21 4.645 21h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 4.88c-.866-1.501-3.032-1.501-3.898 0L2.697 17.626zM12 17.25h.007v.008H12v-.008z" />
                </svg>
                <svg v-if="changePrompt!=0" class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path>
                </svg>
                <svg v-if="addPrompt!=0" class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                </svg>
              </div>
              <div class="mt-3 text-center w-full sm:mt-0 sm:ml-4 sm:text-left">
                <h3 class="text-lg font-medium leading-6 text-gray-900">
                  <span v-if="deletePrompt!=0">Variable löschen</span>
                  <span v-if="changePrompt!=0">Variable umbenennen</span>
                  <span v-if="addPrompt!=0">Variable hinzufügen</span>
                </h3>
                <div class="mt-2 text-sm text-gray-500">
                  <p v-if="deletePrompt!=0">Wollen Sie wirklich diese Variable löschen? Diese Aktion kann nicht rückgängig gemacht werden.</p>
                  <p v-if="changePrompt!=0">Bitte geben Sie einen neuen Variablennamen an:</p>
                  <p v-if="addPrompt!=0">Bitte wählen Sie einen Namen für die neue Variable aus:</p>
                </div>
                <input v-if="changePrompt!=0 || addPrompt!=0" @keyup.enter="(changePrompt!=0)?changeVarName():addVar()" type="text" placeholder="Variablenname" v-model="promptInput" class="w-full mt-3 px-1 py-0.5 rounded-md border border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm">
                <div v-if="promptError!=''" class="mt-2 text-sm text-red-500">
                  <p>{{ promptError }}</p>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
            <button v-if="deletePrompt!=0" type="button" @click="deleteVar()" class="inline-flex w-full justify-center rounded-md border border-transparent bg-red-600 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 sm:ml-3 sm:w-auto sm:text-sm">
              Löschen
            </button>
            <button v-if="changePrompt!=0" type="button" @click="changeVarName()" class="inline-flex w-full justify-center rounded-md border border-transparent bg-yellow-500 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:ring-offset-2 sm:ml-3 sm:w-auto sm:text-sm">
              Umbenennen
            </button>
            <button v-if="addPrompt!=0" type="button" @click="addVar()" class="inline-flex w-full justify-center rounded-md border border-transparent bg-green-500 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2 sm:ml-3 sm:w-auto sm:text-sm">
              Hinzufügen
            </button>
            <button type="button" @click="closePrompt()" class="mt-3 inline-flex w-full justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-base font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
              Abbrechen
            </button>
          </div>

      </div>
    </div>
    <!-- INFO POPUP -->
    <div v-if="info_key!=''" @click="closeInfo()" class="fixed flex z-20 w-full h-full bg-black top-0 bg-opacity-50 justify-center items-center">
      <div @click.stop.prevent="" class="flex flex-col w-10/12 bg-white rounded-lg z-20" style="max-height: calc( 500% / 6 )">
        <!-- Leave Button -->
        <button @click="closeInfo()"
          class="absolute ml-auto aspect-square h-6 text-gray-600 rounded-full hover:bg-gray-300"
          style="margin-left: calc( (500%/6) - 26px ); margin-top: 2px;">
          <i class="fa-solid fa-x"></i>
        </button>
        <!-- Title -->
        <ol class="pt-4 flex items-center space-x-2 px-6">
          <li>
            <div class="flex items-center">
              <router-link :to="`/${tracking_items[info_key].drg}`" class="mr-2 text-sm font-medium text-gray-900">
                <span v-if="tracking_items[info_key].drg=='icd'">ICD-10</span>
                <span v-if="tracking_items[info_key].drg=='ops'">OPS</span>
              </router-link>
              <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
                <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
              </svg>
            </div>
          </li>
          <li>
            <div class="flex items-center">
              <router-link :to="`/${tracking_items[info_key].drg}/version/${tracking_items[info_key].year}`" class="mr-2 text-sm font-medium text-gray-900">
                {{ tracking_items[info_key].year }}
              </router-link>
              <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
                <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
              </svg>
            </div>
          </li>
          <li>
            <div class="flex items-center">
              <router-link :to="`/${tracking_items[info_key].drg}/version/${tracking_items[info_key].year}/kapitel/${tracking_items[info_key].data.code.KapNr}`" class="mr-2 text-sm font-medium text-gray-900">
                {{ tracking_items[info_key].data.code.KapNr }}
              </router-link>
              <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
                <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
              </svg>
            </div>
          </li>
          <li>
            <div class="flex items-center">
              <router-link :to="`/${tracking_items[info_key].drg}/version/${tracking_items[info_key].year}/gruppe/${tracking_items[info_key].data.code.GrVon}`" class="mr-2 text-sm font-medium text-gray-900">
                {{ tracking_items[info_key].data.code.GrVon }} - {{ tracking_items[info_key].data.code.GrBis }}
              </router-link>
              <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
                <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
              </svg>
            </div>
          </li>
          <li v-if="tracking_items[info_key].drg == 'ops'">
            <div class="flex items-center">
              <router-link :to="`/${tracking_items[info_key].drg}/version/${tracking_items[info_key].year}/dreisteller/${tracking_items[info_key].data.code.DCode}`" class="mr-2 text-sm font-medium text-gray-900">
                {{ tracking_items[info_key].data.code.DCode }}
              </router-link>
              <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
                <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
              </svg>
            </div>
          </li>
          <li>
            <div class="flex items-center">
              <router-link :to="`/${tracking_items[info_key].drg}/version/${tracking_items[info_key].year}/code/${tracking_items[info_key].data.code.GruppeCodeNorm}`" class="mr-2 text-sm font-medium text-gray-900">
                {{ tracking_items[info_key].data.code.GruppeCode }}
              </router-link>
              <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="h-5 w-4 text-gray-300">
                <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
              </svg>
            </div>
          </li>
          <li class="text-sm">
            <p class="font-medium text-gray-500">{{ tracking_items[info_key].data.code.Code }}</p>
          </li>
        </ol>
        <div class="flex flex-row justify-end mx-4 space-x-2 px-2 py-5 border-b border-gray-300">
          <h3 class="text-xl flex-1 font-medium leading-6 text-gray-900">{{ tracking_items[info_key].data.code.Code }} - {{ tracking_items[info_key].data.code.Titel }}</h3>
          <!-- <p class="mt-1 max-w-2xl text-sm text-gray-500">Personal details and application.</p> -->
          <button @click="tracking_items[info_key].edit_code=2"
            v-if="tracking_items[info_key].data.status_code!=0 && tracking_items[info_key].edit_code<=1"
            height="38px" class="flex self-end justify-center rounded-md border border-transparent bg-yellow-500 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:ring-offset-2">
            <span class="pr-2">Bearbeiten</span>
            <i class="fa-solid fa-pen text-sm"></i>
          </button>

          <button @click="tracking_items[info_key].edit_code=0"
            v-if="tracking_items[info_key].data.status_code!=0 && tracking_items[info_key].edit_code>=2"
            height="38px" class="flex self-end justify-center rounded-md border border-transparent bg-red-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2">
            <span class="pr-2">Abbrechen</span>
            <i class="fa-solid fa-x text-sm"></i>
          </button>
          <button @click="tracking_items[info_key].edit_code=3"
            v-if="tracking_items[info_key].data.status_code!=0 && tracking_items[info_key].edit_code==2"
            height="38px" class="flex self-end justify-center rounded-md border border-transparent bg-green-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2">
            <span class="pr-2">Speichern</span>
            <i class="fa-solid fa-check text-sm"></i>
          </button>

          <button @click="tracking_items[info_key].edit_code=1"
            v-if="tracking_items[info_key].data.status_code!=0 && tracking_items[info_key].edit_code==0"
            height="38px" class="flex self-end justify-center rounded-md border border-transparent bg-green-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2">
            <span class="pr-2">Ohne Änderung übernehmen</span>
            <i class="fa-solid fa-check text-sm"></i>
          </button>

          <span v-if="tracking_items[info_key].edit_code==3" class="flex self-end justify-center rounded-md border border-green-500 py-2 px-4 text-sm font-medium text-green-500 shadow-sm">
            <span class="pr-2">Gespeichert</span>
            <i class="fa-solid fa-check text-sm"></i>
          </span>
          <span v-if="tracking_items[info_key].edit_code==1" class="flex self-end justify-center rounded-md border border-green-500 py-2 px-4 text-sm font-medium text-green-500 shadow-sm">
            <span class="pr-2">Ohne Änderung übernommen</span>
            <i class="fa-solid fa-check text-sm"></i>
          </span>
          <span v-if="tracking_items[info_key].data.status_code==0" class="flex self-end justify-center rounded-md border border-green-500 py-1 px-2 text-sm font-medium text-green-500 shadow-sm">
            Keine Probleme gefunden
          </span>
        </div>
        <!-- Info Content -->
        <div class="flex-1 py-4 overflow-y-scroll">
          <!-- Code Editing -->
          <div v-if="tracking_items[info_key].edit_code>=2 && tracking_items[info_key].edit_data.length!=0" class="mx-4 px-2 pb-5 border-b border-gray-300">
            <span class="text-sm font-medium">Codes zum Einbeziehen auswählen:</span>
            <table class="table w-full mt-2 text-center">
              <tbody>
                <tr class="bg-gray-200 border-b border-gray-300">
                  <td></td>
                  <td v-for="val, year in tracking_items[info_key].edit_data" :key="val" class="py-2 border-l border-gray-300">
                    <span>{{ year }}</span>
                  </td>
                </tr>
                <tr v-for="code, idx in tracking_items[info_key].data.codes" :key="idx" class="border-b border-gray-300">
                  <td class="text-left w-16 py-2 border-r border-gray-300">{{ code }}</td>
                  <td v-for="year in tracking_items[info_key].edit_data" :key="year" class="border-l border-gray-300" :class="(year[code].checked)?'bg-green-400':'bg-red-400'" @click="year[code].checked=!year[code].checked;tracking_items[info_key].data.edit_code=2">
                    <i v-if="year[code].checked" class="fa-solid fa-check text-lg"></i>
                    <i v-if="!year[code].checked" class="fa-solid fa-x text-sm"></i>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <LoadingAnimation v-if="tracking_items[info_key].edit_data.length==0"></LoadingAnimation>
          <!-- Info SVG -->
          <TrackingSVG class="pt-4" :drg="tracking_items[info_key].drg" :code="(tracking_items[info_key].drg == 'ops') ? tracking_items[info_key].data.code.Code : tracking_items[info_key].data.code.CodeOhnePunkt" :years="tracking_years" :year="tracking_items[info_key].year"></TrackingSVG>
        </div>
      </div>
    </div>
    <!-- SHARE POPUP -->
    <div v-if="shareCode!=''" @click="shareCode=''" class="fixed flex z-20 w-full h-full bg-black top-0 bg-opacity-50 justify-center items-center">
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
                  <p>{{ shareCode }}</p>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
            <button type="button" @click="shareCode=''" class="inline-flex w-full justify-center rounded-md border border-transparent bg-green-500 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2 sm:ml-3 sm:w-auto sm:text-sm">
              Bestätigen
            </button>
          </div>

      </div>
    </div>
    <!-- NOTIFICATION POPUP -->
    <div v-if="alertShown!=0" @click="alertShown=0" class="fixed z-20 mt-4 flex flex-row place-items-center fade show right-0 mr-4 alert bg-blue-200 rounded-lg py-3 px-10 text-base text-blue-800 inline-flex items-center border border-blue-300 alert-dismissible hover:cursor-pointer">
      <p class="w-full text-center">{{ alertText }}</p>
    </div>
    <!--<LoadingAnimation v-if="loading!=0"></LoadingAnimation>-->
  </div>
</template>


<script>
import axios from 'axios'
import noUiSlider from 'nouislider'

import LoadingAnimation from '@/components/LoadingAnimation.vue'
import TrackingSVG from '@/components/TrackingSVG.vue'
import router from '@/router'

export default {
  data() {
    return {
      tab_value: -1,
      loading: 0,
      loadingFile: false,
      results_icd: [],
      results_ops: [],
      searchText: "",
      searchDropdown: 0,
      searchYear: "",
      available_years_loaded: false,
      available_years: [],
      tracking_years: [],
      tracking_vars: {},
      exportDropdown: 0,
      displayed_var: "",
      varDropdown: 0,
      tracking_items: {},
      info_key: "",
      deletePrompt: 0,
      changePrompt: 0,
      addPrompt: 0,
      promptInput: "",
      promptError: "",
      shareCode: "",
      alertText: "",
      alertShown: 0
    }
  },
  watch: {
    // CALL NEW RESULTS FOR TRACKER (CLEAR GRAPH-INFO)
    tracking_years: {
      handler: function(newYears, oldYears) {
        if (newYears == oldYears || oldYears.length == 0) {
          return
        }
        for (let vars in this.tracking_vars) {
          for (let item in this.tracking_vars[vars]) {
            this.tracking_vars[vars][item].loading = true
            delete this.tracking_vars[vars][item].data
            if (!this.loadingFile) {
              this.tracking_vars[vars][item].edit_code = 0
              this.tracking_vars[vars][item].edit_data = {}
            }
          }
        }
        for (let item in this.tracking_items) {
          this.tracking_items[item].loading = true
          delete this.tracking_items[item].data
          if (!this.loadingFile) {
            this.tracking_items[item].edit_code = 0
            this.tracking_items[item].edit_data = {}
          }
          this.loadTrackingInfo(this.tracking_items[item].drg, item)
        }
        if (!(newYears[0] <= this.searchYear && this.searchYear <= newYears[1])) {
          this.searchYear = newYears[1]
        }
        localStorage.tracking_years = JSON.stringify(newYears)
        localStorage.tracking_vars = JSON.stringify(this.tracking_vars)
      },
      deep: true
    },
    /*tracking_vars: {
      handler: function(newVars, oldVars) {
        localStorage.tracking_vars = JSON.stringify(newVars)
      },
      deep: true
    },*/
    displayed_var: {
      handler: function(newVar, oldVar) {
        localStorage.tracking_displayed_var = newVar
        this.loadingFile = false
      }
    }
  },
  async created() {
    let error = 0
    if ('sharecode' in this.$route.params) {
      let sharecode = this.$route.params.sharecode
      await axios.get(`${this.$baseURL}/api/share/code/?code=${sharecode}`).then(async res => {
        let data = JSON.parse(res.data.JSON)
        this.tracking_years = data.tracking_years
        this.searchYear = data.tracking_years[1]
        this.tracking_vars = data.tracking_vars
        //this.tracking_displayed_var = data.tracking_displayed_var
        //this.tracking_items = this.tracking_vars[this.tracking_displayed_var]
        this.changeToVar(data.tracking_displayed_var)
        await axios.get(`${this.$baseURL}/api/icd/version`).then(res => {
          this.available_years = res.data
          this.available_years_loaded = true
        })
        this.createSlider()
      }).catch(err => {
        //console.log(err)
        error = 1
        //alert("Ungültiger Share-Code!")
        //this.$route.params.sharecode = undefined
        //this.$router.go('/track/')
        //delete this.$route.params.sharecode
        //this.$router.push('/track')
        //this.$forceUpdate()
      })
    }
    if (error == 1) {
      this.$router.push('/track')
      this.showAlert("Ungültiger Share-Code!")
    } else if (error == 0 && 'sharecode' in this.$route.params) {
      return
    }
    if (localStorage.getItem("tracking_vars") === null) {
      this.displayed_var = "Neue Variable"
      this.tracking_vars["Neue Variable"] = {}
    } else {
      //console.log("HIhihia")
      //this.tracking_vars = Object.fromEntries(Object.entries(JSON.parse(localStorage.tracking_vars)).filter(([k, v]) => Object.keys(v).length != 0))
      this.tracking_vars = JSON.parse(localStorage.tracking_vars)
      //this.displayed_var = localStorage.tracking_displayed_var
      this.changeToVar(localStorage.tracking_displayed_var)
    }
    if (localStorage.getItem("tracking_years") === null) {
      this.tracking_years = [2005, 2023]
      this.searchYear = 2023
    } else {
      this.tracking_years = JSON.parse(localStorage.tracking_years)
      this.searchYear = JSON.parse(localStorage.tracking_years)[1]
    }
    await axios.get(`${this.$baseURL}/api/icd/version`).then(res => {
      this.available_years = res.data
      this.available_years_loaded = true
    })
    this.createSlider()
    
    
    /*this.searchText = "ECMO"
    this.search()*/
  },
  methods: {
    async showAlert(s) {
      this.alertText = s
      this.alertShown += 1
      await new Promise(resolve => setTimeout(resolve, 3000))
      this.alertShown -= 1
    },
    /*    INFO POPUP    */
    closeInfo() {
      this.info_key = ""
      this.tracking_vars[this.displayed_var] = this.tracking_items
      localStorage.tracking_vars = JSON.stringify(this.tracking_vars)
      //this.info_code = {}
    },
    async openInfo(code) {
      this.info_key = code
      if (Object.keys(this.tracking_items[code].edit_data).length != 0) {
        return
      }
      await axios.get(`${this.$baseURL}/api/${this.tracking_items[code].drg}/track/?year_start=${this.tracking_years[0]}&year_stop=${this.tracking_years[1]}&year=${this.tracking_items[code].year}&code=${code}&get_nodes=1`).then(res => {
        this.available_years.forEach((year) => {
          if (this.tracking_years[0] <= year.Year && year.Year <= this.tracking_years[1]) {
            if (!(year.Year in this.tracking_items[code].edit_data)) {
              this.tracking_items[code].edit_data[year.Year] = {}
              //this.tracking_items[code].edit_data[year.Year][code] = {'Code': code, 'checked': true}
            }
            //console.log(res.data)
            for (let c of res.data) {
              //console.log(c)
              if ('edit_data_imported' in this.tracking_items[code] && c in this.tracking_items[code].edit_data_imported[year.Year]) {
                this.tracking_items[code].edit_data[year.Year][c] = this.tracking_items[code].edit_data_imported[year.Year][c]
              } else {
                this.tracking_items[code].edit_data[year.Year][c] = {'Code': c, 'checked': false}
              }
            }
          }
        })
        this.tracking_items[code].data.codes = res.data

        if (this.tracking_items[code].data.code.Code in this.tracking_items[code].edit_data[this.tracking_years[0]]) {
          this.available_years.forEach((year) => {
            if (this.tracking_years[0] <= year.Year && year.Year <= this.tracking_years[1]) {
              this.tracking_items[code].edit_data[year.Year][this.tracking_items[code].data.code.Code].checked = true
            }
          })
        } else if (this.tracking_items[code].data.code.Code.replace('-','') in this.tracking_items[code].edit_data[this.tracking_years[0]]) {
          this.available_years.forEach((year) => {
            if (this.tracking_years[0] <= year.Year && year.Year <= this.tracking_years[1]) {
              this.tracking_items[code].edit_data[year.Year][this.tracking_items[code].data.code.Code.replace('-','')].checked = true
            }
          })
        } else if (this.tracking_items[code].data.code.Code.replace('-','').replace('.','') in this.tracking_items[code].edit_data[this.tracking_years[0]]) {
          this.available_years.forEach((year) => {
            if (this.tracking_years[0] <= year.Year && year.Year <= this.tracking_years[1]) {
              this.tracking_items[code].edit_data[year.Year][this.tracking_items[code].data.code.Code.replace('-','').replace('.','')].checked = true
            }
          })
        } else {
          this.available_years.forEach((year) => {
            if (this.tracking_years[0] <= year.Year && year.Year <= this.tracking_years[1]) {
              this.tracking_items[code].edit_data[year.Year][this.tracking_items[code].data.code.Code] = {'Code': this.tracking_items[code].data.code.Code, 'checked': true}
            }
          })
          this.tracking_items[code].data.codes.unshift(this.tracking_items[code].data.code.Code)
        }
      })
    },
    /*    VAR SELECTION    */
    addVar() {
      //let varname = prompt("Wie soll die neue Variable genannt werden?")
      if (this.promptInput === '') {
        this.promptError = "Bitte einen gültigen Namen wählen."
        return
      } else if (Object.prototype.hasOwnProperty.call(this.tracking_vars, this.promptInput)) {
        this.promptError = "Dieser Name ist bereits vergeben."
        return
      }
      this.tracking_vars[this.promptInput] = {}
      let unsorted = this.tracking_vars
      this.tracking_vars = Object.keys(unsorted).sort().reduce(function(v, i) {
        v[i] = unsorted[i]
        return v
      }, {})
      this.changeToVar(this.promptInput)
      this.closePrompt()
    },
    changeVarName() {
      //let varname = prompt("In was soll die Variable umbenannt werden?")
      if (this.promptInput === '') {
        this.promptError = "Bitte einen gültigen Namen wählen."
        return
      } else if (Object.prototype.hasOwnProperty.call(this.tracking_vars, this.promptInput)) {
        this.promptError = "Dieser Name ist bereits vergeben."
        return
      }
      //if (varname != this.displayed_var) {
      this.tracking_vars[this.promptInput] = this.tracking_vars[this.displayed_var]
      let unsorted = this.tracking_vars
      this.tracking_vars = Object.keys(unsorted).sort().reduce(function(v, i) {
        v[i] = unsorted[i]
        return v
      }, {})
      let old_varname = this.displayed_var
      this.displayed_var = this.promptInput
      this.closePrompt()
      delete this.tracking_vars[old_varname]
      localStorage.tracking_vars = JSON.stringify(this.tracking_vars)
      //}
    },
    changeToVar(name) {
      this.tracking_vars[this.displayed_var] = this.tracking_items
      this.displayed_var = name
      this.tracking_items = this.tracking_vars[name]
      localStorage.tracking_vars = JSON.stringify(this.tracking_vars)
      for (let item in this.tracking_items) {
        if (!this.tracking_items[item].loading) {
          continue
        }
        this.tracking_items[item].loading = true
        delete this.tracking_items[item].data
        this.loadTrackingInfo(this.tracking_items[item].drg, item)
      }
    },
    closePrompt() {
      this.deletePrompt = 0
      this.changePrompt = 0
      this.addPrompt = 0
      this.promptError = ""
      this.promptInput = ""
    },
    deleteVar() {
      //if (confirm("Soll die Variable wirklich gelöscht werden?")) {
      let old_varname = this.displayed_var
      let new_var = ""
      for (var key in this.tracking_vars) {
        if (key != old_varname && key != '') {
          new_var = key
          this.changeToVar(key)
          break
        }
      }
      if (new_var == "") {
        this.tracking_vars["Neue Variable"] = {}
        this.changeToVar("Neue Variable")
        this.closePrompt()
        return
      }
      this.closePrompt()
      delete this.tracking_vars[old_varname]
      //}
    },
    /*    TRACKING    */
    add(drg, code) {
      this.tracking_items[code] = {'drg': drg, 'loading': true, 'year': this.searchYear}
      let unsorted = this.tracking_items
      this.tracking_items = Object.keys(unsorted).sort().reduce(function(v, i) {
        v[i] = unsorted[i]
        return v
      }, {})
      this.loadTrackingInfo(drg, code)
      this.tracking_vars[this.displayed_var] = this.tracking_items
      localStorage.tracking_vars = JSON.stringify(this.tracking_vars)
    },
    del(code) {
      delete this.tracking_items[code]
      delete this.tracking_vars[this.displayed_var][code]
      localStorage.tracking_vars = JSON.stringify(this.tracking_vars)
    },
    delAll() {
      this.changeToVar("")
      //this.displayed_var = ""
      this.tracking_items = {}
      this.tracking_vars = {}
      this.tracking_vars["Neue Variable"] = {}
      this.changeToVar("Neue Variable")
      this.showAlert("Alles gelöscht.")
    },
    exportFile(format) {
      // edit all unclear var-items
      /*for (let vars in this.tracking_vars) {
        if (vars == '') {
          continue
        }
        this.changeToVar(vars)
        for (let item in this.tracking_vars[vars]) {
          //console.log(this.tracking_vars[vars][item].data.status_code)
          if (!('data' in this.tracking_vars[vars][item]) || (this.tracking_vars[vars][item].data.status_code != 0 && this.tracking_vars[vars][item].edit_code == 0)) {
            this.showAlert("Bitte erst problematische Variablen bearbeiten!")
            return
          }
        }
      }*/
      // download file
      let data = null
      let blob = null
      if (format == 'json') {
        data = this.exportFileJSON()
        blob = new Blob([JSON.stringify(data)], {type: "application/json;charset=utf-8"})
      } else if (format == 'csv') {
        data = this.exportFileCSV()
        blob = new Blob([data], {type: "text/csv;charset=utf-8"})
      } else {
        return
      }
      const url = URL.createObjectURL(blob)
      const elem = document.createElement("a")
      elem.setAttribute('href', url)
      elem.setAttribute('download', 'drg_tracking.'+format)
      document.body.appendChild(elem)
      elem.click()
      document.body.removeChild(elem)
    },
    exportFileCSV() {
      // var;code;drg;added_year;year;edit_code;edit_data
      let data = []
      for (let vars in this.tracking_vars) {
        if (vars == '') {
          continue
        }
        for (let item in this.tracking_vars[vars]) {
          this.available_years.forEach((year) => {
            if (this.tracking_years[0] <= year.Year && year.Year <= this.tracking_years[1]) {
              if (!('edit_code' in this.tracking_vars[vars][item])) {
                data.push([vars, item, this.tracking_vars[vars][item].drg, this.tracking_vars[vars][item].year, year.Year, 0, ""])
              } else if (this.tracking_vars[vars][item].edit_code != 0) {
                let edit_data = ""
                for (let edit_item in this.tracking_vars[vars][item].edit_data[year.Year]) {
                  if (this.tracking_vars[vars][item].edit_data[year.Year][edit_item].checked) {
                    edit_data += edit_item+","
                  }
                }
                data.push([vars, item, this.tracking_vars[vars][item].drg, this.tracking_vars[vars][item].year, year.Year, this.tracking_vars[vars][item].edit_code, edit_data.substring(0, edit_data.length-1)])
              } else {
                data.push([vars, item, this.tracking_vars[vars][item].drg, this.tracking_vars[vars][item].year, year.Year, this.tracking_vars[vars][item].edit_code, ""])
              }
            }
          })
        }
      }
      let res = ""
      data.forEach(function(row) {
        res += row.join(";")+"\r\n"
      })
      return res
    },
    exportFileJSON() {
      var data = {'tracking_years': this.tracking_years, 'tracking_displayed_var': this.displayed_var}
      let tmp = {}
      for (let vars in this.tracking_vars) {
        if (vars == '') {
          continue
        }
        tmp[vars] = {}
        for (let item in this.tracking_vars[vars]) {
          tmp[vars][item] = {
            'drg': this.tracking_vars[vars][item].drg,
            'year': this.tracking_vars[vars][item].year,
            'edit_code': this.tracking_vars[vars][item].edit_code,
            'edit_data': this.tracking_vars[vars][item].edit_data,
            'loading': true}
        }
      }
      data.tracking_vars = tmp
      return data
    },
    load() {
      var input = document.createElement('input')
      input.setAttribute('type', 'file')
      input.onchange = e => {
        var file = e.target.files[0]
        if (!file) {
          return
        }
        var reader = new FileReader()
        let loadHandlerJSON = this.loadHandlerJSON
        let loadHandlerCSV = this.loadHandlerCSV
        let showAlert = this.showAlert
        reader.onload = function(e) {
          if (file.type == 'application/json') {
            loadHandlerJSON(e)
          } else if (file.type == 'text/csv') {
            loadHandlerCSV(e)
          }
          //loadHandler(e)
          showAlert("Datei importiert.")
        }
        reader.readAsText(file)
      }
      input.click()
    },
    loadHandlerCSV(e) {
      // var;code;drg;added_year;year;edit_code;edit_data
      let used_years = []
      var content_lines = e.target.result.split("\r\n")
      // tracking_years
      for (let idx_lines = 0; idx_lines < content_lines.length; idx_lines++) {
        if (content_lines[idx_lines] == '') {
          continue
        }
        let content_cells = content_lines[idx_lines].split(";")
        if (!(content_cells[4] in used_years)) {
          used_years.push(content_cells[4])
        } else {
          break
        }
      }
      // handle tracking_years
      this.tracking_years = []
      this.tracking_years.push(Math.min.apply(Math, used_years))
      this.tracking_years.push(Math.max.apply(Math, used_years))
      // tracking_vars
      this.changeToVar("")
      this.tracking_items = {}
      this.tracking_vars = {}
      for (let idx_lines = 0; idx_lines < content_lines.length; idx_lines++) {
        if (content_lines[idx_lines] == '') {
          continue
        }
        let content_cells = content_lines[idx_lines].split(";")
        if (!(content_cells[0] in this.tracking_vars)) {
          this.tracking_vars[content_cells[0]] = {}
        }
        if (!(content_cells[1] in this.tracking_vars[content_cells[0]])) {
          this.tracking_vars[content_cells[0]][content_cells[1]] = {}
        }
        this.tracking_vars[content_cells[0]][content_cells[1]].drg = content_cells[2]
        this.tracking_vars[content_cells[0]][content_cells[1]].year = content_cells[3]
        this.tracking_vars[content_cells[0]][content_cells[1]].edit_code = content_cells[5]
        if (!('edit_data_imported' in this.tracking_vars[content_cells[0]][content_cells[1]])) {
          this.tracking_vars[content_cells[0]][content_cells[1]].edit_data_imported = {}
        }
        if (!(content_cells[4] in this.tracking_vars[content_cells[0]][content_cells[1]].edit_data_imported)) {
          this.tracking_vars[content_cells[0]][content_cells[1]].edit_data_imported[content_cells[4]] = {}
        }
        var edit_items = content_cells[6].split("")
        for (var idx_item = 0; idx_item < edit_items; idx_item++) {
          this.tracking_vars[content_cells[0]][content_cells[1]].edit_data_imported[content_cells[4]][edit_items[idx_item]] = {'Code': edit_items[idx_item], 'checked': true}
        }
        this.tracking_vars[content_cells[0]][content_cells[1]].loading = true
      }
      // displayed_var
      var display_var = ""
      for (var key in this.tracking_vars) {
        if (key != '') {
          this.changeToVar(key)
          display_var = key
          break
        }
      }
      // tracking_items
      this.tracking_items = this.tracking_vars[display_var]
    },
    loadHandlerJSON(e) {
      var contents = JSON.parse(e.target.result)
      this.loadingFile = true
      //console.log(contents)
      //console.log(this.tracking_vars)
      var range = document.getElementById('timelineslider')
      this.tracking_years = contents.tracking_years
      range.noUiSlider.updateOptions({
        start: contents.tracking_years
      })
      //console.log(this.tracking_years)
      //changeToVar(contents.tracking_displayed_var)
      this.tracking_vars = contents.tracking_vars
      //this.displayed_var = contents.tracking_displayed_var
      //this.tracking_items = contents.tracking_vars[contents.tracking_displayed_var]
      for (var key in this.tracking_vars) {
        if (key != "") {
          this.changeToVar(key)
          break
        }
      }
    },
    save() {
      localStorage.tracking_vars = JSON.stringify(this.tracking_vars)
      localStorage.tracking_years = JSON.stringify(this.tracking_years)
      localStorage.tracking_displayed_var = this.displayed_var
      //alert("Daten wurden gespeichert.")
      this.showAlert('Daten wurden gespeichert.')
    },
    async share() {
      let data = JSON.stringify(this.exportFileJSON())
      await axios.post(`${this.$baseURL}/api/share/code/`, {"JSON": data}).then(res => {
        //console.log(res.data)
        //alert(res.data.Code)
        this.shareCode = this.$baseURL+'/track/'+res.data.Code
      })
    },
    async loadTrackingInfo(drg, code) {
      await axios.get(`${this.$baseURL}/api/${drg}/track/?code=${code}&year_start=${this.tracking_years[0]}&year_stop=${this.tracking_years[1]}&year=${this.searchYear}&overview=1`).then(res => {
        //console.log(res.data)
        this.tracking_items[code].loading = false
        this.tracking_items[code].data = res.data
        if (!('edit_code' in this.tracking_items[code])) {
          this.tracking_items[code].edit_code = 0
          this.tracking_items[code].edit_data = {}
        }
        this.tracking_vars[this.displayed_var][code] = this.tracking_items[code]
        localStorage.tracking_vars = JSON.stringify(this.tracking_vars)
      })
      //console.log(this.tracking_items)
    },
    /*   TRACKING YEARS   */
    changeTrackingYears(startYear, stopYear) {
      if (startYear != undefined && stopYear != undefined) {
        this.tracking_years = [startYear, stopYear]
      }
    },
    createSlider() {
      var range = document.getElementById('timelineslider');
      var values = []
      this.available_years.forEach((year) => {
        values.push(year.Year)
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
        start: this.tracking_years,
        range: {'min': 0, 'max': values.length-1},
        step: 1,
        margin: 1,
        connect: true,
        format: format,
        pips: {mode: 'steps', format: format, density: 50}
      });
      var changeTrackingYears = this.changeTrackingYears
      range.noUiSlider.on('change', function(values, handle) {
        changeTrackingYears(values[0], values[1])
      })
      //this.changeTrackingYears(values[0], values[values.length-1])
    },
    tab(i) {
      this.tab_value = i;
    },
    /*   SEARCH    */
    async search() {
      if (this.searchText.length < 3) {
        this.tab_value = -2;
        this.results_icd = [];
        this.results_ops = [];
        return;
      }
      try {
        this.tab_value = -1;
        this.loading = 2;
        this.results_icd = [];
        this.results_ops = [];
        await axios.get(`${this.$baseURL}/api/icd/search/?s=${this.searchText}&year=${this.searchYear}`).then(res => {
          this.results_icd = res.data;
          this.loading -= 1;
          if (this.results_icd.length > 0) {
            this.tab_value = 0;
          }
        });
        await axios.get(`${this.$baseURL}/api/ops/search/?s=${this.searchText}&year=${this.searchYear}`).then(res => {
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
  components: { LoadingAnimation, TrackingSVG }
}
</script>

<style>
.noUi-pips-horizontal {
  height: auto !important;
}
</style>