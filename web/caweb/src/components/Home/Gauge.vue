<template>
  <div>
    <DxCircularGauge id="gauge" ref="gauge" :value="score">
      <DxScale :start-value="0" :end-value="max_value" :tick-interval="interval">
        <DxLabel :use-range-colors="false" :font="{color:'#8e93a7'}" :indentFromTick="0"/>
        <DxTick color="#363e5b" :width="8" :length="10"/>
      </DxScale>
      <DxValueIndicator type="rectangleNeedle" color="#ffffff" :offset="10"/>
      <DxRangeContainer :palette="palette">
        <DxRange :start-value="0" :end-value="interval"/>
        <DxRange :start-value="interval" :end-value="interval*3"/>
        <DxRange :start-value="interval*3" :end-value="200"/>
      </DxRangeContainer>
    </DxCircularGauge>
  </div>
</template>
<script>
import {
  DxCircularGauge,
  DxScale,
  DxLabel,
  DxRangeContainer,
  DxRange,
  DxValueIndicator,
  DxTick
} from "devextreme-vue/circular-gauge";

export default {
  components: {
    DxCircularGauge,
    DxScale,
    DxLabel,
    DxRangeContainer,
    DxRange,
    DxValueIndicator,
    DxTick
  },
  props: {
    score: {
      type: Number,
      default: 0
    },
    max_value: {
      type: Number,
      default: 200
    },
    palette:{
        type: String,
        default: "Pastel"
    }
  },
  data: () => ({}),
  computed: {
    interval() {
      return this.max_value / 4;
    }
  },
  mounted() {
    this.updateValues();
  },
  watch: {
      score(){
          this.updateValues();
      }
  },
  methods: {
    updateValues() {
      this.$refs.gauge.instance.value(this.score);
    }
  }
};
</script>
<style scoped>
#gauge {
  width: 210px;
  height: 175px;
}
.dx-visibility-change-handler >>> .dxg-spindle-hole {
  fill: #363e5b !important;
}
</style>
