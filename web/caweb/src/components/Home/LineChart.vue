<template>
  <DxChart
    id="chart"
    :data-source="dataSource"
    :palette="palette"
    @legend-click="legendClickHandler($event)"
    @series-click="seriesClickHandler($event)"
  >
    <DxCommonSeriesSettings type="spline" argument-field="holyca_index"/>
    <DxCommonAxisSettings>
      <DxGrid color="#515873" :visible="true"/>
      <DxLabel :font="{color:'#8e93a7'}"/>
      <DxTick color="#515873"/>
    </DxCommonAxisSettings>
    <DxSeries v-for="(player,index) in players" :key="index" :value-field="player" :name="player">
      <DxPoint :size="6"/>
    </DxSeries>
    <DxValueAxis color="#515873"/>
    <DxArgumentAxis :allow-decimals="false" :axis-division-factor="1" color="#515873">
      <DxLabel>
        <DxFormat type="decimal"/>
      </DxLabel>
    </DxArgumentAxis>
    <DxLegend vertical-alignment="bottom" horizontal-alignment="center" :font="{color:'#8e93a7'}"/>
    <DxTooltip :enabled="true" :customize-tooltip="customizeTooltip"/>
  </DxChart>
</template>
<script>
import {
  DxChart,
  DxSeries,
  DxArgumentAxis,
  DxCommonSeriesSettings,
  DxCommonAxisSettings,
  DxGrid,
  DxLegend,
  DxTooltip,
  DxLabel,
  DxFormat,
  DxValueAxis,
  DxTick,
  DxPoint
} from "devextreme-vue/chart";

export default {
  components: {
    DxChart,
    DxSeries,
    DxArgumentAxis,
    DxCommonSeriesSettings,
    DxCommonAxisSettings,
    DxGrid,
    DxLegend,
    DxTooltip,
    DxLabel,
    DxFormat,
    DxValueAxis,
    DxTick,
    DxPoint
  },
  props: {
    players: {
      type: Array,
      default: () => {
        return [];
      }
    },
    dataSource: {
      type: Array,
      default: () => {
        return [];
      }
    },
    palette: {
      type: String,
      default: "Violet"
    }
  },
  data: () => ({}),
  methods: {
    seriesClickHandler(e) {
        this.toggleVisibility(e.target);
    },
    legendClickHandler(e) {
        let item=e.component.getSeriesByName(e.target.name);
        this.toggleVisibility(item);
    },
    toggleVisibility(item) {
        item.isVisible() ? item.hide() : item.show();
    },
    customizeTooltip(pointInfo){
      return {
        text: `${pointInfo.valueText}<br/>${this.dataSource[pointInfo.argument-1].holyca_date.split("T")[0]}`
      };
    }
  }
};
</script>
<style scoped>
#chart {
  width: 600px;
  height: 220px;
  max-height: 220px;
  padding-top: 10px;
}
</style>
