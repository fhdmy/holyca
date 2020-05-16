<template>
  <DxForm :form-data="formData" id="form-wrapper">
    <DxGroupItem :col-count="3" css-class="group-wrapper" :col-count-by-screen="{'lg':3,'md':3,'sm':3,'xs':3}">
      <DxGroupItem>
        <DxSimpleItem data-field="nickname">
          <DxLabel text="昵称"/>
        </DxSimpleItem>
        <DxSimpleItem data-field="input_pwd" :editor-options="pwdOptions">
          <DxLabel text="站内密码"/>
        </DxSimpleItem>
        <DxSimpleItem data-field="input_new_pwd" :editor-options="cfmPwdOptions">
          <DxLabel text="新密码"/>
        </DxSimpleItem>
      </DxGroupItem>
      <DxGroupItem :colCount="1">
        <DxSimpleItem data-field="repstats_acc">
          <DxLabel text="RepStats账号"/>
        </DxSimpleItem>
        <DxSimpleItem data-field="repstats_pwd" :editor-options="pwdOptions">
          <DxLabel text="RepStats密码"/>
        </DxSimpleItem>
        <DxSimpleItem data-field="auth">
          <DxLabel text="Auth Key"/>
        </DxSimpleItem>
      </DxGroupItem>
      <DxGroupItem :colCount="1">
        <DxSimpleItem data-field="score" css-class="score-input">
          <DxLabel text="站内积分"/>
        </DxSimpleItem>
      </DxGroupItem>
    </DxGroupItem>
  </DxForm>
</template>
<script>
import {
  DxForm,
  DxSimpleItem,
  DxGroupItem,
  DxLabel
} from "devextreme-vue/form";

export default {
  components: {
    DxForm,
    DxGroupItem,
    DxSimpleItem,
    DxLabel
  },
  props:{
    formData:{
      type:Object,
      default(){
        return {
          nickname: "",
          input_pwd: "",
          input_new_pwd: "",
          auth:"",
          repstats_acc: "",
          repstats_pwd:"",
          score: 0
        };
      }
    }
  },
  watch: {
    formData:{
      handler: function (newVal) {
        this.$emit('update:formData', newVal);
      },
      deep: true,
    }
  },
  computed: {
    
  },
  data: () => ({
    pwdOptions: {
      mode: "password"
    },
    cfmPwdOptions: {
      mode: "password"
    },
  })
};
</script>
<style>
.group-wrapper {
  padding: 15px 0 0 0;
}
.score-input {
  pointer-events: none;
}
</style>
