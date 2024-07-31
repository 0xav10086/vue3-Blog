<template>
  <div class="common-layout">
    <el-calendar
      ref="calendar"
      class="custom-calendar"
      :model-value="currentDate"
      :range="monthRange"
      @click="handleCalendarClick"
    >
      <template #header>
        <div class="el-calendar__header">
          <div class="el-calendar__title">{{ quarterY }}年{{ quarterM }}月新番表</div>
          <div class="el-calendar__button-group">
            <div class="el-button-group">
              <button @click="prevMonth" aria-disabled="false" type="button" class="el-button el-button--small">
                <span>上个月</span>
              </button>
              <button @click="goToday" aria-disabled="false" type="button" class="el-button el-button--small">
                <span>今天</span>
              </button>
              <button @click="nextMonth" aria-disabled="false" type="button" class="el-button el-button--small">
                <span>下个月</span>
              </button>
            </div>
          </div>
        </div>
      </template>
      <template #dateCell="{ date }">
        <div class="el-calendar-day current" @click="handleDateClick(date)">
          <span>{{ date.getDate() }}</span>
        </div>
      </template>
    </el-calendar>
    <el-container class="lay-container">
      <el-container class="r-content">
        <p class="main-messagebox">
          你好，欢迎来到我的网站<br>
          关于本网站，只是本人的一个vue练手项目，存在诸多bug，大部分只需要F5刷新即可<br>
          关于新番表，只需要点击就可以查看当日有哪些新番，除了查询外暂不支持其他功能<br>
          本项目还在缓慢填坑中，有诸多部件没有完善，本人正在努力掉头发当中<br>
          推荐全屏浏览，你也不想遇到元素位置错误吧<br>
          最后一句话，Ciallo～(∠・ω< )⌒☆
        </p>
        <CommonAside />
        <CommonHeader />
        <CommonFooter />
        <Live2DModel />
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';
import { ElMessageBox, ElLoading } from 'element-plus';
import CommonHeader from '../components/CommonHeader.vue';
import CommonAside from '../components/CommonAside.vue';
import CommonFooter from '../components/CommonFooter.vue';
import Live2DModel from '../components/live2d.vue';

function getMonthRange(date) {
  const startOfMonth = new Date(date.getFullYear(), date.getMonth(), 1);
  const endOfMonth = new Date(date.getFullYear(), date.getMonth() + 1, 0);

  const formatDate = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  return [formatDate(startOfMonth), formatDate(endOfMonth)];
}

function getQuarterYear(date) {
  const year = date.getFullYear();
  return year;
}

function getQuarterMonth(date) {
  const month = date.getMonth() + 1;
  if (month >= 1 && month <= 3) {
    return '1';
  } else if (month >= 4 && month <= 6) {
    return '4';
  } else if (month >= 7 && month <= 9) {
    return '7';
  } else {
    return '10';
  }
}

const currentDate = ref(new Date());
const monthRange = ref(getMonthRange(currentDate.value));

const quarterM = computed(() => {
  return getQuarterMonth(currentDate.value);
});

const quarterY = computed(() => {
  return getQuarterYear(currentDate.value);
});

const prevMonth = () => {
  const date = new Date(currentDate.value);
  date.setMonth(date.getMonth() - 1);
  currentDate.value = date;
  monthRange.value = getMonthRange(date);
};

const nextMonth = () => {
  const date = new Date(currentDate.value);
  date.setMonth(date.getMonth() + 1);
  currentDate.value = date;
  monthRange.value = getMonthRange(date);
};

const goToday = () => {
  const date = new Date();
  currentDate.value = date;
  monthRange.value = getMonthRange(date);
};

const handleCalendarClick = (event) => {
  const target = event.target.closest('.current') || event.target.closest('.next');

  if (target) {
    const day = target.querySelector('span').innerText;
    handleDateClick(day);
  }
};


const calculateMaxWidth = (content) => {
  const lines = content.split('<br>');
  let maxWidth = 0;
  const tempElement = document.createElement('div');
  tempElement.style.position = 'absolute';
  tempElement.style.visibility = 'hidden';
  tempElement.style.whiteSpace = 'nowrap';
  document.body.appendChild(tempElement);

  lines.forEach(line => {
    tempElement.innerHTML = line;
    const width = tempElement.offsetWidth;
    if (width > maxWidth) {
      maxWidth = width;
    }
  });

  document.body.removeChild(tempElement);
  return Math.min(maxWidth, 1200);
};

const applyGlobalStyleWidth = (width) => {
  document.documentElement.style.setProperty('--my-messagebox-width', `${width}px`);
};

const handleDateClick = async (day) => {
  const date = new Date(currentDate.value);
  const formattedDate = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
  const month = String(date.getMonth() + 1).padStart(2, '0');
  let loadingInstance;
  try {
    console.log(`Fetching data for date: ${formattedDate}`);
    loadingInstance = ElLoading.service({
      lock: true,
      text: 'Loading',
      spinner: 'el-icon-loading',
      background: 'rgba(0, 0, 0, 0.7)'
    });
    const response = await axios.get('http://127.0.0.1:5000/api/FanList', {params: {date: formattedDate}});
    let fanLists = response.data;

    console.log(`Received data: ${fanLists}`);
    fanLists = fanLists.replace(/\n/g, '<br>');
    const maxWidth = calculateMaxWidth(fanLists);
    applyGlobalStyleWidth(maxWidth);
    ElMessageBox.alert(fanLists, `${month}月${day}号番剧列表以及播出时间`, {
      confirmButtonText: '我知道啦',
      dangerouslyUseHTMLString: true,
      customClass: 'custom-message-box'
    });
  } catch (error) {
    console.error('Error fetching anime schedule:', error);
  } finally {
    if (loadingInstance) {
      loadingInstance.close();
    }
  }
};
</script>

<style scoped>
.custom-calendar {
  position: absolute;
  left: 160px;
  top: 100px;
  width: 30%;
  background-color: var(--background-color);
  border: 1px solid var(--text-color);
}

.el-calendar__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: none;
}

.el-calendar__title {
  font-size: 32px;
  font-weight: bold;
}

.el-button-group {
  margin-left: auto;
  display: flex;
  gap: 10px;
}

.custom-date-cell span {
  font-size: 14px;
}

::v-deep .custom-date-cell a {
  color: purple;
  cursor: pointer;
  text-decoration: underline;
  margin-top: 5px;
}

.main-messagebox {
  position: absolute;
  width: auto;
  left: 160px;
  top: 800px;
  border: 1px solid var(--text-color);
  padding: 10px;
  text-align: left;
  line-height: 25px;
}
</style>
