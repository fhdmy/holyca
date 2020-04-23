<template>
  <DxPolarChart
    id="chart"
    :data-source="DataSource"
    :use-spider-web="true"
    :palette="palette"
    @point-click="pointClickHandler($event)"
    @legend-click="legendClickHandler($event)"
  >
    <DxCommonSeriesSettings type="line"/>
    <DxSeries v-for="it in items" :key="it.value" :value-field="it.value" :name="it.name">
      <DxPoint :size="6"/>
    </DxSeries>
    <DxLabel :font="{color:'#8e93a7'}"/>
    <DxLegend vertical-alignment="bottom" horizontal-alignment="center" :font="{color:'#8e93a7'}"/>
    <DxTooltip :enabled="true" :customize-tooltip="customizeTooltip"/>
  </DxPolarChart>
</template>
<script>
import {
  DxPolarChart,
  DxCommonSeriesSettings,
  DxSeries,
  DxTooltip,
  DxLabel,
  DxLegend,
  DxPoint
} from "devextreme-vue/polar-chart";

export default {
  components: {
    DxPolarChart,
    DxCommonSeriesSettings,
    DxSeries,
    DxTooltip,
    DxLabel,
    DxLegend,
    DxPoint
  },
  props: {
    palette: {
      type: String,
      default: "Pastel"
    },
    items: {
      type: Array,
      default: () => {
        return [];
      }
    },
    DataSource: {
      type: Array,
      default: () => {
        return [];
      }
    }
  },
  data: () => ({}),
  methods: {
    customizeTooltip(pointInfo) {
      return {
        text: `${pointInfo.seriesName}<br/>${pointInfo.valueText}`
      };
    },
    pointClickHandler(e) {
      this.toggleVisibility(e.target);
    },
    legendClickHandler(e) {
      let item=e.component.getSeriesByName(e.target.name);
      this.toggleVisibility(item);
    },
    toggleVisibility(item) {
      item.isVisible() ? item.hide() : item.show();
    }
  }
};
</script>
<style>
#chart {
  width: 300px;
  height: 210px;
}
</style>
