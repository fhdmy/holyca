<template>
  <div class="wrapper">
    <DxBox :height="table_height" direction="col" width="100%">
      <!-- title -->
      <DxItem :ratio="1">
        <template #default>
          <div class="title-wrapper">
            <DxBox :height="20" direction="row" width="100%">
              <DxItem :ratio="3">
                <template #default>
                  <div class="cell">玩家</div>
                </template>
              </DxItem>
              <DxItem :ratio="2">
                <template #default>
                  <div class="cell">玩家MMR</div>
                </template>
              </DxItem>
              <DxItem :ratio="2">
                <template #default>
                  <div class="cell">玩家种族</div>
                </template>
              </DxItem>
              <DxItem :ratio="3">
                <template #default>
                  <div class="cell">对手</div>
                </template>
              </DxItem>
              <DxItem :ratio="2">
                <template #default>
                  <div class="cell">对手MMR</div>
                </template>
              </DxItem>
              <DxItem :ratio="2">
                <template #default>
                  <div class="cell">对手种族</div>
                </template>
              </DxItem>
              <DxItem :ratio="2">
                <template #default>
                  <div class="cell">游戏时长</div>
                </template>
              </DxItem>
              <DxItem :ratio="3">
                <template #default>
                  <div class="cell">胜者</div>
                </template>
              </DxItem>
              <DxItem :ratio="2">
                <template #default>
                  <div class="cell">链接</div>
                </template>
              </DxItem>
            </DxBox>
          </div>
        </template>
      </DxItem>

      <!-- cell -->
      <DxItem :ratio="1" v-for="(item,index) in dataSource" :key="index">
        <template #default>
          <div class="cell-wrapper" :class="{'darker':(index%2==1)}">
            <DxBox :height="20" direction="row" width="100%">
              <DxItem :ratio="3">
                <template #default>
                  <div class="cell">{{item.player}}</div>
                </template>
              </DxItem>
              <DxItem :ratio="2">
                <template #default>
                  <div class="cell">{{item.play_MMR}}</div>
                </template>
              </DxItem>
              <DxItem :ratio="2">
                <template #default>
                  <div class="cell">{{item.player_race}}</div>
                </template>
              </DxItem>
              <DxItem :ratio="3">
                <template #default>
                  <div class="cell">{{item.opponent}}</div>
                </template>
              </DxItem>
              <DxItem :ratio="2">
                <template #default>
                  <div class="cell">{{item.opponent_MMR}}</div>
                </template>
              </DxItem>
              <DxItem :ratio="2">
                <template #default>
                  <div class="cell">{{item.opponent_race}}</div>
                </template>
              </DxItem>
              <DxItem :ratio="2">
                <template #default>
                  <div class="cell">{{item.game_length}}</div>
                </template>
              </DxItem>
              <DxItem :ratio="3">
                <template #default>
                  <div class="cell">{{item.winner}}</div>
                </template>
              </DxItem>
              <DxItem :ratio="2">
                <template #default>
                  <div class="cell">观看</div>
                </template>
              </DxItem>
            </DxBox>
          </div>
        </template>
      </DxItem>
      <DxItem :ratio="2">
        <template #default>
        </template>
        </DxItem>
    </DxBox>
  </div>
</template>
<script>
import { DxBox, DxItem } from "devextreme-vue/box";
export default {
  components: {
    DxBox,
    DxItem
  },
  computed: {
      table_height(){
          return (this.dataSource.length+3)*40;
      }
  },
  props:{
      dataSource:{
          type:Array,
          default:()=>{
              return [];
          }
      }
  },
  data: () => ({
  })
};
</script>

<style scoped>
.cell {
  padding-top: 10px;
}
.title-wrapper {
  border-bottom: 1px solid #ffffff;
}
.cell-wrapper {
  border-bottom: 1px solid #6b7289;
}
.darker {
  background: #313854;
}

</style>

