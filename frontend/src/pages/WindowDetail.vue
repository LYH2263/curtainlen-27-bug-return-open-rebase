<script setup>
import { onMounted, ref, watch } from 'vue'
import { getJSON } from '../api'
import PanelCut from '../components/PanelCut.vue'
const props = defineProps({ id: String })
const w = ref(null); const fabrics = ref([]); const fid = ref(1)
const retL = ref(0); const retR = ref(0)
const out = ref(null); const base = ref(null); const err = ref('')
async function load(){
  w.value = await getJSON(`/api/windows/${props.id}`)
  fabrics.value = (await getJSON('/api/fabrics')).items.filter(x=>x.data_quality==='clean')
  if (fabrics.value.length) fid.value = fabrics.value[0].id
  await dry()
}
onMounted(load)
async function dry(){
  err.value = ''
  if (!w.value || w.value.data_quality === 'dirty') return
  try {
    const l = Number(retL.value)||0, r = Number(retR.value)||0
    if (l < 0 || r < 0) throw new Error('回位不能为负')
    out.value = await getJSON(`/api/estimate?window_id=${props.id}&fabric_id=${fid.value}&return_left_cm=${l}&return_right_cm=${r}`)
    base.value = await getJSON(`/api/estimate?window_id=${props.id}&fabric_id=${fid.value}`)
  } catch (e) { err.value = e.message || String(e) }
}
watch(fid, dry)
</script>
<template><div class="page" v-if="w"><h1>{{ w.name }}</h1>
<p v-if="w.data_quality==='dirty'" class="bad">{{ w.note }}</p>
<template v-if="w.data_quality!=='dirty'">
<p>宽 {{ w.width }} 高 {{ w.height }} 褶倍 {{ w.fullness }}</p>
<label>面料
<select v-model.number="fid"><option v-for="x in fabrics" :key="x.id" :value="x.id">{{ x.name }}</option></select>
</label>
<label>左回位 cm <input type="number" min="0" step="1" v-model="retL" @change="dry"></label>
<label>右回位 cm <input type="number" min="0" step="1" v-model="retR" @change="dry"></label>
<button @click="dry">试算</button>
<p v-if="err" class="bad">试算失败：{{ err }}</p>
<p v-if="out">成品宽 {{ out.finished_width }} m｜幅数
  <strong>{{ out.panels }}</strong>（无回位 {{ base?.panels }} 幅）｜用布 {{ out.meters }} m</p>
<PanelCut v-if="out" :panels="out.panels" :cut-height="out.cut_height" :meters="out.meters" :finished-width="out.finished_width" />
</template>
</div></template>
