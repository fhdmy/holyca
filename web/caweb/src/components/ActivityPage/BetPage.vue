<template>
  <div class="wrapper">
    <DxBox :height="1800" direction="row" width="100%">
      <DxItem :ratio="1">
        <template #default></template>
      </DxItem>

      <!-- main -->
      <DxItem :ratio="6" id="datatable">
        <template #default>
          <DxBox :height="1800" direction="col" width="100%">
            <!-- Main Title -->
            <DxItem :ratio="2">
              <template #default>
                <div class="main-title"><span>积分专区</span></div>
              </template>
            </DxItem>

            <!-- ######## -->
            <!-- ######## -->
            <!-- 日程表 -->
            <DxItem :ratio="10">
              <template #default>
                <div>
                  <scheduler :dataSource="matches" id="myscheduler"></scheduler>
                  <DxLoadPanel
                    :position="position"
                    :visible.sync="loading_visible"
                    :show-indicator="true"
                    :show-pane="true"
                    :shading="true"
                    :close-on-outside-click="false"
                    shading-color="rgba(0,0,0,0.4)"
                  />
                </div>
              </template>
            </DxItem>

            <DxItem :ratio="1">
              <template #default></template>
            </DxItem>

            <!-- ######## -->
            <!-- ######## -->
            <!-- 积分框架 -->
            <DxItem :ratio="18">
              <template #default>
                <div>
                  <p class="more-btn" @click="ownbet_open()">历史记录</p>
                  <DxPopup
                    :visible.sync="ownbet_popup_visible"
                    :drag-enabled="false"
                    :close-on-outside-click="false"
                    :show-title="true"
                    :width="1000"
                    title="历史记录"
                  >
                    <template #content>
                      <betOwn :dataSource="own_bets"></betOwn>
                    </template>
                  </DxPopup>
                  <betList :dataSource="bets" :score.sync="score" :token="token"></betList>
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
import BetList from "./BetList.vue";
import BetOwn from "./BetOwn.vue";
import Scheduler from "./Scheduler.vue";
import { DxPopup } from 'devextreme-vue/popup';

export default {
  components: {
    DxBox,
    DxItem,
    DxLoadPanel,
    BetList,
    Scheduler,
    DxPopup,
    BetOwn
  },
  props: {},
  data: () => ({
      token:localStorage.getItem("token") == null
        ? ""
        : "Token " + localStorage.getItem("token"),
      reps:[],
      loading_visible: true,
      position: { of: '#myscheduler' },
      matches:[],
      bets:[],
      own_bets:[],
      bets_timer:"",
      ownbets_timer:"",
      has_login:false,
      score:0,
      ownbet_popup_visible:false,
  }),
  created() {
      this.loading_visible=true;
      this.match_scheduler();
      this.get_bets();
      if(this.token!=""){
        this.get_score();
        this.get_own_bets();
      }
  },
  beforeDestroy() {
    clearInterval(this.bets_timer);
    clearInterval(this.ownbets_timer);
  },
  methods: {
    match_scheduler(){
      this.$http({
        method: "get",
        url: "/api/activity/match_scheduler/",
        headers: {
          "Authorization": this.token
        },
      })
        .then(res => {
          for(let k=0;k<res.data.length;k++){
            // 得到的只是开始时间，需加预估结束时间
            let start_split=res.data[k].start_time.split("T")
            let start_year=start_split[0].split("-")[0]
            let start_month=start_split[0].split("-")[1]-1
            let start_day=start_split[0].split("-")[2]
            let start_hour=start_split[1].split(":")[0]
            let start_minute=start_split[1].split(":")[1]

            let end_split=res.data[k].end_time.split("T")
            let end_year=end_split[0].split("-")[0]
            let end_month=end_split[0].split("-")[1]-1
            let end_day=end_split[0].split("-")[2]
            let end_hour=parseInt(end_split[1].split(":")[0])
            end_hour+=2;              
            let end_minute=end_split[1].split(":")[1]

            this.$set(this.matches,k,{
              text:res.data[k].tournament,
              startDate: new Date(start_year, start_month, start_day, start_hour, start_minute),
              endDate: new Date(end_year, end_month, end_day, end_hour, end_minute),
            })
          }
          this.loading_visible=false;
        })
        .catch(error => {
          console.log(error.response);
          this.loading_visible=false;
          notify("请检查你的网络!", "error", 1500);
        });
    },
    get_bets(){
      this.$http({
        method: "get",
        url: "/api/activity/bet/get_bets/?sum=-1",
        headers: {
          "Authorization": this.token
        },
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
    get_own_bets(){
      this.$http({
        method: "get",
        url: "/api/activity/bet/get_own_bets/",
        headers: {
          "Authorization": this.token
        },
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

            this.$set(this.own_bets,k,{
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
              stop_bet:res.data[k].stop_bet,
              score:res.data[k].score,
              gain:res.data[k].gain,
              target:res.data[k].target,
            })
          }

          this.ownbets_timer=setInterval(()=>{
              for(let i=0;i<this.own_bets.length;i++){
                if(this.own_bets.last=="正在进行中" || this.own_bets.last=="已结束")
                  continue
                let year=this.own_bets[i].time.split("  ")[0].split("-")[0];
                let month=this.own_bets[i].time.split("  ")[0].split("-")[1];
                let day=this.own_bets[i].time.split("  ")[0].split("-")[2];
                let hour=this.own_bets[i].time.split("  ")[1].split(":")[0];
                let minute=this.own_bets[i].time.split("  ")[1].split(":")[1];
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
                this.$set(this.own_bets[i],"last",last)
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
    ownbet_open(){
      this.ownbet_popup_visible=true;
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
.more-btn{
  cursor: pointer;
  text-align: right;
  width: 100%;
  margin: 0;
}
</style>
