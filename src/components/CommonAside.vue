<template>
  <div class="accordion-container">
    <el-button class="accordion"
               :class="{ active: panels[0] }"
               @click="togglePanel(0)">
      笔记
    </el-button>
    <div class="panel" :style="{ display: panels[0] ? 'block' : 'none' }">
      <div @click="goNotes()">点击查看笔记</div>
    </div>

    <el-button class="accordion"
               :class="{ active: panels[1] }"
               @click="togglePanel(1)">
      图床
    </el-button>
    <div class="panel" :style="{ display: panels[1] ? 'block' : 'none' }">
      <div @click="goImg">点击查看图床</div>
    </div>

    <el-button class="accordion"
               :class="{ active: panels[2] }"
               @click="togglePanel(2)">
      日志
    </el-button>
    <div class="panel" :style="{ display: panels[2] ? 'block' : 'none' }">
      <div @click="goLogs">点击查看日志</div>
    </div>

    <el-button class="accordion"
               :class="{ active: panels[3] }"
               @click="togglePanel(3)">
      书库
    </el-button>
    <div class="panel" :style="{ display: panels[3] ? 'block' : 'none' }">
      <div @click="goLibrary">点击查看书库</div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    const panels = ref([false, false, false, false]);

    const goNotes = () => {
      router.push('/notes');
    };

    const goImg = () => {
      router.push('/images');
    };

    const goLogs = () => {
      router.push('/logs');
    };

    const goLibrary = () => {
      router.push('/library');
    };

    const togglePanel = (index) => {
      panels.value[index] = !panels.value[index];
    };

    return {
      panels,
      togglePanel,
      goNotes,
      goImg,
      goLogs,
      goLibrary,
    };
  },
};
</script>

<style scoped>
.accordion-container {
  position: fixed;
  top: 60px;
  bottom: 60px;
  left: 0;
  width: 144px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow-y: auto;
}

.accordion {
  background-color: var(--aside-background-color);
  color: var(--aside-text-color);
  cursor: pointer;
  padding: 18px;
  width: 100%;
  text-align: center;
  border: none;
  outline: none;
  transition: 0.4s;
  font-size: 28px;
  margin-bottom: 36px;
}

.active, .accordion:hover {
  background-color: var(--aside-background-color);
}

.panel {
  padding: 0 18px;
  background-color: var(--aside-background-color);
  overflow: hidden;
}

.accordion:after {
  content: '\02795';
  font-size: 12px;
  float: right;
  margin-left: 5px;
}

.active:after {
  content: "\2796";
}
</style>
