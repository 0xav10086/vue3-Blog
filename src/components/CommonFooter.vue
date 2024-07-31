<template>
  <el-footer class="common-footer">
    <div class="footer-center">
      {{ displayedQuote }}
    </div>
    <div class="footer-right">
      <el-button icon="arrow-left" @click="previousQuote"></el-button>
      <el-button icon="arrow-right" @click="nextQuote"></el-button>
    </div>
  </el-footer>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';

export default {
  setup() {
    const quotes = [
      "老实说，真的会有人看这个吗？",
      "tips:tips:tips:tips:tips:tips",
      "这个网站就是一个笑话，但是还是一个蛮耗时间的笑话",
      "发现点不动了就直接F5刷新，代码是这样的，能跑就行",
      "Success is not how high you have climbed, but how you make a positive difference to the world. - Roy T. Bennett"
    ];
    const currentQuoteIndex = ref(0);
    const currentQuote = ref(quotes[currentQuoteIndex.value]);
    const displayedQuote = ref('');
    let typingTimeout = null;
    let nextQuoteTimeout = null;

    const typeQuote = (quote) => {
      clearTimeout(typingTimeout);
      let index = 0;
      displayedQuote.value = '';
      const type = () => {
        if (index < quote.length) {
          displayedQuote.value += quote.charAt(index);
          index++;
          typingTimeout = setTimeout(type, 80); // 每80ms显示一个字符
        } else {
          startNextQuoteTimer();
        }
      };
      type();
    };

    const startNextQuoteTimer = () => {
      clearTimeout(nextQuoteTimeout);
      nextQuoteTimeout = setTimeout(showNextQuote, 60000); // 名言显示60秒后切换
    };

    const resetQuoteDisplay = () => {
      clearTimeout(typingTimeout);
      clearTimeout(nextQuoteTimeout);
      displayedQuote.value = '';
    };

    const showNextQuote = () => {
      currentQuoteIndex.value = (currentQuoteIndex.value + 1) % quotes.length;
      currentQuote.value = quotes[currentQuoteIndex.value];
      resetQuoteDisplay();
      typeQuote(currentQuote.value);
    };

    const previousQuote = () => {
      currentQuoteIndex.value = (currentQuoteIndex.value - 1 + quotes.length) % quotes.length;
      currentQuote.value = quotes[currentQuoteIndex.value];
      resetQuoteDisplay();
      typeQuote(currentQuote.value);
    };

    const nextQuote = () => {
      currentQuoteIndex.value = (currentQuoteIndex.value + 1) % quotes.length;
      currentQuote.value = quotes[currentQuoteIndex.value];
      resetQuoteDisplay();
      typeQuote(currentQuote.value);
    };

    onMounted(() => {
      typeQuote(currentQuote.value);
    });

    onBeforeUnmount(() => {
      clearTimeout(typingTimeout);
      clearTimeout(nextQuoteTimeout);
    });

    return {
      displayedQuote,
      previousQuote,
      nextQuote
    };
  }
};
</script>

<style scoped>
.common-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background: var(--footer-background-color);
  color: var(--footer-text-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  box-sizing: border-box;
  z-index: 1000;
}

.footer-center {
  flex: 1;
  text-align: center;
}

.footer-right {
  display: flex;
  align-items: center;
}

.footer-right .el-button {
  margin-left: 5px;
}
</style>
