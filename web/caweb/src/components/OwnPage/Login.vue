<template>
  <DxForm :form-data="formData" id="form-wrapper">
    <DxGroupItem :col-count="3" css-class="group-wrapper">
      <DxGroupItem>
        <DxSimpleItem data-field="nickname" css-class="nickname-item">
          <DxLabel text="昵称"/>
        </DxSimpleItem>
        <DxSimpleItem data-field="input_pwd" :editor-options="pwdOptions">
          <DxLabel text="站内密码"/>
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
    DxLabel,
  },
  computed: {
    
  },
  props:{
    formData:{
      type:Object,
      default(){
        return {
          nickname: "",
          input_pwd: ""
        }
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
  data: () => ({
    pwdOptions: {
      mode: "password"
    },
  })
};
</script>
<style>
.group-wrapper {
  padding: 15px 0 0 0;
}
.nickname-item{
  margin-bottom: 15px;
}
</style>
