<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import CommonAside from "../components/CommonAside.vue";
import CommonHeader from "../components/CommonHeader.vue";
import CommonFooter from "../components/CommonFooter.vue";
import Live2DModel from "../components/live2d.vue";

const folders = ref([]);

const fetchFiles = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/NotesFiles');
    console.log('Fetched files:', response.data); // 添加日志输出以确认数据加载
    folders.value = response.data;
  } catch (error) {
    console.error('Failed to fetch files:', error);
  }
};

const router = useRouter();

const getBoxWidth = (folder) => {
  let maxLength = folder.name.length;
  folder.files.forEach(file => {
    maxLength = Math.max(maxLength, file.length);
  });
  return maxLength * 20 * 1.2 + 'px';
};


const openFile = (folderName, fileName) => {
  const filePath = `${folderName}/${fileName}`;
  console.log('File path:', filePath); // 添加日志输出以确认 filePath 的值
  router.push({ name: 'note', params: { name: filePath } });
};
fetchFiles();
</script>

<template>
  <div class="common-layout">
    <el-container class="lay-container">
      <el-aside>
        <CommonAside />
      </el-aside>
      <el-container class="r-content">
        <commonHeader/>
        <el-main>
          <div class="file-container">
            <div
                v-for="folder in folders"
                :key="folder.name"
                class="folder-box"
                :style="{ width: getBoxWidth(folder) }"
              >
              <div class="folder-title">{{ folder.name }}</div>
              <ul>
                <li
                  v-for="file in folder.files"
                  :key="file"
                  class="file-item"
                  @click="openFile(folder.name, file)"
                >
                  {{ file }}
                </li>
              </ul>
            </div>
          </div>
          <live2DModel />
        </el-main>
        <CommonFooter />
      </el-container>
    </el-container>
  </div>
</template>

<style scoped>
.file-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  padding: 20px;
  overflow-y: auto;
}

.folder-box {
  color: var(--text-color);
  background-color: var(--background-color);
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 4px;
}

.folder-title {
  text-align: center;
  font-weight: bold;
  margin-bottom: 10px;
}

.file-item {
  margin: 5px 0;
  cursor: pointer;
}

.file-item:hover {
  color: #535bf2;
}
</style>
