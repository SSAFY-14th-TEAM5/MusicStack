<template>
  <form class="search-box" @submit.prevent="submitSearch">
    <input
      type="text"
      v-model="localKeyword"
      :placeholder="placeholder"
    />
    <button type="submit">
      Search
    </button>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: 'Search songs, artists, genres...',
  },
})

const emit = defineEmits(['update:modelValue', 'search'])

const localKeyword = ref(props.modelValue)

/* v-model 동기화 */
watch(localKeyword, (val) => {
  emit('update:modelValue', val)
})

watch(
  () => props.modelValue,
  (val) => {
    localKeyword.value = val
  }
)

const submitSearch = () => {
  if (!localKeyword.value.trim()) return
  emit('search', localKeyword.value)
}
</script>

<style scoped>
.search-box {
  display: flex;
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  border-radius: 50px;
  overflow: hidden;
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.6);
  transition: all 0.3s ease;
  opacity: 0;
  animation: fadeUp 0.8s ease-out 0.6s forwards;
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.search-box:focus-within {
  border-color: #D4FF00;
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.6), 0 0 30px rgba(212, 255, 0, 0.2);
}

.search-box input {
  flex: 1;
  padding: 18px 26px;
  border: none;
  outline: none;
  font-size: 1rem;
  background: transparent;
  color: #ffffff;
  font-family: 'Outfit', sans-serif;
}

.search-box input::placeholder {
  color: #666666;
}

.search-box button {
  padding: 0 32px;
  border: none;
  background: #D4FF00;
  color: #0a0a0a;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.25s ease;
  font-family: 'Outfit', sans-serif;
}

.search-box button:hover {
  background: #E6FF33;
  padding: 0 36px;
  box-shadow: 0 0 30px rgba(212, 255, 0, 0.4);
}
</style>