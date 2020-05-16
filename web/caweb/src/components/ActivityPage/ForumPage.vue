<template>
  <div class="wrapper">
    <DxBox :height="1200" direction="row" width="100%">
      <DxItem :ratio="1">
        <template #default></template>
      </DxItem>

      <!-- main -->
      <DxItem :ratio="6">
        <template #default>
          <DxBox :height="1200" direction="col" width="100%">
            <!-- Main Title -->
            <DxItem :ratio="2">
              <template #default>
                <div class="main-title"><span>论坛专区</span></div>
              </template>
            </DxItem>

            <!-- ######## -->
            <!-- ######## -->
            <!-- 比赛框架 -->
            <DxItem :ratio="13">
              <template #default>
                <div>
                  <forum></forum>
                  <DxLoadPanel
                    :position="position"
                    :visible.sync="rep_loading_visible"
                    :show-indicator="true"
                    :show-pane="true"
                    :shading="true"
                    :close-on-outside-click="false"
                    shading-color="rgba(0,0,0,0.4)"
                  />
                </div>
              </template>
            </DxItem>
            <DxItem :ratio="2">
              <template #default></template>
            </DxItem>
          </DxBox>
        </template>
      </DxItem>

      <DxItem :ratio="1">
        <template #default></template>
      </DxItem>
    </DxBox>
  </div>
</template>
<script>
import { DxBox, DxItem } from "devextreme-vue/box";
import notify from 'devextreme/ui/notify';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import Forum from "./Forum.vue";

export default {
  components: {
    DxBox,
    DxItem,
    DxLoadPanel,
    Forum
  },
  props: {},
  data: () => ({
      token:localStorage.getItem("token") == null
        ? ""
        : "Token " + localStorage.getItem("token"),
      reps:[],
      rep_loading_visible: true,
      position: { of: '#datatable' },
  }),
  created() {
      this.replay_statistics();
      this.rep_loading_visible=true;
  },
  methods: {
    replay_statistics(){
      this.$http({
        method: "get",
        url: "/api/match/replay_statistics/?replays=-1",
        headers: {
          "Authorization": this.token
        },
      })
        .then(res => {
          // console.log(res);
          for(let k=0;k<res.data.length;k++){
            let game_map;
            game_map=res.data[k].game_map.split("-天梯版")[0];
            this.$set(this.reps,k,{
              player:res.data[k].player1.battlenet_name+" ("+res.data[k].vs_race.split("v")[0]+")",
              player_MMR: res.data[k].player1_mmr,
              opponent: res.data[k].player2.battlenet_name+" ("+res.data[k].vs_race.split("v")[1]+")",
              opponent_MMR: res.data[k].player2_mmr,
              game_length: res.data[k].game_length,
              winner: res.data[k].winner,
              map:game_map,
              date:res.data[k].date,
              rep_id:res.data[k].rep_id,
              date_show:res.data[k].date.split("T")[0]
            });
          }
          this.rep_loading_visible=false;
        })
        .catch(error => {
          console.log(error.response);
          this.rep_loading_visible=false;
          notify("请检查你的网络!", "error", 1500);
        });
    },
  }
};
</script>
<style scoped>
.wrapper {
  display: block;
  position: relative;
}
DxItem {
  position: relative;
}
.main-title {
  font-size: 28px;
  padding-top: 5%;
  height: 100%;
  color: white;
  font-weight: 250;
  font-family: 'Segoe UI Light', 'Helvetica Neue Light', 'Segoe UI', 'Helvetica Neue', Helvetica, 'Trebuchet MS', 'Droid Sans', Tahoma, Geneva, sans-serif;
}
.sub-title-wrapper {
  display: flex;
  flex-wrap: nowrap;
  flex-direction: row;
}
.sub-title {
  font-size: 16px;
  color: white;
  font-weight: 250;
  font-family: 'Segoe UI Light', 'Helvetica Neue Light', 'Segoe UI', 'Helvetica Neue', Helvetica, 'Trebuchet MS', 'Droid Sans', Tahoma, Geneva, sans-serif;
}
.hr {
  width: 100%;
  height: 10px;
  border-bottom: 1px solid #6b7289;
  position: relative;
  bottom: 75%;
}
</style>
