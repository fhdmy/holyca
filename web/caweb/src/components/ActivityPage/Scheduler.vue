<template>
  <DxScheduler
    :data-source="dataSource"
    :current-date="currentDate"
    :views="views"
    :height="545"
    current-view="week"
    :editing="false"
    :firstDayOfWeek="1"
    :show-all-day-panel="false"
    :shade-until-current-time="true"
    :cellDuration="90"
    id="myscheduler"
  />
</template>
<script>

import DxScheduler from 'devextreme-vue/scheduler';

export default {
  components: {
    DxScheduler
  },
  props:{
    dataSource:{
      type:Array,
      default(){
        return []
      }
    }
  },
  data:()=>({
    views: ['day', 'week','month'],
    currentDate: new Date(),
  })
};
</script>

<style scoped>
#myscheduler>>>.dx-scheduler-appointment-content-date{
  line-height: 20px;
  width: 100%;
  word-wrap: break-word;
  white-space: pre-wrap;
}
</style>

