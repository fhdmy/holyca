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
                          <template #default></template>
                        </DxItem>
                        <!-- 仪表盘 -->
                        <DxItem :ratio="3">
                          <template #default></template>
                        </DxItem>
                        <!-- 图表 -->
                        <DxItem :ratio="7">
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
                          <template #default></template>
                        </DxItem>
                        <!-- 雷达图 -->
                        <DxItem :ratio="3">
                          <template #default></template>
                        </DxItem>
                        <!-- 图表 -->
                        <DxItem :ratio="7">
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
                    <template #default></template>
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

export default {
  components: {
    DxBox,
    DxItem,
    DxButton,
    ProfileForm,
    Signup,
    Login
  },
  props: {},
  data: () => ({
    token:"",
    has_login:false,
    signup_flag:false,
    // player_info: {
    //   nickname: "Xnick",
    //   input_pwd: "",
    //   input_confirm_pwd: "",
    //   auth:
    //     "ba729318a506a1ec476654053cf7e7483b1056df;eff1d56f879b05be0b8f53cf3aec7d65bffdc2fe;1584699974",
    //   repstats_acc: "holyca@126.com",
    //   repstats_pwd: "HolyHolyCA",
    //   score: 100
    // },
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
    }
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
      const text = "输入项为空!";
      const type = "error";
      notify(text, type, 1500);
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
        console.log(res);
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
          const text = "账号或密码错误!";
          const type = "error";
          notify(text, type, 1500);
        }
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
          console.log(res);
          this.player_info.nickname=res.data.nickname;
          this.player_info.score=res.data.score;
          this.player_info.auth=res.data.auth;
          this.player_info.repstats_acc=res.data.repstats_acc;
          this.player_info.repstats_pwd=res.data.repstats_pwd;
          this.has_login=true;
        })
        .catch(error => {
          console.log(error.response);
          notify("获取信息失败!", "error", 1500);
          this.has_login=false;
        });
    },
    refresh_all(){
      this.reset_player_info();
      this.get_player_info();
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
          console.log(res);
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
          console.log(res)
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
          if(error.response.data=="Username already exisits"){
            notify("用户名已被使用!", "error", 1500);
          }
          if(error.response.data=="RepStats verification is invalid"){
            notify("RepStats核对错误!", "error", 1500);
          }
          if(error.response.data=="Serializer is invalid"){
            notify("修改信息有误!", "error", 1500);
          }
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
  bottom: 45%;
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
</style>
