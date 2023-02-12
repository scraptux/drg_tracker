<template>
  <!-- NOTIFICATION POPUP -->
    <div class="fixed flex flex-col z-20 right-0 mt-2 mr-4 text-base text-blue-800">
      <div v-for="notification, idx in store.notifications.slice().reverse()" :key="notification"  @click="store.deleteNotification(idx)"
        class="flex w-full place-items-center fade show bg-blue-200 rounded-lg mt-2 py-3 px-10 inline-flex items-center border border-blue-300 hover:cursor-pointer"
        :class="(notification=='')?'hidden':'block'">
        <p class="w-full text-center">{{ notification }}</p>
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