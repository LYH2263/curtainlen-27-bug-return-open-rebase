<script setup>
import { onMounted, ref, watch } from 'vue'
import { getJSON, postJSON } from '../api'
import PanelCut from '../components/PanelCut.vue'
const windows = ref([]); const fabrics = ref([])
const wid = ref(1); const fid = ref(1)
const retL = ref(0); const retR = ref(0)
const out = ref(null); const base = ref(null); const err = ref('')
onMounted(async () => {
  windows.value = (await getJSON('/api/windows')).items.filter(x=>x.data_quality==='clean')
  fabrics.value = (await getJSON('/api/fabrics')).items.filter(x=>x.data_quality==='clean')
  if (windows.value.length) wid.value = windows.value[0].id
  if (fabrics.value.length) fid.value = fabrics.value[0].id
  await dry()
})
async function dry(){
  err.value = ''
  try {
    const l = Number(retL.value)||0, r = Number(retR.value)||0
    if (l < 0 || r < 0) throw new Error('回位不能为负')
    const q = `/api/estimate?window_id=${wid.value}&fabric_id=${fid.value}&return_left_cm=${l}&return_right_cm=${r}`
    out.value = await getJSON(q)
    base.value = await getJSON(`/api/estimate?window_id=${wid.value}&fabric_id=${fid.value}`)
  } catch (e) { err.value = e.message || String(e) }
}
async function save(){
  err.value = ''
  try {
    const r = await postJSON('/api/estimate',{
      window_id:wid.value, fabric_id:fid.value, save:true,
      return_left_cm:Number(retL.value)||0, return_right_cm:Number(retR.value)||0,
    })
    out.value = r
  } catch (e) { err.value = e.message || String(e) }
}
watch([wid, fid], dry)
</script>
<template><div class="page"><h1>算料</h1>
<label>窗户
<select v-model.number="wid"><option v-for="x in windows" :key="x.id" :value="x.id">{{ x.name }}</option></select>
</label>
<label>面料
<select v-model.number="fid"><option v-for="x in fabrics" :key="x.id" :value="x.id">{{ x.name }}</option></select>
</label>
<label>左回位 cm <input type="number" min="0" step="1" v-model="retL" @change="dry"></label>
<label>右回位 cm <input type="number" min="0" step="1" v-model="retR" @change="dry"></label>
<button @click="dry">试算</button><button @click="save">保存</button>
<p v-if="err" class="bad">试算失败：{{ err }}</p>
<p v-if="out">成品宽 {{ out.finished_width }} m｜幅数
  <strong>{{ out.panels }}</strong>（无回位 {{ base?.panels }} 幅）｜用布 {{ out.meters }} m</p>
<PanelCut v-if="out" :panels="out.panels" :cut-height="out.cut_height" :meters="out.meters" :finished-width="out.finished_width" />
</div></template>
