<template>
  <DxDataGrid
    :data-source="dataSource"
    :show-borders="true"
    :show-row-lines="true"
    :height="850"
  >
    <DxPaging :page-size="20"/>
    <DxPager
      :show-page-size-selector="true"
      :allowed-page-sizes="pageSizes"
      :show-info="true"
    />
    <DxSearchPanel
      :visible="true"
      :highlight-case-sensitive="true"
    />
    <DxFilterRow
        :visible="true"
        apply-filter="Immediately"
      />
      <DxHeaderFilter
        :visible="true"
      />
    <DxColumn data-field="date" caption="时间" alignment="center" data-type="date"/>
    <DxColumn data-field="player" caption="主题" alignment="center"/>
    <DxColumn data-field="map" caption="分类" alignment="center"/>
    <DxColumn data-field="date_show" caption="对抗" alignment="center"/>
    <DxColumn data-field="player_MMR" caption="创建者" alignment="center"/>
    <!-- <DxColumn data-field="opponent" caption="对手" alignment="center"/>
    <DxColumn data-field="opponent_MMR" caption="对手MMR" alignment="center"/>
    <DxColumn data-field="game_length" caption="游戏时长" alignment="center"/>
    <DxColumn data-field="winner" caption="胜者" alignment="center"/> -->
    <DxColumn data-field="rep_id" caption="操作" cell-template="data-template" alignment="center"/>
    <template #data-template="cell">
      <p style="margin:0;cursor: pointer;" @click="get_rep(cell.data.value)">查看</p>
    </template>
  </DxDataGrid>
</template>
<script>

import { DxDataGrid, DxColumn, DxPager, DxPaging,DxSearchPanel,DxHeaderFilter,DxFilterRow } from 'devextreme-vue/data-grid';

export default {
  components: {
    DxDataGrid,
    DxColumn,
    DxPager,
    DxPaging,
    DxSearchPanel,
    DxHeaderFilter,
    DxFilterRow
  },
  // props:{
  //   dataSource:{
  //     type:Array,
  //     default(){
  //       return []
  //     }
  //   }
  // },
  data:()=> ({
    pageSizes: [5, 10, 20],
    dataSource:{

    }
  }),
  methods: {
    // get_rep(rep_id) {
    //   let url = "https://sc2replaystats.com/replay/" + rep_id;
    //   window.open(url, "_blank");
    // }
  },
};
</script>
