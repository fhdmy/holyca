<template>
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
          <div style="float:left;width:30%;">
            <p style="margin-bottom:0;"><span class="player">{{item.player_1}}  </span><span style="color:#8e93a7;">vs</span><span class="player">  {{item.player_2}}</span></p>
            <p class="tournament">{{item.tournament}}</p>
          </div>
          <div style="float:left;">
            <p :id="'time'+item.id" @mouseenter="toggleDefault(item)"
            @mouseleave="toggleDefault(item)" class="item-time">~{{item.last}}</p>
            <DxTooltip
              :visible.sync="item.time_visible"
              :close-on-outside-click="false"
              :target="'#time'+item.id"
              :position="'top'"
            >
              {{item.time}}
            </DxTooltip>
          </div>
          <div style="float:right;" class="right-wrapper">
            <div>
              <span class="odds-title">输入积分:</span>
              <DxNumberBox class="input-odds" :width="100" :height="30"
                :value.sync="item.input_bet" @keyDown="keyDown($event)"
                :max="score" :min="0"
              />
              <span class="odds-opt" @click="input_bet(item,'1/4')">1/4</span>
              <span class="odds-opt" @click="input_bet(item,'1/2')">1/2</span>
              <span class="odds-opt" @click="input_bet(item,'全部')">全部</span>
              <div style="clear:both;"></div>
            </div>
            <div style="margin-top:10px;">
              <DxButton :width="145" :height="30" 
              :text="item.player_1+'   '+item.bet_1" type="success" 
              styling-mode="success" 
              :element-attr="{class:'odds-btn'}" @click="clickto_submit_bet(item,item.player_1)"/>
              <DxButton :width="145" :height="30" 
              :text="item.bet_2+'   '+item.player_2" 
              type="danger" styling-mode="danger" 
              :element-attr="{class:'odds-btn'}" @click="clickto_submit_bet(item,item.player_2)"/>
            </div>
          </div>
          <div style="clear:both;"></div>
        </div>
      </template>
    </DxList>
  </div>
</template>
<script>
import DxList from 'devextreme-vue/list';
import { DxNumberBox } from 'devextreme-vue';
import { DxButton } from 'devextreme-vue';
import { DxTooltip } from 'devextreme-vue/tooltip';
import notify from 'devextreme/ui/notify';

export default {
  components: {
    DxList,
    DxNumberBox,
    DxButton,
    DxTooltip
  },
  props:{
    dataSource:{
      type:Array,
      default(){
        return []
      }
    },
    score:{
      type:Number,
      default:0
    },
    token:{
      type:String,
      default:""
    }
  },
  data:()=> ({

  }),
  methods: {
    toggleDefault(e) {
      e.time_visible=!e.time_visible;
    },
    keyDown(e) {
      const event = e.event;
      const str = event.key || String.fromCharCode(event.which);
      if(/^[.,e]$/.test(str)) {
        event.preventDefault();
      }
    },
    input_bet(item,opt){
      switch(opt){
        case '1/2':
          item.input_bet=parseInt(this.score/2);
          break;
        case '1/4':
          item.input_bet=parseInt(this.score/4);
          break;
        case '全部':
          item.input_bet=this.score;
          break;
      }
    },
    clickto_submit_bet(item,choice){
      if(this.token==""){
        notify("账号未登录!", "error", 1500);
        return;
      }
      if(item.stop_bet || item.finished){
        notify("已停止投注!", "error", 1500);
        return;
      }
      if(item.input_bet==null || item.input_bet==0){
        notify("输入不能为空!", "error", 1500);
        return;
      }
      if(confirm("确定要投注？")){
        this.submit_bet(item,choice);
      }
    },
    submit_bet(item,choice){
      this.$http({
        method: "post",
        url: "/api/activity/bet/post_bet/",
        headers: {
          "Authorization": this.token
        },
        data:{
          score:item.input_bet,
          target:choice,
          bet_id:item.id
        }
      })
        .then(res => {
          console.log(res);
          this.$emit('update:score',parseInt(this.score)-parseInt(item.input_bet));
          item.input_bet=0;
          notify("投注成功!", "success", 1500);
        })
        .catch(error => {
          console.log(error.response);
          if(error.response.statusText=="Unauthorized"){
            notify("账户未登录或登录状态错误!", "error", 1500);
          }
          else if(error.response.data=="Serializer is invalid"){
            notify("提交信息不全!", "error", 1500);
          }
          else if(error.response.data=="Score format has error"){
            notify("已停止投注!", "error", 1500);
          }
          else if(error.response.data=="Bet shut down"){
            notify("积分确认错误!", "error", 1500);
          }
          else
            notify("请检查你的网络!", "error", 1500);
        });
    }
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
  margin-left: 150px;
}
.input-odds{
  float: left;
}
.odds-title{
  float: left;
  font-size: 14px;
  margin-top: 5px;
  margin-right: 4px;
}
.odds-opt{
  float: left;
  cursor: pointer;
  margin-left: 20px;
  font-size: 14px;
  margin-top: 5px;
}
.right-wrapper{
  margin-left: 150px;
}
.odds-btn{
  /* margin-right: 30px; */
  color: white;
}
</style>
