<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template><div class="page"><h1>记录</h1><ul>
<li v-for="r in items" :key="r.id">
<router-link :to="`/runs/${r.id}`">#{{ r.id }}</router-link>
{{ r.window_name }} {{ r.result?.meters }}m
<span class="dim">（回位 左{{ r.result?.return_left_cm ?? 0 }}/右{{ r.result?.return_right_cm ?? 0 }}cm，{{ r.result?.panels }}幅）</span>
</li>
</ul>
<p class="hint">开放视图保留回位厘米字段；成品宽 / 幅数 / 米数取列表接口返回值。</p>
</div></template>
