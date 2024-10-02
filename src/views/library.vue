<script setup>
import CommonHeader from "../components/CommonHeader.vue";
import CommonAside from "../components/CommonAside.vue";
import CommonFooter from "../components/CommonFooter.vue";
import Live2DModel from "../components/live2d.vue";

</script>

<template>
  <div class="common-layout">
    <el-container class="lay-container">
      <el-aside>
        <CommonAside />
      </el-aside>
      <el-container class="r-content">
        <common-header />
        <p>这是书库，还没写呢</p>
        <live2DModel />
        <CommonFooter />
      </el-container>
    </el-container>
  </div>
</template>

