<template>
  <div class="hello">
    <p>nickname: {{nickname}}</p>
    <p>score: {{score}}</p>
    <p>auth: {{auth}}</p>
    <button @click="login()">登录</button>
    <button @click="sign_up()">注册</button>
   <button @click="change_pwd()">更改密码</button>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data:()=>({
    nickname:"",
    score:"",
    auth:"",
    token:(localStorage.getItem("token")==null)?"":"Token " + localStorage.getItem("token")
  }),
  created() {
    //get all teammates
    this.$http({
        method: "get",
        url: "/api/account/teammates/",
      })
        .then(res => {
          console.log(res);
        })
        .catch(error => {
          console.log(error.response);
        });
  },
  methods: {
    change_pwd(){
      this.$http({
        method: "post",
        url: "/api/account/teammates/change_pwd/",
        data:{
          old_pwd:this.Base64.encode("123456"),
          new_pwd:this.Base64.encode("Jch199669")
        },
        headers: {
          "Authorization": this.token
        },
      })
        .then(res => {
          console.log(res);
        })
        .catch(error => {
          console.log(error.response);
        });
    },
    login(){
      this.$http({
        method: "post",
        url: "/api/account/teammates/login/",
        data:{
          username:"Xnick",
          password:this.Base64.encode("Jch199669"),
        }
      })
        .then(res => {
          console.log(res);
          localStorage.clear();
          localStorage.setItem("token", res.data.token);
          localStorage.setItem("user_id", res.data.profile_url);
          this.token=(localStorage.getItem("token")==null)?"":"Token " + localStorage.getItem("token");
          this.get_home_page();
        })
        .catch(error => {
          console.log(error.response);
        });
    },
    sign_up(){
      this.$http({
        method: "post",
        url: "/api/account/sign_up/",
        data:{
          username:"fungal",
          password:this.Base64.encode("123456"),
        }
      })
        .then(res => {
          console.log(res);
        })
        .catch(error => {
          console.log(error.response);
        });
    },
    get_home_page(){
      this.$http({
        method: "get",
        url: "/api/account/teammates/get_homepage/",
        headers: {
          "Authorization": this.token
        },
      })
        .then(res => {
          console.log(res);
          this.nickname=res.data.nickname;
          this.score=res.data.score;
          this.auth=res.data.auth;
        })
        .catch(error => {
          console.log(error.response);
        });
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
