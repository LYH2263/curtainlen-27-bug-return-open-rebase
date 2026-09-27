<script setup>
const props = defineProps({ panels: Number, cutHeight: Number, meters: Number, finishedWidth: Number })
function panelW() {
  const fw = props.finishedWidth || 0
  const n = props.panels || 1
  // 裁幅示意随新成品宽刷新：总宽按成品宽等比，单幅不超 90px
  return Math.max(24, Math.min(90, Math.round((fw * 40) / n)))
}
</script>
<template>
  <div class="panel-cut">
    <div v-for="n in Math.min(panels||0,8)" :key="n" class="panel"
         :style="{height: `${(cutHeight||1)*40}px`, width: `${panelW()}px`}"></div>
    <span v-if="(panels||0) > 8" class="more">…</span>
    <p>成品宽 {{ finishedWidth }} m｜{{ panels }} 幅 × {{ cutHeight }} m = {{ meters }} m</p>
  </div>
</template>
