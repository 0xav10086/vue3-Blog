<script setup>
import CommonHeader from "../components/CommonHeader.vue";
import CommonAside from "../components/CommonAside.vue";
import CommonFooter from "../components/CommonFooter.vue";
import Live2DModel from "../components/live2d.vue";
import { ElMessageBox, ElMessage } from 'element-plus';

const openMessageBox = () => {
  ElMessageBox.alert('这是一段内容', '标题名称', {
    confirmButtonText: '确定',
    callback: action => {
      ElMessage({
        type: 'info',
        message: `action: ${action}`
      });
    }
  });
};
</script>

<template>
  <div class="common-layout">
    <el-container class="lay-container">
      <el-aside>
        <CommonAside />
      </el-aside>
      <el-container class="r-content">
        <common-header />
        <el-button type="text" @click="openMessageBox">这是日志</el-button>
        <live2DModel />
        <CommonFooter />
      </el-container>
    </el-container>
  </div>
</template>

