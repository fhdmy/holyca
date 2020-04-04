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
                              <label class="active-score">{{active_score_show}}</label>
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
                              <label class="mmr-score">{{mmr_score_show}}</label>
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
    active_timer:"",
    imba_timer:"",
    mmr_timer:"",
    active_score_show:0,
    active_score:0,
    active_max_value:200,
    active_palette:"Pastel",
    active_graph:[],
    mmr_score:0,
    mmr_score_show:0,
    mmr_max_value:6000,
    mmr_palette:"Violet",
    mmr_players : [],
    mmr_players_mmr : [],
    imba_most:"P",
    imba_vs:['TVP','PVZ','ZVT'],
    imba_rate:[],
    imba_palette:"Soft Blue",
    imba_sums:[
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
    ],
    reps:[]
  }),
  created() {
    this.active_statistics();
    this.replay_statistics();
    this.racesum_statistics();
    this.raceimba_statistics();
    this.mmr_statistics();
  },
  beforeDestroy() {
    clearInterval(this.active_timer);
    clearInterval(this.imba_timer);
    clearInterval(this.mmr_timer);
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
    },
    active_statistics(){
      this.$http({
        method: "get",
        url: "/api/match/active_statistics/",
        headers: {
          "Authorization": this.token
        },
      })
        .then(res => {
          console.log(res);
          let sum=0;
          // 取盘数非0的账号
          let acc_not_zero=0;
          for(let k=0;k<res.data.length;k++){
            sum+=res.data[k].sum;
            if(res.data[k].sum!=0)
              acc_not_zero+=1;
          }
          let old_val=this.active_score;
          if(this.active_score_show != sum)
            this.active_timer=setInterval(()=>{
              this.active_score_show=this.active_score_show+parseInt((sum-old_val+50)/50);
              if(this.active_score_show >= sum){
                this.active_score_show = sum;
                clearInterval(this.active_timer);
              }
            },10)
          this.active_score=sum;
          if(acc_not_zero*200>sum)
            this.active_max_value=acc_not_zero*200;
          else
            this.active_max_value=sum;
          //排序，取前8
          for(let i=0;i<res.data.length-1;i++){
            for(let j=0;j<i;j++){
              if(res.data[j].sum<res.data[j+1].sum){
                let temp=res.data[j].sum;
                res.data[j].sum=res.data[j+1].sum;
                res.data[j+1].sum=temp;
              }
            }
          }
          for(let k=0;k<(res.data.length<8?res.data.length:8);k++){
            this.$set(this.active_graph,k,{
              teammate: res.data[k].account,
              reps: res.data[k].sum
            });
          }
        })
        .catch(error => {
          console.log(error.response);
          notify("请检查你的网络!", "error", 1500);
        });
    },
    replay_statistics(){
      this.$http({
        method: "get",
        url: "/api/match/replay_statistics/",
        headers: {
          "Authorization": this.token
        },
      })
        .then(res => {
          console.log(res);
          for(let k=0;k<res.data.length;k++){
            let game_map;
            game_map=res.data[k].game_map.split("-天梯版")[0];
            this.$set(this.reps,k,{
              player:res.data[k].player1.battlenet_name,
              play_MMR: res.data[k].player1_mmr,
              player_race: res.data[k].vs_race.split("v")[0],
              opponent: res.data[k].player2.battlenet_name,
              opponent_MMR: res.data[k].player2_mmr,
              opponent_race: res.data[k].vs_race.split("v")[1],
              game_length: res.data[k].game_length,
              winner: res.data[k].winner,
              map:game_map,
              date:res.data[k].date,
              rep_id:res.data[k].rep_id
            });
          }
        })
        .catch(error => {
          console.log(error.response);
          notify("请检查你的网络!", "error", 1500);
        });
    },
    racesum_statistics(){
      this.$http({
        method: "get",
        url: "/api/match/racesum_statistics/",
        headers: {
          "Authorization": this.token
        },
      })
        .then(res => {
          console.log(res);
          this.$set(this.imba_sums,0,{
            race:"P",
            sum:res.data[0].sum
          });
          this.$set(this.imba_sums,1,{
            race:"Z",
            sum:res.data[1].sum
          });
          this.$set(this.imba_sums,2,{
            race:"T",
            sum:res.data[2].sum
          });
        })
        .catch(error => {
          console.log(error.response);
          notify("请检查你的网络!", "error", 1500);
        });
    },
    raceimba_statistics(){
      this.$http({
        method: "get",
        url: "/api/match/race_winrate_statistics/",
        headers: {
          "Authorization": this.token
        },
      })
        .then(res => {
          console.log(res);
          for(let k=0;k<res.data.length;k++){
            this.$set(this.imba_rate,k,{
              date:res.data[k].date,
              TVP:res.data[k].TVP,
              PVZ:res.data[k].PVZ,
              ZVT:res.data[k].ZVT,
              index:k+1
            })
          }
          let T=res.data[res.data.length-1].TVP+(100-res.data[res.data.length-1].ZVT);
          let P=res.data[res.data.length-1].PVZ+(100-res.data[res.data.length-1].TVP);
          let Z=res.data[res.data.length-1].ZVT+(100-res.data[res.data.length-1].PVZ);
          let max_rate=0;
          let IMBA="P";
          if(T>P){
            IMBA="T";
            max_rate=T;
          }else{
            IMBA="P";
            max_rate=P;
          }
          if(Z>max_rate){
            IMBA="Z";
            max_rate=Z;
          }
          let i=0;
          this.imba_timer=setInterval(()=>{
            let temp;
            if(i%3==0)
              temp="P"
            else if(i%3==1)
              temp="Z"
            else if(i%3==2)
              temp="T"
            this.imba_most=temp;
            i+=1;
            if(i == 10){
              clearInterval(this.imba_timer);
              this.imba_most=IMBA;
            }
          },60)
        })
        .catch(error => {
          console.log(error.response);
          notify("请检查你的网络!", "error", 1500);
        });
    },
    mmr_statistics(){
      this.$http({
        method: "get",
        url: "/api/match/mmr_statistics/",
        headers: {
          "Authorization": this.token
        },
      })
        .then(res => {
          console.log(res);
          for(let m=0;m<res.data[0].length;m++){
            this.$set(this.mmr_players,m,res.data[0][m].name);
          }
          for(let m=0;m<res.data.length;m++){
            this.$set(this.mmr_players_mmr,m,{});
            for(let n=0;n<res.data[m].length;n++){
              this.$set(this.mmr_players_mmr[m],res.data[m][n].name,res.data[m][n].mmr);
            }
            this.$set(this.mmr_players_mmr[m],"index",m);
          }
          let mmr_sum=0;
          for(let k=0;k<res.data[11].length;k++){
            mmr_sum+=res.data[11][k].mmr;
          }
          let avg_mmr=parseInt(mmr_sum/res.data[11].length);
          let old_val=this.mmr_score;
          if(this.mmr_score_show != avg_mmr)
            this.mmr_timer=setInterval(()=>{
              this.mmr_score_show=this.mmr_score_show+parseInt((avg_mmr-old_val+100)/100);
              if(this.mmr_score_show >= avg_mmr){
                this.mmr_score_show = avg_mmr;
                clearInterval(this.mmr_timer);
              }
            },5)
          this.mmr_score=avg_mmr;
        })
        .catch(error => {
          console.log(error.response);
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

