<template>
  <!-- PROMPT POPUP -->
  <div v-if="store.show_prompt!=''" @click="closePrompt()" class="fixed flex z-20 w-full h-full bg-black top-0 bg-opacity-50 justify-center items-center">
    <div @click.stop.prevent="" class="flex flex-col bg-white rounded-lg z-20 relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:w-full sm:max-w-lg">
      <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
        <div class="sm:flex sm:items-start">
          <div class="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full sm:mx-0 sm:h-10 sm:w-10"
            :class="[(store.show_prompt=='delete')?'bg-red-100':'',(store.show_prompt=='change')?'bg-yellow-100':'',(store.show_prompt=='add')?'bg-green-100':'']">
            <svg v-if="store.show_prompt=='delete'" class="h-6 w-6 text-red-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 10.5v3.75m-9.303 3.376C1.83 19.126 2.914 21 4.645 21h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 4.88c-.866-1.501-3.032-1.501-3.898 0L2.697 17.626zM12 17.25h.007v.008H12v-.008z" />
            </svg>
            <svg v-if="store.show_prompt=='change'" class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path>
            </svg>
            <svg v-if="store.show_prompt=='add'" class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
            </svg>
          </div>
          <div class="mt-3 text-center w-full sm:mt-0 sm:ml-4 sm:text-left">
            <h3 class="text-lg font-medium leading-6 text-gray-900">
              <span v-if="store.show_prompt=='delete'">Variable löschen</span>
              <span v-if="store.show_prompt=='change'">Variable umbenennen</span>
              <span v-if="store.show_prompt=='add'">Variable hinzufügen</span>
            </h3>
            <div class="mt-2 text-sm text-gray-500">
              <p v-if="store.show_prompt=='delete'">Wollen Sie wirklich diese Variable löschen? Diese Aktion kann nicht rückgängig gemacht werden.</p>
              <p v-if="store.show_prompt=='change'">Bitte geben Sie einen neuen Variablennamen an:</p>
              <p v-if="store.show_prompt=='add'">Bitte wählen Sie einen Namen für die neue Variable aus:</p>
            </div>
            <input v-if="store.show_prompt=='change' || store.show_prompt=='add'" @keyup.enter="(store.show_prompt=='change')?changeVarName():addVar()" type="text" placeholder="Variablenname" v-model="promptInput" class="w-full mt-3 px-1 py-0.5 rounded-md border border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm">
            <div v-if="promptError!=''" class="mt-2 text-sm text-red-500">
              <p>{{ promptError }}</p>
            </div>
          </div>
        </div>
      </div>
      <div class="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
        <button v-if="store.show_prompt=='delete'" type="button" @click="deleteVar()" class="inline-flex w-full justify-center rounded-md border border-transparent bg-red-600 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 sm:ml-3 sm:w-auto sm:text-sm">
          Löschen
        </button>
        <button v-if="store.show_prompt=='change'" type="button" @click="changeVarName()" class="inline-flex w-full justify-center rounded-md border border-transparent bg-yellow-500 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:ring-offset-2 sm:ml-3 sm:w-auto sm:text-sm">
          Umbenennen
        </button>
        <button v-if="store.show_prompt=='add'" type="button" @click="addVar()" class="inline-flex w-full justify-center rounded-md border border-transparent bg-green-500 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2 sm:ml-3 sm:w-auto sm:text-sm">
          Hinzufügen
        </button>
        <button type="button" @click="closePrompt()" class="mt-3 inline-flex w-full justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-base font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
          Abbrechen
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
      store,
      promptError: "",
      promptInput: ""
    }
  },
  methods: {
    addVar() {
      if (this.promptInput === '') {
        this.promptError = "Bitte einen gültigen Namen wählen."
        return
      } else if (store.tracker.containsVar(this.promptInput)) {
        this.promptError = "Dieser Name ist bereits vergeben."
        return
      }
      store.tracker.addVar(this.promptInput)
      this.closePrompt()
    },
    changeVarName() {
      if (this.promptInput === '') {
        this.promptError = "Bitte einen gültigen Namen wählen."
        return
      } else if (store.tracker.containsVar(this.promptInput)) {
        this.promptError = "Dieser Name ist bereits vergeben."
        return
      }
      store.tracker.changeVarName(this.promptInput)
      this.closePrompt()
    },
    deleteVar() {
      store.tracker.delVar(store.tracker.displayedVar)
      this.closePrompt()
    },
    closePrompt() {
      store.show_prompt = ""
      this.promptError = ""
      this.promptInput = ""
    },
  }
}
</script>