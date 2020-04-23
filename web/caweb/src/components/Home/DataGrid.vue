<template>
  <div class="wrapper">
    <DxBox :height="table_height" direction="col" width="100%">
      <!-- title -->
      <DxItem :ratio="1">
        <template #default>
          <div class="title-wrapper">
            <DxBox :height="40" direction="row" width="100%">
              <DxItem :ratio="2">
                <template #default>
                  <div class="cell">日期</div>
                </template>
              </DxItem>
              <DxItem :ratio="2">
                <template #default>
                  <div class="cell">地图</div>
                </template>
              </DxItem>
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
      <DxItem :ratio="10">
        <template #default>
          <div>
            <div
              class="cell-wrapper"
              v-for="(item,index) in dataSource"
              :key="index"
              :class="{'darker':(index%2==1)}"
            >
              <DxBox :height="40" direction="row" width="100%">
                <DxItem :ratio="2">
                  <template #default>
                    <div class="cell">{{item.date}}</div>
                  </template>
                </DxItem>
                <DxItem :ratio="2">
                  <template #default>
                    <div class="cell">{{item.map}}</div>
                  </template>
                </DxItem>
                <DxItem :ratio="3">
                  <template #default>
                    <div class="cell">{{item.player}} ({{item.player_race}})</div>
                  </template>
                </DxItem>
                <DxItem :ratio="2">
                  <template #default>
                    <div class="cell">{{item.play_MMR}}</div>
                  </template>
                </DxItem>
                <DxItem :ratio="3">
                  <template #default>
                    <div class="cell">{{item.opponent}} ({{item.opponent_race}})</div>
                  </template>
                </DxItem>
                <DxItem :ratio="2">
                  <template #default>
                    <div class="cell">{{item.opponent_MMR}}</div>
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
                    <div class="cell have_look" @click="get_rep(item)">查看</div>
                  </template>
                </DxItem>
              </DxBox>
            </div>
          </div>
        </template>
      </DxItem>
      <DxItem :ratio="2">
        <template #default></template>
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
    table_height() {
      return (this.dataSource.length + 3) * 40;
    }
  },
  props: {
    dataSource: {
      type: Array,
      default: () => {
        return [];
      }
    }
  },
  data: () => ({}),
  methods: {
    get_rep(item) {
      let rep_id = item.rep_id;
      let url = "https://sc2replaystats.com/replay/" + rep_id;
      window.open(url, "_blank");
    }
  }
};
</script>

<style scoped>
.cell {
  padding-top: 10px;
  overflow: hidden;
  white-space: nowrap;
  height: 100%;
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
.have_look {
  cursor: pointer;
}
</style>

