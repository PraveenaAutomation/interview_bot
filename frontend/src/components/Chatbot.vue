<template>
  <div class="min-h-screen bg-gray-50 text-gray-800">
    <!-- Header -->
    <header class="flex justify-between items-center px-6 py-4 bg-white shadow-sm">
      <div class="flex items-center gap-3">
        <img :src="BotIcon" alt="Bot Icon" class="w-8 h-8" />
        <h1 class="text-xl font-bold">Interview Q&A Bot</h1>
      </div>
      <button @click="clearHistory" class="flex items-center text-red-600 font-medium hover:underline">
        <Trash2 class="w-5 h-5 mr-1" /> Clear History
      </button>
    </header>

    <!-- Main Content -->
    <div class="flex flex-col md:flex-row max-w-7xl mx-auto px-4 py-6 gap-6">
      <!-- History Panel -->
      <aside class="w-full md:w-1/4 bg-white rounded-2xl shadow p-4 h-fit">
        <h2 class="text-lg font-semibold mb-3 flex justify-between items-center">
          Question History
          <span v-if="history.length" class="bg-blue-100 text-blue-600 text-xs px-2 py-0.5 rounded-full">
            {{ history.length }}
          </span>
        </h2>
        <ul class="space-y-3">
          <li
            v-for="(item, i) in history"
            :key="i"
            class="bg-gray-50 border border-gray-200 rounded-lg p-3 text-sm hover:bg-gray-100"
          >
            <div class="font-medium">{{ item.question }}</div>
            <div class="text-xs text-gray-500">{{ formatTime(item.time) }}</div>
          </li>
        </ul>
      </aside>

      <!-- Chat Area -->
      <main class="flex-1 bg-white rounded-2xl shadow p-6 flex flex-col justify-between">
        <div>
          <!-- Welcome or Chat -->
          <div class="mb-4">
            <h3 class="text-lg font-semibold">Interview Assistant</h3>
            <p class="text-sm text-gray-500">Ready to help with your interview preparation</p>
          </div>

          <!-- Initial Message -->
          <div v-if="!answer" class="flex gap-2 mb-6">
            <img :src="BotIcon" alt="Bot" class="w-6 h-6 mt-1" />
            <div class="bg-blue-50 text-blue-900 p-4 rounded-lg max-w-[90%]">
              Hello! I'm your interview assistant. Ask me any interview question and I'll help you prepare a great answer.
              What would you like to practice today?
            </div>
          </div>

          <!-- Conversation -->
          <div v-else class="space-y-4">
            <!-- User Question -->
            <div class="flex justify-start gap-2">
              <div class="bg-white border border-gray-300 p-3 rounded-lg max-w-[75%] text-gray-800 text-sm">
                {{ currentQuestion }}
              </div>
            </div>
            <!-- Bot Answer -->
            <div class="flex justify-start gap-2">
              <img :src="BotIcon" alt="Bot" class="w-6 h-6 mt-1" />
              <div class="bg-blue-50 text-gray-900 p-3 rounded-lg max-w-[75%] text-sm">
                {{ answer }}
              </div>
            </div>
          </div>

          <!-- Error -->
          <div v-if="error" class="text-red-600 text-sm mt-2">{{ error }}</div>
        </div>

        <!-- Input Area -->
        <div class="mt-6 flex gap-2">
          <input
            v-model="question"
            @keyup.enter="askQuestion"
            type="text"
            placeholder="Ask an interview question..."
            class="flex-1 border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring focus:ring-blue-300"
          />
          <button
            @click="askQuestion"
            :disabled="loading"
            class="bg-blue-600 hover:bg-blue-700 text-white px-5 py-3 rounded-xl shadow flex items-center justify-center"
          >
            <Send class="w-4 h-4" />
          </button>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Trash2, Send } from 'lucide-vue-next'
import BotIcon from '../assets/bot-icon.png'

const question = ref('')
const answer = ref('')
const error = ref('')
const loading = ref(false)
const currentQuestion = ref('')
const history = ref([])

const askQuestion = async () => {
  if (!question.value.trim()) {
    error.value = 'Please enter a question.'
    return
  }

  error.value = ''
  loading.value = true
  answer.value = ''

  try {
    const res = await fetch('http://localhost:5000/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: question.value })
    })
    const data = await res.json()

    if (res.ok) {
      answer.value = data.answer
      currentQuestion.value = question.value
      history.value.unshift({ question: question.value, time: new Date() })
    } else {
      error.value = data.error || 'Something went wrong.'
    }
  } catch (err) {
    error.value = 'Backend error. Check connection.'
  } finally {
    loading.value = false
    question.value = ''
  }
}

const clearHistory = () => {
  history.value = []
  question.value = ''
  answer.value = ''
  error.value = ''
  currentQuestion.value = ''
}

const formatTime = (date) => {
  const diff = Math.floor((new Date() - new Date(date)) / 60000)
  if (diff < 1) return 'just now'
  if (diff === 1) return '1 minute ago'
  return `${diff} minutes ago`
}
</script>

<style scoped>
body { font-family: 'Inter', sans-serif; }
</style>
