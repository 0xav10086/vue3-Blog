<template>
  <div class="common-layout">
    <el-container class="lay-container">
        <CommonAside />
      <el-container class="r-content">
        <common-header />
        <div class="content-wrapper">
          <h1 class="title">{{ title }}</h1>
          <div class="markdown-body" v-html="content" />
        </div>
        <CommonFooter />
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, watchEffect, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { marked } from 'marked';
import axios from 'axios';
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css';
import CommonFooter from "../components/CommonFooter.vue";
import CommonAside from "../components/CommonAside.vue";
import CommonHeader from "../components/CommonHeader.vue";

// 设置 marked 以使用 highlight.js 进行语法高亮
marked.setOptions({
  highlight: function (code, lang) {
    const language = hljs.getLanguage(lang) ? lang : 'plaintext';
    return hljs.highlight(code, { language }).value;
  },
});

// 处理代码块添加复制按钮
marked.use({
  renderer: {
    code(code, lang) {
      const language = hljs.getLanguage(lang) ? lang : 'plaintext';
      const highlighted = hljs.highlight(code, { language }).value;
      return `
        <div class="code-block">
          <button class="copy-button" onclick="copyToClipboard(this)">复制</button>
          <pre><code class="hljs ${lang}">${highlighted}</code></pre>
        </div>`;
    }
  }
});

const route = useRoute();
const content = ref('');
const title = ref(''); // 新增的标题状态

watchEffect(() => {
  if (route.params.name) {
    const filePath = `../../public/data/note/${route.params.name}`;
    console.log(filePath);
    title.value = route.params.name.split('/').pop();

    axios.get(filePath)
      .then(response => {
        if (response.status === 200) {
          console.log(response.data)
          return response.data;
        } else {
          throw new Error(`Failed to fetch Markdown file, status: ${response.status}`);
        }
      })
      .then(mdContent => {
        content.value = marked(mdContent);
      })
      .catch(error => {
        console.error('Failed to load MD file:', error);
      });
  }
});

// 为代码块复制功能添加 JavaScript
onMounted(() => {
  window.copyToClipboard = function (button) {
    const codeBlock = button.nextElementSibling.querySelector('code');
    navigator.clipboard.writeText(codeBlock.innerText).then(() => {
      button.textContent = '已复制';
      setTimeout(() => {
        button.textContent = '复制';
      }, 2000);
    }).catch(err => {
      console.error('Failed to copy: ', err);
    });
  };
});
</script>

<style>
/* 导入 GitHub 风格的 Markdown 样式 */
@import 'https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/4.0.0/github-markdown.min.css';

/* 为 markdown-body 设置样式 */
.markdown-body {
  box-sizing: border-box;
  min-width: 200px;
  max-width: 980px;
  margin: 0 auto;
  padding: 45px;
  text-align: left; /* 左对齐文本 */
  color: var(--text-color);
}

/* 代码块和复制按钮样式 */
.code-block {
  position: relative;
  background-color: var(--background-color); /* 设置代码块背景颜色 */
  border: 1px solid; /* 设置代码块边框颜色 */
  border-radius: 6px; /* 设置代码块边框圆角 */
  padding: 16px; /* 设置代码块内边距 */
  overflow: auto; /* 允许代码块内容溢出时滚动 */
  margin-bottom: 16px; /* 设置代码块与其他内容的间距 */
}

.copy-button {
  position: absolute;
  top: 8px; /* 调整按钮位置 */
  right: 8px; /* 调整按钮位置 */
  background: var(--background-color);
  border: none;
  color: var(--text-color);
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 4px; /* 设置按钮边框圆角 */
}

.copy-button:hover {
  background: gray;
}

.hljs {
  padding: 0; /* 移除代码块内的默认内边距 */
  color: var(--text-color);
}

.markdown-body .highlight pre, .markdown-body pre {
  padding: 16px;
  overflow: auto;
  font-size: 85%;
  line-height: 1.45;
  color: var(--text-color);
  background-color: var(--background-color); /* 设置背景颜色为黑色 */
  border-radius: 3px;
}

/* 新增的样式 */
.content-wrapper {
  margin-top: 60px; /* 整体下移60px */
}

.title {
  font-size: 60px; /* 设置标题的字体大小 */
  text-align: left; /* 左对齐文本 */
  margin: 0; /* 移除默认的 margin */
  padding: 0 45px; /* 与 markdown-body 一致的 padding */
}
</style>
