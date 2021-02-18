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
                <div class="main-title"><span>队内交流</span></div>
              </template>
            </DxItem>

            <!-- ######## -->
            <!-- ######## -->
            <!-- 比赛框架 -->
            <DxItem :ratio="3">
              <template #default>
                <DxBox :height="200" direction="col" width="100%">
                  <!-- sub-title -->
                  <DxItem :ratio="1">
                    <template #default>
                      <DxBox :height="25" direction="row" width="100%">
                        <DxItem :ratio="1">
                          <template #default>
                            <div class="sub-title">比赛</div>
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
                            
                          </template>
                        </DxItem>
                        <!-- 仪表盘 -->
                        <DxItem :ratio="3">
                          <template #default>
                            
                          </template>
                        </DxItem>
                        <!-- 图表 -->
                        <DxItem :ratio="7">
                          <template #default>

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
            <!-- 积分框架 -->
            <DxItem :ratio="5">
              <template #default>
                <DxBox :height="266" direction="col" width="100%">
                  <!-- sub-title -->
                  <DxItem :ratio="1">
                    <template #default>
                      <DxBox :height="20" direction="row" width="100%">
                        <DxItem :ratio="1">
                          <template #default>
                            <div class="sub-title">积分</div>
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
                      <div style="position:relative;">
                        <DxBox :height="25" direction="row" width="100%">
                          <DxItem :ratio="16">
                            <template #default>
                            </template>
                          </DxItem>
                          <DxItem :ratio="1">
                            <template #default>
                              <p class="more-btn" @click="switch_to_bet()">查看更多</p>
                            </template>
                          </DxItem>
                        </DxBox>
                        <betList :dataSource="bets" :score.sync="score" :token="token"></betList>
                      </div>
                    </template>
                  </DxItem>
                </DxBox>
              </template>
            </DxItem>

            <!-- ######## -->
            <!-- ######## -->
            <!-- 论坛框架 -->
            <DxItem :ratio="5">
              <template #default>
                <DxBox :height="266" direction="col" width="100%">
                  <!-- sub-title -->
                  <DxItem :ratio="1">
                    <template #default>
                      <DxBox :height="20" direction="row" width="100%">
                        <DxItem :ratio="1">
                          <template #default>
                            <div class="sub-title">论坛</div>
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
                      <div style="position:relative;">
                        <DxBox :height="25" direction="row" width="100%">
                          <DxItem :ratio="16">
                            <template #default>
                            </template>
                          </DxItem>
                          <DxItem :ratio="1">
                            <template #default>
                              <p class="more-btn" @click="switch_to_forum()" v-if="false">查看更多</p>
                            </template>
                          </DxItem>
                        </DxBox>
                        <forumOuter v-if="false"></forumOuter>
                      </div>
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
    <div class="left-icon" @click="switchPage()"><i class="dx-icon-chevronleft icon-left"></i></div>
  </div>
</template>
<script>
import { DxBox, DxItem } from "devextreme-vue/box";
import ForumOuter from "./ForumOuter.vue";
import BetList from "./BetList.vue";
import notify from 'devextreme/ui/notify';

export default {
  components: {
    DxBox,
    DxItem,
    ForumOuter,
    BetList,
  },
  props: {},
  data: () => ({
    token:localStorage.getItem("token") == null
        ? ""
        : "Token " + localStorage.getItem("token"),
    has_login:false,
    score:0,
    bets:[]
  }),
  created() {
    this.get_bets();
      if(this.token!=""){
        this.get_score();
      }
  },
  methods: {
    switchPage() {
      this.$router.push({
        name: "homepage"
      });
    },
    switch_to_forum(){
      let routeData = this.$router.resolve({ path: '/forum_page'});
      window.open(routeData.href, '_blank');
    },
    switch_to_bet(){
      let routeData = this.$router.resolve({ path: '/bet_page'});
      window.open(routeData.href, '_blank');
    },
    get_bets(){
      this.$http({
        method: "get",
        url: "/api/activity/bet/get_bets/?sum=3",
        // headers: {
        //   "Authorization": this.token
        // },
      })
        .then(res => {
          console.log(res);
          for(let k=0;k<res.data.length;k++){
            let t_split=res.data[k].time.split("T")
            let year=t_split[0].split("-")[0]
            let month=t_split[0].split("-")[1]
            let day=t_split[0].split("-")[2]
            let hour=t_split[1].split(":")[0]
            let minute=t_split[1].split(":")[1]
            let time=year+"-"+month+"-"+day+"  "+hour+":"+minute;
            let dt=new Date(year,month-1,day,hour,minute);
            let now=new Date()
            let last="";
            if(dt<now || dt==now){
              if(res.data[k].finished)
                last="已结束";
              else
                last="正在进行中";
            }
            else{
              let d = Math.floor((dt-now)/(24*60*60*1000));
              let h = Math.floor((dt-now)/60/60/1000-(d*24));
              let m = Math.floor((dt-now)/60/1000-(h*60)-(d*24*60));
              last=d+"天"+h+"小时"+m+"分钟";
            }

            this.$set(this.bets,k,{
              id:res.data[k].id,
              player_1:res.data[k].player_1,
              player_2:res.data[k].player_2,
              tournament:res.data[k].tournament,
              match_url:res.data[k].match_url,
              time:time,
              time_visible:false,
              last:last,
              input_bet:0,
              bet_1:res.data[k].bet_1,
              bet_2:res.data[k].bet_2,
              finished:res.data[k].finished,
              stop_bet:res.data[k].stop_bet
            })
          }

          this.bets_timer=setInterval(()=>{
              for(let i=0;i<this.bets.length;i++){
                if(this.bets.last=="正在进行中" || this.bets.last=="已结束")
                  continue
                let year=this.bets[i].time.split("  ")[0].split("-")[0];
                let month=this.bets[i].time.split("  ")[0].split("-")[1];
                let day=this.bets[i].time.split("  ")[0].split("-")[2];
                let hour=this.bets[i].time.split("  ")[1].split(":")[0];
                let minute=this.bets[i].time.split("  ")[1].split(":")[1];
                let dt=new Date(year,month-1,day,hour,minute);
                let now=new Date()
                let last="";
                if(dt<now || dt==now){
                  last="正在进行中";
                }
                else{
                  let d = Math.floor((dt-now)/(24*60*60*1000));
                  let h = Math.floor((dt-now)/60/60/1000-(d*24));
                  let m = Math.floor((dt-now)/60/1000-(h*60)-(d*24*60));
                  last=d+"天"+h+"小时"+m+"分钟";
                }
                this.$set(this.bets[i],"last",last)
              }
          },60000)
        })
        .catch(error => {
          console.log(error.response);
          notify("请检查你的网络!", "error", 1500);
        });
    },
    get_score(){
      this.$http({
        method: "get",
        url: "/api/account/teammates/get_score/",
        headers: {
          "Authorization": this.token
        },
      })
        .then(res => {
          // console.log(res);
          this.score=res.data;
          this.has_login=true;
        })
        .catch(error => {
          console.log(error.response);
          if(error.response.statusText=="Unauthorized"){
            notify("账户未登录或登录状态错误!", "error", 1500);
          }
          else
            notify("获取信息失败!", "error", 1500);
          this.has_login=false;
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
.left-icon {
  background: white;
  border-radius: 0 60px 60px 0;
  width: 30px;
  height: 60px;
  position: absolute;
  top: 400px;
  left: -4px;
  cursor: pointer;
}
.icon-left {
  font-size: 22px;
  color: #1c1f2b;
  position: relative;
  top: 18px;
  left: 3px;
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
  bottom: 68%;
}
.more-btn{
  cursor: pointer;
  text-align: right;
  width: 100%;
  margin: 0;
}
</style>
