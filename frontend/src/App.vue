<template>
  <div class="min-h-screen bg-gray-50">
    <Chatbot />
  </div>
</template>

<script>
import Chatbot from './components/Chatbot.vue';

export default {
  name: 'App',
  components: { Chatbot },
};
</script>


<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
