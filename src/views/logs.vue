<template>
  <div class="common-layout">
    <el-container class="lay-container">
      <el-aside>
        <CommonAside />
      </el-aside>
      <el-container class="r-content">
        <common-header />
        <live2DModel />
        <CommonFooter />
      </el-container>
    </el-container>
  </div>
  <div class="container">
    <div class="upload-section">
      <img :src="defaultImageSrc" alt="默认图片" class="image" />
      <div class="text">
        <p>{{ textContent }}</p>
      </div>
      <div class="upload-form">
        <form @submit.prevent="submitDiary">
          <div>
            <label for="title">Title:</label>
            <input type="text" id="title" v-model="title" required />
          </div>
          <div>
            <label for="content">Content:</label>
            <textarea id="content" v-model="content" required></textarea>
          </div>
          <div>
            <label for="image">Image:</label>
            <input type="file" id="image" @change="onFileChange" />
          </div>
          <button type="submit">Upload</button>
        </form>
      </div>
    </div>
    <hr class="divider" />
    <div class="diary-section">
      <p>目前一共有 {{ diaries.length }} 条日记</p>
      <div v-for="diary in diaries" :key="diary.id" class="diary-entry">
        <h3>{{ diary.title }}</h3>
        <p>{{ diary.content }}</p>
        <img v-if="diary.imagePath" :src="`../../public/data/log/${diary.imagePath}`" alt="Diary Image" class="diary-image" />
        <button @click="editDiary(diary)">修改</button>
        <button @click="deleteDiary(diary.id)">删除</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import CommonHeader from "../components/CommonHeader.vue";
import CommonAside from "../components/CommonAside.vue";
import CommonFooter from "../components/CommonFooter.vue";
import Live2DModel from "../components/live2d.vue";
import { ref, onMounted } from 'vue';
import axios from 'axios';

const defaultImageSrc = ref('../../public/blender.png');
// const textContent = ref('这是一段用于测试的文字内容');
const title = ref('');
const content = ref('');
const imageFile = ref<File | null>(null);
const diaries = ref([]);
const currentDiaryId = ref<number | null>(null);

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    imageFile.value = target.files[0];
  }
};

const submitDiary = async () => {
  const formData = new FormData();
  formData.append('title', title.value);
  formData.append('content', content.value);

  // 检查是否有图片文件，如果没有则使用默认图片
  if (imageFile.value) {
    formData.append('image', imageFile.value);
  } else {
    const defaultImage = new File([''], 'blender.png', { type: 'image/png' });
    formData.append('image', defaultImage);
  }

  try {
    const response = await axios.post('http://127.0.0.1:5000/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    alert('Content uploaded successfully!');
    fetchDiaries(); // 上传成功后重新获取日记条目
  } catch (error) {
    alert('Error uploading content.');
  }
};


const deleteDiary = async (id: number) => {
  try {
    const response = await axios.delete(`http://127.0.0.1:5000/api/diaries/${id}`);
    alert('Diary deleted successfully!');
    fetchDiaries(); // 删除成功后重新获取日记条目
  } catch (error) {
    alert('Error deleting diary.');
  }
};


const fetchDiaries = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/diaries');
    diaries.value = response.data;
    console.log('Fetched diaries:', diaries.value); // 添加日志
  } catch (error) {
    console.error('Error fetching diaries:', error); // 添加日志
    alert('Error fetching diaries.');
  }
};

const editDiary = (diary: any) => {
  currentDiaryId.value = diary.id;
  title.value = diary.title;
  content.value = diary.content;
  imageFile.value = null; // 清空图片文件
  // 你可以选择是否清空图片路径
  // defaultImageSrc.value = diary.imagePath || '../../public/blender.png';
};

const updateDiary = async () => {
  if (currentDiaryId.value === null) {
    alert('No diary selected for update.');
    return;
  }

  const formData = new FormData();
  formData.append('title', title.value);
  formData.append('content', content.value);
  if (imageFile.value) {
    formData.append('image', imageFile.value);
  }

  try {
    const response = await axios.put('http://127.0.0.1:5000/api/diaries/${currentDiaryId.value}', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    alert('Diary updated successfully!');
    fetchDiaries(); // 更新成功后重新获取日记条目
    // 清空表单
    currentDiaryId.value = null;
    title.value = '';
    content.value = '';
    imageFile.value = null;
  } catch (error) {
    alert('Error updating diary.');
  }
};

onMounted(() => {
  fetchDiaries();
});
</script>

<style scoped>
.container {
  border: 2px solid #e0e0e0;
  padding: 20px;
  border-radius: 10px;
  background-color: var(--background-color);
  position: fixed;
  left: 180px;
  top: 60px;
  bottom: 60px;
  right: 40px; /* 你可以根据需要调整右边距 */
  overflow: auto; /* 如果内容超出容器高度，可以滚动 */
  overflow-x: hidden;
}


.image {
  width: 150px;
  height: auto;
  margin-right: 20px;
}

.text {
  flex: 1;
}

.upload-form {
  margin: 20px;
}

.upload-form form {
  display: flex;
  flex-direction: column;
  transition: background-color 0.3s ease;

}

.upload-form div {
  margin-bottom: 10px;
}

.upload-form label {
  margin-bottom: 5px;
}

.upload-form input,
.upload-form textarea {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 3px;
}

.upload-form button {
  background-color: #28a745;
}

.upload-form button:hover {
  background-color: #218838;
}

.divider {
  width: 100%;
  border: 1px solid black;
  margin: 20px 0;
}

.diary-section {
  width: 100%;
}

.diary-entry {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
}

.diary-image {
  width: 400px;
  height: auto;
  margin-top: 10px;
  transition: transform 0.3s ease;
}

.diary-image:hover {
  transform: scale(1.1);
}
</style>
