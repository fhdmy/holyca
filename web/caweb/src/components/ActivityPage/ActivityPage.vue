<template>
  <div>
    <div class="left-icon" @click="switchPage()"><i class="dx-icon-chevronleft icon-left"></i></div>
  </div>
</template>
<script>
export default {
  components: {},
  props: {},
  data: () => ({}),
  methods: {
    switchPage() {
      this.$router.push({
        name: "homepage"
      });
    }
  }
};
</script>
<style scoped>
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
</style>
