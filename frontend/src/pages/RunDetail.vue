<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
import PanelCut from '../components/PanelCut.vue'
const props = defineProps({ id: String })
const r = ref(null)
onMounted(async () => { r.value = await getJSON(`/api/runs/${props.id}`) })
</script>
<template><div class="page" v-if="r"><h1>旧单 #{{ r.id }}</h1>
<p>{{ r.window_name }} × {{ r.fabric_name }}</p>
<p>写入时回位：左 {{ r.result?.return_left_cm ?? 0 }} cm｜右 {{ r.result?.return_right_cm ?? 0 }} cm</p>
<p>成品宽 {{ r.result?.finished_width }} m｜{{ r.result?.panels }} 幅 × {{ r.result?.cut_height }} m</p>
<p>用布 <strong>{{ r.result?.meters }} m</strong></p>
<PanelCut v-if="r.result" :panels="r.result.panels" :cut-height="r.result.cut_height"
  :meters="r.result.meters" :finished-width="r.result.finished_width" />
<p class="dim">成品宽、幅数、米数与回位厘米均按编号打开时的落库快照显示，不随后续改动重算。</p>
<p v-if="r.note">备注：{{ r.note }}</p>
</div></template>
