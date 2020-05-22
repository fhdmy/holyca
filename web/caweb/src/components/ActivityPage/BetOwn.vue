<template>
  <DxScrollView
    width="100%"
    height="100%"
  >
    <div class="list-container">
      <DxList
        :data-source="dataSource"
        height="100%"
        :focusStateEnabled="false"
        :activeStateEnabled="false"
        :hoverStateEnabled="false"
        class="list"
      >
        <template #item="{ data: item }">
          <div>
            <div style="float:left;width:45%;">
              <p style="margin-bottom:0;"><span class="player">{{item.player_1}}  </span><span style="color:#8e93a7;">vs</span><span class="player">  {{item.player_2}}</span></p>
              <p class="tournament">{{item.tournament}}</p>
            </div>
            <div style="float:left;">
              <p :id="'owntime'+item.id" @mouseenter="toggleDefault(item)"
              @mouseleave="toggleDefault(item)" class="item-time">~{{item.last}}</p>
              <DxTooltip
                :visible.sync="item.time_visible"
                :close-on-outside-click="false"
                :target="'#owntime'+item.id"
                :position="'top'"
              >
              {{item.time}}
              </DxTooltip>
            </div>
            <div style="float:right;" class="right-wrapper">
              <div>
                <span class="odds-title">投注: {{item.score}}</span>
                <span class="odds-title">赚取: {{item.gain}}</span>
                <span class="odds-target">下注对象: {{item.target}}</span>
                <div style="clear:both;"></div>
              </div>
              <div style="margin-top:10px;">
                <DxButton :width="145" :height="30" 
                :text="item.player_1+'   '+item.bet_1" type="success" 
                styling-mode="success" 
                :element-attr="{class:'odds-btn'}"/>
                <DxButton :width="145" :height="30" 
                :text="item.bet_2+'   '+item.player_2" 
                type="danger" styling-mode="danger" 
                :element-attr="{class:'odds-btn'}"/>
              </div>
            </div>
            <div style="clear:both;"></div>
          </div>
        </template>
      </DxList>
    </div>
  </DxScrollView>
</template>
<script>
import DxList from 'devextreme-vue/list';
import { DxButton } from 'devextreme-vue';
import { DxScrollView } from 'devextreme-vue/scroll-view';
import { DxTooltip } from 'devextreme-vue/tooltip';

export default {
  components: {
    DxList,
    DxButton,
    DxScrollView,
    DxTooltip
  },
  props:{
    dataSource:{
      type:Array,
      default(){
        return []
      }
    },
  },
  data:()=> ({

  }),
  methods: {
     toggleDefault(e) {
      e.time_visible=!e.time_visible;
    },
  },
};
</script>
<style scoped>
.list-container{
  position: relative;
}
.list-container>>>.dx-list-item{
  cursor:default!important;
}
.player{
  font-weight: 500;
  font-size: 16px;
}
.tournament{
  margin-top: 5px;
  color:#8e93a7;
}
.item-time{
  color:#8e93a7;
  font-size: 14px;
  margin-top: 30px;
  margin-left: 40px;
}
.input-odds{
  float: left;
}
.odds-title{
  float: left;
  font-size: 14px;
  margin-top: 5px;
  width: 80px;
}
.odds-target{
  float: left;
  font-size: 14px;
  margin-top: 5px;
  width: 130px;
}
.right-wrapper{
  margin-left: 30px;
}
.odds-btn{
  /* margin-right: 30px; */
  color: white;
}
</style>
