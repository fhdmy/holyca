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
                <div class="main-title" @click="sign_in()"><span>Team HolyCA</span></div>
              </template>
            </DxItem>

            <!-- ######## -->
            <!-- ######## -->
            <!-- 活跃度框架 -->
            <DxItem :ratio="3">
              <template #default>
                <DxBox :height="200" direction="col" width="100%">
                  <!-- sub-title -->
                  <DxItem :ratio="1">
                    <template #default>
                      <DxBox :height="25" direction="row" width="100%">
                        <DxItem :ratio="1">
                          <template #default>
                            <div class="sub-title">活跃度</div>
                          </template>
                        </DxItem>
                        <DxItem :ratio="16">
                          <template #default>
                            <div class="hr"></div>
                          </template>
                        </DxItem>
                      </DxBox>
                    </template>
                  </DxItem>
                  <!-- sub-content -->
                  <DxItem :ratio="7">
                    <template #default>
                      <DxBox :height="175" direction="row" width="100%">
                        <!-- 说明部分 -->
                        <DxItem :ratio="3">
                          <template #default>
                            <div>
                              <div class="explain-content">查看本周上传REP的总数，右边展示了较活跃的玩家上传的REP数量。</div>
                              <label class="active-score">{{active_score}}</label>
                            </div>
                          </template>
                        </DxItem>
                        <!-- 仪表盘 -->
                        <DxItem :ratio="3">
                          <template #default>
                            <gauge :score="active_score" 
                            :max_value="active_max_value"
                            :palette="active_palette"></gauge>
                          </template>
                        </DxItem>
                        <!-- 图表 -->
                        <DxItem :ratio="7">
                          <template #default>
                            <barChart :dataSource="active_graph"></barChart>
                          </template>
                        </DxItem>
                      </DxBox>
                    </template>
                  </DxItem>
                </DxBox>
              </template>
            </DxItem>

            <!-- ######## -->
            <!-- ######## -->
            <!-- MMR框架 -->
            <DxItem :ratio="4">
              <template #default>
                <DxBox :height="266" direction="col" width="100%">
                  <!-- sub-title -->
                  <DxItem :ratio="1">
                    <template #default>
                      <DxBox :height="25" direction="row" width="100%">
                        <DxItem :ratio="1">
                          <template #default>
                            <div class="sub-title">MMR</div>
                          </template>
                        </DxItem>
                        <DxItem :ratio="16">
                          <template #default>
                            <div class="hr"></div>
                          </template>
                        </DxItem>
                      </DxBox>
                    </template>
                  </DxItem>
                  <!-- sub-content -->
                  <DxItem :ratio="7">
                    <template #default>
                      <DxBox :height="175" direction="row" width="100%">
                        <!-- 说明部分 -->
                        <DxItem :ratio="3">
                          <template #default>
                            <div>
                              <div class="explain-content">查看站内玩家平均MMR值，右图所示为玩家的MMR变化趋势。</div>
                              <label class="mmr-score">{{mmr_score}}</label>
                            </div>
                          </template>
                        </DxItem>
                        <!-- 仪表盘 -->
                        <DxItem :ratio="3">
                          <template #default>
                            <gauge :score="mmr_score" 
                            :max_value="mmr_max_value"
                            :palette="mmr_palette"></gauge>
                          </template>
                        </DxItem>
                        <!-- 图表 -->
                        <DxItem :ratio="7">
                          <template #default>
                            <lineChart :players="mmr_players" 
                            :players_mmr="mmr_players_mmr"
                            :palette="mmr_palette"
                            ></lineChart>
                          </template>
                        </DxItem>
                      </DxBox>
                    </template>
                  </DxItem>
                </DxBox>
              </template>
            </DxItem>

            <!-- ######## -->
            <!-- ######## -->
            <!-- 种族胜率框架 -->
            <DxItem :ratio="4">
              <template #default>
                <DxBox :height="266" direction="col" width="100%">
                  <!-- sub-title -->
                  <DxItem :ratio="1">
                    <template #default>
                      <DxBox :height="25" direction="row" width="100%">
                        <DxItem :ratio="1">
                          <template #default>
                            <div class="sub-title">IMBA</div>
                          </template>
                        </DxItem>
                        <DxItem :ratio="16">
                          <template #default>
                            <div class="hr"></div>
                          </template>
                        </DxItem>
                      </DxBox>
                    </template>
                  </DxItem>
                  <!-- sub-content -->
                  <DxItem :ratio="7">
                    <template #default>
                      <DxBox :height="175" direction="row" width="100%">
                        <!-- 说明部分 -->
                        <DxItem :ratio="3">
                          <template #default>
                            <div>
                              <div class="explain-content">本月最IMBA的种族是？右图展示了录像中对手是各种族的盘数，以及三族对抗胜率变化趋势。</div>
                              <label class="imba-score">{{imba_most}}</label>
                            </div>
                          </template>
                        </DxItem>
                        <!-- 雷达图 -->
                        <DxItem :ratio="3">
                          <template #default>
                            <pieChart :dataSource="imba_sums" :palette="imba_palette"></pieChart>
                          </template>
                        </DxItem>
                        <!-- 图表 -->
                        <DxItem :ratio="7">
                          <template #default>
                            <lineChart :players="imba_vs" 
                            :players_mmr="imba_rate"
                            :palette="imba_palette"
                            ></lineChart>
                          </template>
                        </DxItem>
                      </DxBox>
                    </template>
                  </DxItem>
                </DxBox>
              </template>
            </DxItem>

            <!-- ######## -->
            <!-- ######## -->
            <!-- REP框架 -->
            <DxItem :ratio="3">
              <template #default>
                <DxBox :height="200" direction="col" width="100%">
                  <!-- sub-title -->
                  <DxItem :ratio="1">
                    <template #default>
                      <DxBox :height="25" direction="row" width="100%">
                        <DxItem :ratio="1">
                          <template #default>
                            <div class="sub-title">录像</div>
                          </template>
                        </DxItem>
                        <DxItem :ratio="16">
                          <template #default>
                            <div class="hr"></div>
                          </template>
                        </DxItem>
                      </DxBox>
                    </template>
                  </DxItem>
                  <!-- sub-content -->
                  <DxItem :ratio="7">
                    <template #default>
                      <dataGrid :dataSource="reps"></dataGrid>
                    </template>
                  </DxItem>
                </DxBox>
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
    <div class="left-icon" @click="switchPage('left')"><i class="dx-icon-chevronleft icon-left"></i></div>
    <div class="right-icon" @click="switchPage('right')"><i class="dx-icon-chevronright icon-right"></i></div>
  </div>
</template>

<script>
import { DxBox, DxItem } from "devextreme-vue/box";
import notify from 'devextreme/ui/notify';
import Gauge from "./Gauge.vue";
import BarChart from "./BarChart.vue";
import LineChart from "./LineChart.vue";
import PieChart from "./PieChart.vue";
import DataGrid from "./DataGrid.vue";
 
export default {
  components: {
    DxBox,
    DxItem,
    Gauge,
    BarChart,
    LineChart,
    PieChart,
    DataGrid,
  },

  data: () => ({
    token:localStorage.getItem("token") == null
        ? ""
        : "Token " + localStorage.getItem("token"),
    active_score:153,
    active_max_value:200,
    active_palette:"Pastel",
    active_graph : [{
      teammate: 'Xnick',
      reps: 40
    }, {
      teammate: '星之所在',
      reps: 10
    }, {
      teammate: 'Fungal',
      reps: 3
    }, {
      teammate: 'Almee',
      reps: 120
    }],
    mmr_score:4436,
    mmr_max_value:6000,
    mmr_palette:"Violet",
    mmr_players : ['fungal','Xnick','送饭人族','星之所在','SHKStarlight'],
    mmr_players_mmr : [
    {
        month:1,
        fungal: 4200,
        Xnick: 5000,
        送饭人族: 4400,
        星之所在: 5300,
        SHKStarlight:4600
    },
    {
        month:2,
        fungal: 4150,
        Xnick: 5100,
        送饭人族: 4400,
        星之所在: 4900,
        SHKStarlight:4650
    },
    {
        month:3,
        fungal: 4330,
        Xnick: 5010,
        送饭人族: 4400,
        星之所在: 4830,
        SHKStarlight:4610
    },
    {
        month:4,
        fungal: 4420,
        Xnick: 5100,
        送饭人族: 4420,
        星之所在: 3800,
        SHKStarlight:4700
    },
    {
        month:5,
        fungal: 4220,
        Xnick: 5200,
        送饭人族: 4420,
        星之所在: 3300,
        SHKStarlight:4730
    },
    {
        month:6,
        fungal: 4000,
        Xnick: 5100,
        送饭人族: 4450,
        星之所在: 3500,
        SHKStarlight:4800
    },
    {
        month:7,
        fungal: 4050,
        Xnick: 4950,
        送饭人族: 4450,
        星之所在: 4500,
        SHKStarlight:4700
    },
    {
        month:8,
        fungal: 4150,
        Xnick: 4850,
        送饭人族: 4450,
        星之所在: 4200,
        SHKStarlight:4750
    },
    {
        month:9,
        fungal: 4150,
        Xnick: 5000,
        送饭人族: 4430,
        星之所在: 4800,
        SHKStarlight:4800
    },
    {
        month:10,
        fungal: 4060,
        Xnick: 5010,
        送饭人族: 4450,
        星之所在: 4700,
        SHKStarlight:4900
    },
    {
        month:11,
        fungal: 4000,
        Xnick: 4950,
        送饭人族: 4500,
        星之所在: 4800,
        SHKStarlight:4800
    },
    {
        month:12,
        fungal: 4150,
        Xnick: 4950,
        送饭人族: 4500,
        星之所在: 4700,
        SHKStarlight:4950
    }],
    imba_most:"P",
    imba_vs:['TVP','PVZ','ZVT'],
    imba_rate:[
      {
        month:1,
        TVP: 41.4,
        PVZ: 46.2,
        ZVT: 58.1,
      },
      {
        month:2,
        TVP: 42.2,
        PVZ: 42.8,
        ZVT: 53.1,
      },
      {
        month:3,
        TVP: 38.2,
        PVZ: 40.8,
        ZVT: 61.1,
      },
      {
        month:4,
        TVP: 41.2,
        PVZ: 42.8,
        ZVT: 55.1,
      },
      {
        month:5,
        TVP: 45.4,
        PVZ: 48.5,
        ZVT: 57.6,
      },
      {
        month:6,
        TVP: 44.5,
        PVZ: 42.2,
        ZVT: 53.4,
      },
      {
        month:7,
        TVP: 44.1,
        PVZ: 51.2,
        ZVT: 52.5,
      },
      {
        month:8,
        TVP: 42.2,
        PVZ: 49.8,
        ZVT: 52.1,
      },
      {
        month:9,
        TVP: 49.2,
        PVZ: 51.1,
        ZVT: 50.9,
      },
      {
        month:10,
        TVP: 45.2,
        PVZ: 42.1,
        ZVT: 49.6,
      },
      {
        month:11,
        TVP: 43.1,
        PVZ: 55.2,
        ZVT: 55.5,
      },
      {
        month:12,
        TVP: 47.7,
        PVZ: 51.1,
        ZVT: 51.6,
      },
    ],
    imba_palette:"Soft Blue",
    imba_sums:[
      {
        race: "P",
        sum: 120
      },
      {
        race: "Z",
        sum: 50
      },
      {
        race: "T",
        sum: 95
      }
    ],
    reps:[
      {
        player: "Xnick",
        play_MMR: 4800,
        player_race: "T",
        opponent: "蛇口",
        opponent_MMR: 4900,
        opponent_race: "Z",
        game_length: "39:10",
        winner: "Xnick"
      },
      {
        player: "SHKstarlght",
        play_MMR: 4900,
        player_race: "T",
        opponent: "Drima",
        opponent_MMR: 4900,
        opponent_race: "T",
        game_length: "21:25",
        winner: "SHKstarlght"
      }],
  }),
  mounted() {
    
  },
  methods: {
    switchPage(a){
      if(a=="left")
        this.$router.push({
          name: 'ownpage'
        })
      else
        this.$router.push({
          name: 'activitypage'
        })
    },
    sign_in(){
      this.$http({
        method: "post",
        url: "/api/account/teammates/signin/",
        headers: {
          "Authorization": this.token
        },
      })
        .then(res => {
          console.log(res);
          notify("签到成功!", "success", 1500);
        })
        .catch(error => {
          console.log(error.response);
          if(error.response.data=="User has signined today")
            notify("不能重复签到!", "error", 1500);
          else
            notify("请检查你的网络!", "error", 1500);
        });
    }
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
.main-title span{
  cursor: pointer;
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
  bottom: 65%;
}
.explain-content{
  padding-top: 10px;
  font-size: 11px;
  color: #8e93a7;
}
.active-score{
  color: #7cd2c7;
  font-size: 60px;
  font-weight: 600;
}
.mmr-score{
  color: #D0B2DA;
  font-size: 60px;
  font-weight: 600;
}
.imba-score{
  color: #75c0e0;
  font-size: 60px;
  font-weight: 600;
}
.left-icon{
  background: white;
  border-radius: 0 60px 60px 0;
  width: 30px;
  height: 60px;
  position: absolute;
  top:400px;
  left:-4px;
  cursor: pointer;
}
.right-icon{
  background: white;
  border-radius: 60px 0 0 60px;
  width: 30px;
  height: 60px;
  position: absolute;
  top:400px;
  right:-4px;
  cursor: pointer;
}
.icon-left{
  font-size: 22px;
  color:#1c1f2b;
  position: relative;
  top: 18px;
  left:3px;
}
.icon-right{
  font-size: 22px;
  color:#1c1f2b;
  position: relative;
  top: 18px;
  left:4px;
}
</style>

