<template>
  <el-header class="common-header">
    <div class="header-left">
      <span @click="goHome" :class="{ active: isHome, homeButton: true }">Home</span>
    </div>
    <div class="header-center">
      {{ currentTime }}
    </div>
    <div class="header-right">
      <el-tooltip :content="'搜索'" placement="bottom" :effect="tooltipEffect" popper-class="custom-tooltip">
        <el-button icon="search"></el-button>
      </el-tooltip>
      <el-tooltip :content="'切换模式'" placement="bottom" :effect="tooltipEffect" popper-class="custom-tooltip">
        <el-button icon="open" @click="toggleDarkMode"></el-button>
      </el-tooltip>
      <el-tooltip :content="'个人中心'" placement="bottom" :effect="tooltipEffect" popper-class="custom-tooltip">
        <el-button icon="user" @click="go404"></el-button>
      </el-tooltip>
    </div>
  </el-header>
</template>6

<script>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

export default {
  setup() {
    const currentPageName = ref('主页'); // 默认页面名称，您可以根据路由动态更新
    const currentTime = ref('');
    const route = useRoute();
    const router = useRouter();
    const isHome = ref(route.name === 'Home');
    const isDarkMode = ref(false); // 状态变量控制黑暗模式
    const tooltipEffect = ref('light'); // 状态变量控制tooltip效果

    const updateTime = () => {
      const now = new Date();
      currentTime.value = now.toLocaleTimeString();
    };

    const updatePageName = () => {
      currentPageName.value = route.meta.pageName || '主页';
      isHome.value = route.name === 'Home';
    };

    const goHome = () => {
      router.push({ name: 'Home' });
    };

    const go404 = () => {
      router.push({ name: 'NotFound' });
    }

    const toggleDarkMode = () => {
      isDarkMode.value = !isDarkMode.value;
      document.body.classList.toggle('dark-mode', isDarkMode.value);
      tooltipEffect.value = isDarkMode.value ? 'dark' : 'light'; // 切换tooltip效果
    };

    onMounted(() => {
      updateTime();
      setInterval(updateTime, 1000); // 每秒更新时间
      updatePageName();
    });

    watch(route, () => {
      updatePageName();
    });

    return {
      currentPageName,
      currentTime,
      isHome,
      isDarkMode,
      tooltipEffect,
      goHome,
      go404,
      toggleDarkMode
    };
  }
};
</script>

<style scoped>
.common-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background: var(--background-color);
  color: var(--text-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  box-sizing: border-box;
  z-index: 1000;
}

.header-left {
  flex: 1;
  display: flex;
  align-items: center;
}

.header-center {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.header-right {
  flex: 1;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.header-right .el-button {
  margin-left: 5px;
}

.homeButton {
  font-size: 30px; /* 自定义Home按钮的字体大小 */
  cursor: pointer;
  margin-left: 27px;
}

.homeButton.active {
  color: purple;
}

/* Custom Tooltip Styles */
.custom-tooltip {
  background-color: var(--tooltip-background-color);
  color: var(--tooltip-text-color);
  border: 1px solid var(--tooltip-border-color);
}
</style>
