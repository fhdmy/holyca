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
                <div class="main-title">{{player_info.nickname}}</div>
              </template>
            </DxItem>

            <!-- ######## -->
            <!-- ######## -->
            <!-- 个人信息框架 -->
            <DxItem :ratio="4">
              <template #default>
                <DxBox :height="200" direction="col" width="100%">
                  <!-- sub-title -->
                  <DxItem :ratio="1">
                    <template #default>
                      <DxBox :height="25" direction="row" width="100%">
                        <DxItem :ratio="1">
                          <template #default>
                            <div class="sub-title">账号</div>
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
                      <DxBox :height="220" direction="row" width="100%">
                        <DxItem :ratio="1">
                          <template #default></template>
                        </DxItem>
                        <DxItem :ratio="14">
                          <template #default>
                            <DxBox :height="220" direction="col" width="100%">
                              <DxItem :ratio="12">
                                <template #default>
                                  <div>
                                    <!-- 注册 -->
                                    <signup v-show="!has_login && signup_flag" :formData.sync="signup_info"></signup>
                                    <!-- 登录 -->
                                    <div v-show="!has_login && !signup_flag">
                                      <login :formData.sync="login_info"></login>
                                      <span class="click-to-signup" @click="click_to_signup">点击注册</span>
                                    </div>
                                    <!-- 个人中心 -->
                                    <profileForm :formData.sync="player_info" v-show="has_login"></profileForm>
                                  </div>
                                </template>
                              </DxItem>
                              <DxItem :ratio="3">
                                <template #default>
                                  <DxBox :height="50" direction="row" width="100%">
                                    <DxItem :ratio="7">
                                      <template #default>
                                        <div>
                                          <!-- 用户主页 -->
                                          <DxButton
                                            text="修改"
                                            styling-mode="contained"
                                            :element-attr="change_btn_attrs"
                                            v-show="has_login"
                                            @click="alter_info()"
                                          />
                                          <!-- 登录 -->
                                          <DxButton
                                            text="登录"
                                            styling-mode="contained"
                                            :element-attr="change_btn_attrs"
                                            @click="login()"
                                            v-show="!has_login && !signup_flag"
                                          />
                                          <!-- 注册 -->
                                          <DxButton
                                            text="注册"
                                            styling-mode="contained"
                                            :element-attr="change_btn_attrs"
                                            v-show="!has_login && signup_flag"
                                            @click="signup()"
                                          />
                                        </div>
                                      </template>
                                    </DxItem>
                                    <DxItem :ratio="1">
                                      <template #default>
                                        <div>
                                          <span class="logout-login" 
                                          @click="click_to_login_view()"
                                          v-show="!has_login && signup_flag">登录</span>
                                          <span class="logout-login" 
                                          @click="click_to_logout()"
                                          v-show="has_login"
                                          >注销</span>
                                        </div>
                                      </template>
                                    </DxItem>
                                    <DxItem :ratio="14">
                                      <template #default></template>
                                    </DxItem>
                                  </DxBox>
                                </template>
                              </DxItem>
                              <DxItem :ratio="1">
                                <template #default></template>
                              </DxItem>
                            </DxBox>
                          </template>
                        </DxItem>
                        <DxItem :ratio="1">
                          <template #default></template>
                        </DxItem>
                      </DxBox>
                    </template>
                  </DxItem>
                </DxBox>
              </template>
            </DxItem>

            <!-- ######## -->
            <!-- ######## -->
            <!-- 基础统计框架 -->
            <DxItem :ratio="4">
              <template #default>
                <DxBox :height="266" direction="col" width="100%">
                  <!-- sub-title -->
                  <DxItem :ratio="1">
                    <template #default>
                      <DxBox :height="25" direction="row" width="100%">
                        <DxItem :ratio="1">
                          <template #default>
                            <div class="sub-title">统计</div>
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
                            <div v-if="has_login">
                              <gauge :score="active_score" 
                              :max_value="active_max_value"
                              :palette="active_palette" style="margin:0 auto"></gauge>
                              <span style="margin:10px auto 0" class="sub-title">活跃度: {{active_score_show}}</span>
                            </div>
                          </template>
                        </DxItem>
                        <!-- 仪表盘 -->
                        <DxItem :ratio="3">
                          <template #default>
                            <div v-if="has_login">
                              <polarChart style="margin:0 auto" :palette="basic_palette" :items="basic_items"
                              :DataSource="basic_datas"></polarChart>
                            </div>
                          </template>
                        </DxItem>
                        <!-- 图表 -->
                        <DxItem :ratio="3">
                          <template #default>
                            <div v-if="has_login">
                              <polarChart style="margin:0 auto" :palette="map_palette" :items="map_items"
                              :DataSource="map_datas"></polarChart>
                            </div>
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
                            <div v-if="has_login">
                              <div class="explain-content">查看对应的各战网账号平均MMR值，右图所示为各账号的MMR变化趋势。</div>
                              <label class="mmr-score">{{mmr_score_show}}</label>
                            </div>
                          </template>
                        </DxItem>
                        <!-- 仪表盘 -->
                        <DxItem :ratio="3">
                          <template #default>
                            <gauge :score="mmr_score" 
                            :max_value="mmr_max_value"
                            :palette="mmr_palette" v-if="has_login"></gauge>
                          </template>
                        </DxItem>
                        <!-- 图表 -->
                        <DxItem :ratio="7">
                          <template #default>
                            <lineChart :players="mmr_players" 
                            :dataSource="mmr_players_mmr"
                            :palette="mmr_palette"
                            v-if="has_login"></lineChart>
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
                            <div v-if="has_login">
                              <div class="explain-content">本月最IMBA的种族是？右图展示了录像中对手是各种族的盘数，以及三族对抗胜率变化趋势。</div>
                              <label class="imba-score">{{imba_most}}</label>
                            </div>
                          </template>
                        </DxItem>
                        <!-- 雷达图 -->
                        <DxItem :ratio="3">
                          <template #default>
                            <pieChart :dataSource="imba_sums" :palette="imba_palette" v-if="has_login"></pieChart>
                          </template>
                        </DxItem>
                        <!-- 图表 -->
                        <DxItem :ratio="7">
                          <template #default>
                            <lineChart :players="imba_vs" 
                            :dataSource="imba_rate"
                            :palette="imba_palette"
                            v-if="has_login"></lineChart>
                          </template>
                        </DxItem>
                      </DxBox>
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
    <div class="right-icon" @click="switchPage()">
      <i class="dx-icon-chevronright icon-right"></i>
    </div>
  </div>
</template>
<script>
import { DxBox, DxItem } from "devextreme-vue/box";
import { DxButton } from "devextreme-vue";
import ProfileForm from "./ProfileForm.vue";
import Signup from "./Signup.vue";
import Login from "./Login.vue";
import notify from "devextreme/ui/notify";
import Gauge from "../Home/Gauge.vue";
import LineChart from "../Home/LineChart.vue";
import PieChart from "../Home/PieChart.vue";
import PolarChart from "./PolarChart.vue";

export default {
  components: {
    DxBox,
    DxItem,
    DxButton,
    ProfileForm,
    Signup,
    Login,
    Gauge,
    LineChart,
    PieChart,
    PolarChart
  },
  props: {},
  data: () => ({
    token:"",
    has_login:false,
    signup_flag:false,
    player_info: {
      nickname: "",
      input_pwd: "",
      input_new_pwd: "",
      auth:"",
      repstats_acc: "",
      repstats_pwd: "",
      score: 0
    },
    change_btn_attrs: {
      class: "change_btn"
    },
    login_info: {
      nickname: "",
      input_pwd: ""
    },
    signup_info:{
      nickname: "",
      input_pwd: "",
      input_confirm_pwd: "",
      auth:"",
      repstats_acc: "",
      repstats_pwd:"",
      score: 0
    },
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
    active_score_show:0,
    active_score:0,
    active_max_value:200,
    active_palette:"Pastel",
    map_palette:"Soft Blue",
    map_items:[],
    map_datas:[],
    basic_palette:"Violet",
    basic_items:[
      { value: "Xnick", name: "Xnick" },
      { value: "星之所在", name: "星之所在" }
    ],
    basic_datas:[
      {
        arg: "全面",
        Xnick: 4.21,
        星之所在: 6.22
      },
      {
        arg: "进攻",
        Xnick: 4.21,
        星之所在: 6.22
      },
      {
        arg: "后期",
        Xnick: 4.21,
        星之所在: 6.22
      },
      {
        arg: "运营",
        Xnick: 4.21,
        星之所在: 6.22
      },
      {
        arg: "骚扰",
        Xnick: 4.21,
        星之所在: 6.22
      },
    ],
  }),
  created() {
    this.token=localStorage.getItem("token") == null
        ? ""
        : "Token " + localStorage.getItem("token");
    if(this.token!=""){
      this.refresh_all();
    }
  },
  watch: {
    new_battlenet(val) {
      if (val != "") {
        this.get_new_battlenet(val);
      }
    }
  },
  methods: {
    switchPage() {
      this.$router.push({
        name: "homepage"
      });
    },
    empty_input() {
      notify("输入项为空!", "error", 1500);
    },
    login() {
      if (this.login_info.nickname == "" || this.login_info.input_pwd == "") {
        this.empty_input();
        return;
      }
      this.$http({
        method: "post",
        url: "/api/account/teammates/login/",
        data: {
          username: this.login_info.nickname,
          password: this.Base64.encode(this.login_info.input_pwd)
        }
      })
      .then(res => {
        // console.log(res);
        localStorage.clear();
        localStorage.setItem("token", res.data.token);
        localStorage.setItem("user_id", res.data.user_id);
        localStorage.setItem("profile_id", res.data.profile_id);
        this.token =
          localStorage.getItem("token") == null
            ? ""
            : "Token " + localStorage.getItem("token");
        this.has_login=true;
        notify("登录成功！", "success", 1500);
        this.refresh_all();
      })
      .catch(error => {
        console.log(error.response);
        if (error.response.data == "Serializer is invalid") {
          notify("账号或密码错误", "error", 1500);
        }
        else
          notify("请检查你的网络!", "error", 1500);
      });
    },
    get_player_info(){
      this.$http({
        method: "get",
        url: "/api/account/teammates/get_homepage/",
        headers: {
          "Authorization": this.token
        },
      })
        .then(res => {
          // console.log(res);
          this.player_info.nickname=res.data.nickname;
          this.player_info.score=res.data.score;
          this.player_info.auth=res.data.repstats.auth;
          this.player_info.repstats_acc=res.data.repstats.repstats_acc;
          this.player_info.repstats_pwd=res.data.repstats.repstats_pwd;
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
    refresh_all(){
      this.reset_player_info();
      this.get_player_info();
      this.racesum_statistics();
      this.raceimba_statistics();
      this.mmr_statistics();
      this.active_statistics();
      this.map_statistics();
      this.basic_statistics();
    },
    click_to_signup(){
      this.reset_signup_info();
      this.signup_flag=true;
    },
    click_to_login_view(){
      this.reset_login_info();
      this.signup_flag=false;
    },
    click_to_logout(){
      if(confirm("确定要注销？")){
        localStorage.clear();
        this.has_login=false;
        this.signup_flag=false;
        this.token="";
        this.reset_all();
      }
    },
    reset_all(){
      this.reset_player_info();
      this.reset_login_info();
      this.reset_signup_info();
    },
    reset_login_info(){
      this.login_info.nickname="";
      this.login_info.input_pwd="";
    },
    reset_signup_info(){
      this.signup_info.nickname="";
      this.signup_info.input_pwd= "";
      this.signup_info.input_confirm_pwd= "";
      this.signup_info.auth="";
      this.signup_info.repstats_acc= "";
      this.signup_info.repstats_pwd="";
      this.signup_info.score=0;
    },
    reset_player_info(){
      this.player_info.nickname= "";
      this.player_info.input_pwd= "";
      this.player_info.input_new_pwd="";
      this.player_info.auth="";
      this.player_info.repstats_acc= "";
      this.player_info.repstats_pwd= "";
      this.player_info.score=0;
    },
    signup(){
      if(this.signup_info.nickname=="" || 
      this.signup_info.input_pwd=="" || 
      this.signup_info.input_confirm_pwd==""){
        notify("昵称或密码为空!", "error", 1500);
        return;
      }
      if(this.signup_info.input_pwd!=this.signup_info.input_confirm_pwd){
        notify("密码不符!", "error", 1500);
        return;
      }
      if(this.signup_info.input_pwd.lenth<6 || this.signup_info.input_pwd.lenth>20){
        notify("密码长度不符合要求!", "error", 1500);
        return;
      }
      if((this.signup_info.repstats_acc=="" ||
      this.signup_info.repstats_pwd=="" ||
      this.signup_info.auth=="") && 
      !(this.signup_info.repstats_acc=="" && 
      this.signup_info.repstats_pwd=="" &&
      this.signup_info.auth=="")){
        notify("RepStats信息不全!", "error", 1500);
        return;
      }

      this.$http({
        method: "post",
        url: "/api/account/sign_up/",
        data:{
          nickname:this.signup_info.nickname,
          password:this.Base64.encode(this.signup_info.input_pwd),
          auth:this.signup_info.auth,
          repstats_acc:this.signup_info.repstats_acc,
          repstats_pwd:this.Base64.encode(this.signup_info.repstats_pwd)
        }
      })
        .then(res => {
          // console.log(res);
          localStorage.clear();
          localStorage.setItem("token", res.data.token);
          localStorage.setItem("user_id", res.data.user_id);
          localStorage.setItem("profile_id", res.data.profile_id);
          this.token =
            localStorage.getItem("token") == null
              ? ""
              : "Token " + localStorage.getItem("token");
          this.has_login=true;
          notify("注册成功！", "success", 1500);
          this.refresh_all();
        })
        .catch(error => {
          console.log(error.response);
          if(error.response.data == "RepStats verification is invalid"){
            notify("RepStats核对错误!", "error", 1500);
          }
          else if(error.response.data == "Username already exisits"){
            notify("用户名已被使用!", "error", 1500);
          }
          else if(error.response.data == "Serializer is invalid"){
            notify("注册信息有误!", "error", 1500);
          }
          else if(error.response.data == "RepStats already used"){
            notify("RepStats账号已被使用!", "error", 1500);
          }
          else
            notify("请检查你的网络!", "error", 1500);
        });
    },
    alter_info(){
      if(this.player_info.nickname==""){
        notify("昵称为空!", "error", 1500);
        return;
      }
      if(this.player_info.input_pwd.length<6 || this.player_info.input_pwd.length>20){
        notify("原密码为空或不符合要求!", "error", 1500);
        return;
      }
      if(this.player_info.input_new_pwd!="" && (this.player_info.input_new_pwd.length<6 || this.player_info.input_new_pwd.length>20))
      {
        notify("新密码长度不符合要求!", "error", 1500);
        return;
      }
      if((this.player_info.repstats_acc=="" ||
      this.player_info.repstats_pwd=="" ||
      this.player_info.auth=="") && 
      !(this.player_info.repstats_acc=="" && 
      this.player_info.repstats_pwd=="" &&
      this.player_info.auth=="")){
        notify("RepStats信息不全!", "error", 1500);
        return;
      }

      this.$http({
        method: "post",
        url: "/api/account/teammates/alert_info/",
        data:{
          nickname: this.player_info.nickname,
          password: this.Base64.encode(this.player_info.input_pwd),
          new_password: this.Base64.encode(this.player_info.input_new_pwd),
          auth:this.player_info.auth,
          repstats_acc: this.player_info.repstats_acc,
          repstats_pwd: this.Base64.encode(this.player_info.repstats_pwd),
        },
        headers: {
          "Authorization": this.token
        },
      })
        .then(res => {
          // console.log(res)
          if(res.data=="Alter Info OK"){
            notify("修改成功!", "success", 1500);
          }
          this.refresh_all();
        })
        .catch(error => {
          console.log(error.response);
          if(error.response.data=="Password does not match"){
            notify("原密码错误!", "error", 1500);
          }
          else if(error.response.data=="Username already exisits"){
            notify("用户名已被使用!", "error", 1500);
          }
          else if(error.response.data=="RepStats verification is invalid"){
            notify("RepStats核对错误!", "error", 1500);
          }
          else if(error.response.data=="Serializer is invalid"){
            notify("修改信息有误!", "error", 1500);
          }
          else if(error.response.data == "RepStats already used"){
            notify("RepStats账号已被使用!", "error", 1500);
          }
          else
            notify("请检查你的网络!", "error", 1500);
        });
    },
    racesum_statistics(){
      this.$http({
        method: "get",
        url: "/api/account/teammates/racesum_statistics/",
        headers: {
          "Authorization": this.token
        },
      })
        .then(res => {
          // console.log(res);
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
          if(error.response.statusText=="Unauthorized"){
            notify("账户未登录或登录状态错误!", "error", 1500);
          }
          else
            notify("请检查你的网络!", "error", 1500);
        });
    },
    raceimba_statistics(){
      this.$http({
        method: "get",
        url: "/api/account/teammates/racewinrate_statistics/",
        headers: {
          "Authorization": this.token
        },
      })
        .then(res => {
          // console.log(res);
          for(let k=0;k<res.data.length;k++){
            this.$set(this.imba_rate,k,{
              holyca_date:res.data[k].date,
              TVP:res.data[k].TVP,
              PVZ:res.data[k].PVZ,
              ZVT:res.data[k].ZVT,
              holyca_index:k+1
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
          if(error.response.statusText=="Unauthorized"){
            notify("账户未登录或登录状态错误!", "error", 1500);
          }
          else
            notify("请检查你的网络!", "error", 1500);
        });
    },
    mmr_statistics(){
      this.$http({
        method: "get",
        url: "/api/account/teammates/mmr_statistics/",
        headers: {
          "Authorization": this.token
        },
      })
        .then(res => {
          // console.log(res);
          for(let m=0;m<res.data[0].length;m++){
            this.$set(this.mmr_players,m,res.data[0][m].name);
          }
          for(let m=0;m<res.data.length;m++){
            this.$set(this.mmr_players_mmr,m,{});
            for(let n=0;n<res.data[m].length;n++){
              this.$set(this.mmr_players_mmr[m],res.data[m][n].name,res.data[m][n].mmr);
            }
            this.$set(this.mmr_players_mmr[m],"holyca_index",m+1);
            this.$set(this.mmr_players_mmr[m],"holyca_date",res.data[m][0].date);
          }
          let mmr_sum=0;
          let mmr_num=0;
          for(let k=0;k<res.data[11].length;k++){
            if(res.data[11][k].mmr!=0){
              mmr_sum+=res.data[11][k].mmr;
              mmr_num+=1;
            }
          }
          let avg_mmr=parseInt(mmr_sum/mmr_num);
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
          if(error.response.statusText=="Unauthorized"){
            notify("账户未登录或登录状态错误!", "error", 1500);
          }
          else
            notify("请检查你的网络!", "error", 1500);
        });
    },
    active_statistics(){
      this.$http({
        method: "get",
        url: "/api/account/teammates/active_statistics/",
        headers: {
          "Authorization": this.token
        },
      })
        .then(res => {
          // console.log(res);
          let sum=res.data;
          // 取盘数非0的账号
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
          this.active_max_value=300;
        })
        .catch(error => {
          console.log(error.response);
          if(error.response.statusText=="Unauthorized"){
            notify("账户未登录或登录状态错误!", "error", 1500);
          }
          else
            notify("请检查你的网络!", "error", 1500);
        });
    },
    map_statistics(){
      this.$http({
        method: "get",
        url: "/api/account/teammates/get_map_winrate/",
        headers: {
          "Authorization": this.token
        },
      })
        .then(res => {
          // console.log(res);
          for(let k=0;k<res.data.length;k++){
            this.$set(this.map_items,k,{
              value: res.data[k].account, 
              name: res.data[k].account
            })
            // 设置地图
            for(let j=0;j<res.data[k].winrate.length;j++){
              let map_name=res.data[k].winrate[j].g_map.split("-天梯版")[0];
              let indata=false;
              for(let i=0;i<this.map_datas.length;i++){
                if(this.map_datas[i].arg==map_name){
                  indata=true;
                  break;
                }
              }
              if(!indata){
                this.$set(this.map_datas,this.map_datas.length,{
                  'arg':map_name
                })
              }
            }
          }
          for(let k=0;k<res.data.length;k++){
            // 设置胜率值
            for(let j=0;j<res.data[k].winrate.length;j++){
              let map_name=res.data[k].winrate[j].g_map.split("-天梯版")[0];
              for(let i=0;i<this.map_datas.length;i++){
                if(this.map_datas[i].arg==map_name){
                  this.$set(this.map_datas[i],res.data[k].account,res.data[k].winrate[j].winrate);
                  break;
                }
              }
            }
          }
        })
        .catch(error => {
          console.log(error.response);
          if(error.response.statusText=="Unauthorized"){
            notify("账户未登录或登录状态错误!", "error", 1500);
          }
          else
            notify("请检查你的网络!", "error", 1500);
        });
    },
    basic_statistics(){
      this.$http({
        method: "get",
        url: "/api/account/teammates/get_basic_statistics/",
        headers: {
          "Authorization": this.token
        },
      })
        .then(res => {
          // console.log(res);
          for(let k=0;k<res.data.length;k++){
            this.$set(this.basic_items,k,{
              value: res.data[k].account, 
              name: res.data[k].account
            })
          }
          this.$set(this.basic_datas,0,{
            'arg':'进攻'
          });
          this.$set(this.basic_datas,1,{
            'arg':'运营'
          });
          this.$set(this.basic_datas,2,{
            'arg':'后期'
          });
          this.$set(this.basic_datas,3,{
            'arg':'全面'
          });
          this.$set(this.basic_datas,4,{
            'arg':'骚扰'
          });
          for(let k=0;k<res.data.length;k++){
            this.$set(this.basic_datas[0],res.data[k].account,res.data[k].basic.attack);
            this.$set(this.basic_datas[1],res.data[k].account,res.data[k].basic.operation);
            this.$set(this.basic_datas[2],res.data[k].account,res.data[k].basic.game_length);
            this.$set(this.basic_datas[3],res.data[k].account,res.data[k].basic.variance);
            this.$set(this.basic_datas[4],res.data[k].account,res.data[k].basic.kill);
          }
        })
        .catch(error => {
          console.log(error.response);
          if(error.response.statusText=="Unauthorized"){
            notify("账户未登录或登录状态错误!", "error", 1500);
          }
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
  font-family: "Segoe UI Light", "Helvetica Neue Light", "Segoe UI",
    "Helvetica Neue", Helvetica, "Trebuchet MS", "Droid Sans", Tahoma, Geneva,
    sans-serif;
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
  font-family: "Segoe UI Light", "Helvetica Neue Light", "Segoe UI",
    "Helvetica Neue", Helvetica, "Trebuchet MS", "Droid Sans", Tahoma, Geneva,
    sans-serif;
}
.hr {
  width: 100%;
  height: 10px;
  border-bottom: 1px solid #6b7289;
  position: relative;
  bottom: 55%;
}
.right-icon {
  background: white;
  border-radius: 60px 0 0 60px;
  width: 30px;
  height: 60px;
  position: absolute;
  top: 400px;
  right: -4px;
  cursor: pointer;
}
.icon-right {
  font-size: 22px;
  color: #1c1f2b;
  position: relative;
  top: 18px;
  left: 4px;
}
.battlenet_btn {
}
.change_btn {
  background: #3debd3;
}
.click-to-signup {
  font-size: 14px;
  color: white;
  cursor: pointer;
  position: relative;
  top: 25px;
}
.logout-login{
  font-size: 14px;
  color: white;
  cursor: pointer;
  position: relative;
  top: 10px;
  left: 30px;
}
.imba-score{
  color: #75c0e0;
  font-size: 60px;
  font-weight: 600;
}
.mmr-score{
  color: #D0B2DA;
  font-size: 60px;
  font-weight: 600;
}
.explain-content{
  padding-top: 10px;
  font-size: 11px;
  color: #8e93a7;
}
</style>
