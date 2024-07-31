<script setup>
import { ref, onMounted } from 'vue';
import { getPixivDailyRanking } from '../config/pixivService';
import CommonHeader from '../components/CommonHeader.vue';
import CommonAside from '../components/CommonAside.vue';
import CommonFooter from '../components/CommonFooter.vue';
import Live2DModel from '../components/live2d.vue';

const pixivRanking = ref([]);

onMounted(async () => {
  try {
    const response = await getPixivDailyRanking();
    pixivRanking.value = response.data;
    console.log('Pixiv Ranking:', pixivRanking.value);
  } catch (error) {
    console.error('Failed to load Pixiv daily ranking:', error);
  }
});
</script>

<template>
  <div class="common-layout">
    <el-container class="lay-container">
      <el-aside>
        <CommonAside />
      </el-aside>
      <el-container class="r-content">
        <CommonHeader />
        <el-main>
          <h2 class="pixiv-title">Pixiv 每日排行</h2>
          <div v-if="pixivRanking.length">
            <div class="pixiv-gallery">
              <div class="pixiv-item" v-for="item in pixivRanking" :key="item.id">
                <a :href="item.url" target="_blank">
                  <img :src="item.url" :alt="item.title" />
                  <p>{{ item.title }}</p>
                </a>
              </div>
            </div>
          </div>
          <div v-else>
            <p>加载中...</p>
            <pre>{{ pixivRanking }}</pre>
          </div>
        </el-main>
        <Live2DModel />
        <CommonFooter />
      </el-container>
    </el-container>
  </div>
</template>

<style scoped lang="less">
.pixiv-title {
  margin-top: 72px;
  margin-bottom: 72px;
  text-align: center;
  font-size: 34px;
}

.pixiv-gallery {
  display: flex;
  flex-wrap: wrap;
  gap: 40px;
}

.pixiv-item {
  flex: 1 1 calc(33.333% - 40px);
  box-sizing: border-box;
}

.pixiv-item img {
  width: 100%;
  height: auto;
  display: block;
}
</style>


