<template>
  <div ref="live2dContainer" class="live2d-container"></div>
</template>

<script setup>
import { onMounted, ref, onBeforeUnmount, watch } from 'vue';
import { loadOml2d } from 'oh-my-live2d';
import { useRoute } from 'vue-router';

const live2dContainer = ref(null);

const windowWidth = ref(window.innerWidth);
const windowHeight = ref(window.innerHeight);

const defaultModelWidth = 10; // 默认值
const defaultModelHeight = 25; // 默认值
const defaultModelLeft = 0; // 默认值
const defaultModelBottom = 0; // 默认值
const defaultModelScale = 0.05; // 默认值
const defaultXPosition = -10; // 默认值
const defaultYPosition = 80; // 默认值
const defaultDockedPosition = 'left'; // 默认值

const modelWidth = ref(defaultModelWidth);
const modelHeight = ref(defaultModelHeight);
const modelLeft = ref(defaultModelLeft);
const modelBottom = ref(defaultModelBottom);
const modelScale = ref(defaultModelScale);
const xPosition = ref(defaultXPosition);
const yPosition = ref(defaultYPosition);
const dockedPosition = ref(defaultDockedPosition);

const updateWindowSize = () => {
  windowWidth.value = window.innerWidth;
  windowHeight.value = window.innerHeight;
  if (route.path === '/') {
    modelWidth.value = ((windowWidth.value - 160 - (0.3 * windowWidth.value)) / windowWidth.value) * 100;
    modelHeight.value = ((windowHeight.value - 120) / windowHeight.value) * 100;
    modelLeft.value = ((160 + 0.3 * windowWidth.value) / windowWidth.value) * 100;
    modelBottom.value = (60 / windowHeight.value) * 100;
    modelScale.value = (windowWidth.value + windowHeight.value) / 20000;
    xPosition.value = modelWidth.value * 3;
    yPosition.value = windowHeight.value * -0.01;
    dockedPosition.value = 'right';
  } else {
    modelWidth.value = 144 / windowWidth.value * 100;
    modelHeight.value = modelWidth.value * 4;
    modelLeft.value = 0;
    modelBottom.value = 0;
    modelScale.value = 0.05;
    xPosition.value = -82;
    yPosition.value = 0;
    dockedPosition.value = 'left';
  }
};

const route = useRoute();

const loadModel = () => {
  const oml2d = loadOml2d({
    el: live2dContainer.value,
    models: [{
      path: '../Resources/Mao/Mao.model3.json',
      dockedPosition: dockedPosition.value,
      scale: modelScale.value,
      position: [xPosition.value, yPosition.value],
      stageStyle: {
        width: `${modelWidth.value}%`,
        height: `${modelHeight.value}%`,
        left: `${modelLeft.value}%`,
        bottom: `${modelBottom.value}%`,
      },
    }],
    tips: {
      idleTips: {
        wordTheDay(wordTheDayData) {
          return `${wordTheDayData.hitokoto}    by.${wordTheDayData.from}`;
        },
      },
    }
  });

  oml2d.onLoad((status) => {
    switch (status) {
      case 'success':
        console.log('加载成功');
        return;
      case 'fail':
        console.log('加载失败');
        return;
      case 'loading':
        console.log('正在加载中');
        return;
    }
  });

  return oml2d;
};

const oml2dInstance = ref(null);

const setModelState = (state) => {
  if (oml2dInstance.value) {
    const restButton = document.querySelector('#oml2d-menus #Rest');
    if (restButton) {
      restButton.click();
      console.log(`模型状态已设置为：${state}`);
    }
  }
};

onMounted(() => {
  window.addEventListener('resize', updateWindowSize);

  updateWindowSize();
  oml2dInstance.value = loadModel();

  if (route.path === '/') {
    setModelState('awake');
  } else {
    setModelState('rest');
  }
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateWindowSize);
});

watch(route, (newRoute) => {
  updateWindowSize();
  window.location.reload();
});
</script>

<style scoped>
</style>
