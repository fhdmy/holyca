<template>
  <DxPieChart
    id="pie"
    :data-source="dataSource"
    palette="Soft Blue"
    @point-click="pointClickHandler($event)"
    @legend-click="legendClickHandler($event)"
  >
    <DxSeries argument-field="race" value-field="sum">
      <DxLabel :visible="true">
        <DxConnector :visible="true" :width="1"/>
      </DxLabel>
    </DxSeries>
    <DxLegend vertical-alignment="bottom" horizontal-alignment="center" :font="{color:'#8e93a7'}"/>
  </DxPieChart>
</template>

<script>
import DxPieChart, {
  DxSeries,
  DxLabel,
  DxConnector,
  DxLegend
} from "devextreme-vue/pie-chart";

export default {
  components: {
    DxPieChart,
    DxSeries,
    DxLabel,
    DxConnector,
    DxLegend
  },
  props:{
    palette:{
        type:String,
        default:"Soft Blue"
    },
    dataSource:{
        type:Array,
        default:()=>{
            return [
                {
                    race: "P",
                    sum: 0
                },
                {
                    race: "Z",
                    sum: 0
                },
                {
                    race: "T",
                    sum: 0
                }
            ];
        }
    }
  },
  data: () => ({
    
  }),
  methods: {
    pointClickHandler(e) {
      this.toggleVisibility(e.target);
    },
    legendClickHandler(e) {
      let arg = e.target,
        item = e.component.getAllSeries()[0].getPointsByArg(arg)[0];

      this.toggleVisibility(item);
    },
    toggleVisibility(item) {
      item.isVisible() ? item.hide() : item.show();
    }
  }
};
</script>

<style scoped>
#pie {
  width: 210px;
  height: 210px;
}
</style>
