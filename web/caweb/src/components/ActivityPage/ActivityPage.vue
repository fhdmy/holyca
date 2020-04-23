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
                      <DxBox :height="175" direction="row" width="100%">
                        <!-- 说明部分 -->
                        <DxItem :ratio="3">
                          <template #default>
                            <div>
                              
                            </div>
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
                      <DxBox :height="175" direction="row" width="100%">
                        <!-- 说明部分 -->
                        <DxItem :ratio="3">
                          <template #default>
                            <div>
                              
                            </div>
                          </template>
                        </DxItem>
                        <!-- 雷达图 -->
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
                      <!-- <dataGrid :dataSource="reps"></dataGrid> -->
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
// import notify from 'devextreme/ui/notify';

export default {
  components: {
    DxBox,
    DxItem,
  },
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
  bottom: 65%;
}
</style>
