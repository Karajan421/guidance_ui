<template>
  <div>
    <button @click="runScript">Run Script</button>
    <div class="result-box" v-if="result">
      <h2>Result:</h2>
      <p>{{ result }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      result: null,
    };
  },
  methods: {
    async runScript() {
      const response = await axios.post('http://localhost:5001/run_script', {
        question: 'What is the office location?',
        context: 'your-context-here'
      });
      this.result = response.data;
    },
  },
};
</script>

<style scoped>
.result-box {
  border: 1px solid #333;
  padding: 20px;
  margin: 20px 0;
  background-color: #f0f0f0;
}
</style>
