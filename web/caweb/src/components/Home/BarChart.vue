<template>
  <DxChart
    id="chart"
    :data-source="dataSource"
  >
    <DxArgumentAxis color="#515873" />
    <DxValueAxis color="#515873" />
    <DxCommonAxisSettings>
        <DxGrid color="#515873" />
        <DxLabel :font="{color:'#8e93a7'}"/>
        <DxTick color="#515873"/>
    </DxCommonAxisSettings>
    <DxSeries
      argument-field="teammate"
      value-field="reps"
      name="盘数"
      type="bar"
      color="#7cd2c7"
    >
    </DxSeries>
    <DxLegend
      :font="{color:'#8e93a7'}"
    />
    <DxTooltip
      :enabled="true"
    />
  </DxChart>
</template>
<script>
import { DxChart, DxSeries,DxCommonAxisSettings,DxLabel,DxGrid,DxTick,DxValueAxis,DxArgumentAxis,DxTooltip,DxLegend } from 'devextreme-vue/chart';

export default {
  components: {
    DxChart,
    DxSeries,
    DxCommonAxisSettings,
    DxLabel,
    DxGrid,
    DxTick,
    DxValueAxis,
    DxArgumentAxis,
    DxTooltip,
    DxLegend
  },
  props:{
    dataSource:{
        type: Array,
        default:()=>{
            return [];
        }
    }
  },
  data:()=> ({
    
  })
};
</script>
<style scoped>
#chart {
    width:600px;
    height: 165px;
    padding-top: 10px;
}
</style>
