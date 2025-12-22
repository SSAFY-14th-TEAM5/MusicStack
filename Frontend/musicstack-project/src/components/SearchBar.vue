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
  background: white;
  border-radius: 40px;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

.search-box input {
  flex: 1;
  padding: 16px 22px;
  border: none;
  outline: none;
  font-size: 1rem;
}

.search-box button {
  padding: 0 28px;
  border: none;
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s ease;
}

.search-box button:hover {
  opacity: 0.9;
}
</style>