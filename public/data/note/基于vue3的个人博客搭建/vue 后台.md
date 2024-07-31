# 前言

本文主要是根据项目[vue-element-admin](https://github.com/PanJiaChen/vue-element-admin/tree/master)修改而来，在其中会追加一些笔者不熟悉的东西

# 目录结构

```
├── build // 构建相关   
├── config // 配置相关 
├── src // 源代码 
│   ├── api // 所有请求 
│   ├── assets // 主题 字体等静态资源 
│   ├── components // 全局公用组件 
│   ├── directive // 全局指令 
│   ├── filtres // 全局 filter 
│   ├── icons // 项目所有 svg icons 
│   ├── lang // 国际化 language 
│   ├── mock // 项目mock 模拟数据 
│   ├── router // 路由 
│   ├── store // 全局 store管理 
│   ├── styles // 全局样式 
│   ├── utils // 全局公用方法 
│   ├── vendor // 公用vendor 
│   ├── views // view 
│   ├── App.vue // 入口页面 
│   ├── main.js // 入口 加载组件 初始化等 
│ └── permission.js // 权限管理 
├── static // 第三方不打包资源 
│   └── Tinymce // 富文本 
├── .babelrc // babel-loader 配置 
├── eslintrc.js // eslint 配置项 
├── .gitignore // git 忽略项 
├── favicon.ico // favicon图标 
├── index.html // html模板 
└── package.json // package.json
```

## 理解
### API
[API，即**应用程序编程接口**（Application Programming Interface），是一组规则和协议，它允许不同的软件应用程序相互通信。简单来说，API就像是一个中间人，帮助一个软件或服务请求另一个软件或服务的数据和功能](https://blog.csdn.net/lph188/article/details/87979601)

api和views两个模块一一对应，方便维护

![[c185f7d37a268a1ff4044ff60f5341c0~tplv-t2oaga2asx-jj-mark_3024_0_0_0_q75.webp]]

### components

在其中放置的是一些全局公用的一些组件，如上传组件、富文本等
建议页面级的组件放置在views文件下

![[a355aa4081709f7d9fecf6dfaf08129d~tplv-t2oaga2asx-jj-mark_3024_0_0_0_q75.webp]]

## 富文本

[富文本，通常指的是包含有格式信息的文本，如字体样式（粗体、斜体等）、颜色、超链接、图像、表格等多媒体元素。它允许用户以多样化的方式展示信息，使得文档更加生动、具有吸引力](https://baike.baidu.com/item/%E5%AF%8C%E6%96%87%E6%9C%AC%E6%A0%BC%E5%BC%8F/1017816)[1](https://baike.baidu.com/item/%E5%AF%8C%E6%96%87%E6%9C%AC%E6%A0%BC%E5%BC%8F/1017816)[2](https://blog.csdn.net/qq_14829643/article/details/135832103)[3](https://docs.pingcode.com/ask/296638.html)。

[在Web开发中，富文本编辑器（如Microsoft Word或网页上的HTML编辑器）能支持这些格式，让用户能够创建视觉上丰富的内容。例如，您可以在博客文章中使用富文本来强调重点，插入图片或视频，或者创建链接到其他网页](https://docs.pingcode.com/ask/296638.html)[3](https://docs.pingcode.com/ask/296638.html)。

[富文本格式（Rich Text Format）即RTF格式，是由微软公司开发的跨平台文档格式。大多数文字处理软件都能读取和保存RTF文档。它是一种方便于不同设备、系统查看的文本和图形文档格式](https://baike.baidu.com/item/%E5%AF%8C%E6%96%87%E6%9C%AC%E6%A0%BC%E5%BC%8F/1017816)[1](https://baike.baidu.com/item/%E5%AF%8C%E6%96%87%E6%9C%AC%E6%A0%BC%E5%BC%8F/1017816)。

[总的来说，富文本提供了比普通文本（纯文本）更丰富的表现力，适用于需要丰富表现形式的场景，如网页内容、广告设计等。但在编程或配置文件中，通常使用纯文本，因为它的简洁性和透明性更适合这些应用场景](https://blog.csdn.net/qq_14829643/article/details/135832103)[2](https://blog.csdn.net/qq_14829643/article/details/135832103)。

## store

根据教程，提醒我们文章模块和评论模块是两个独立的东西，没有必要使用vuex来存储data，在每个页面存放自己的data就可以了，但如登录token，用户信息，或是全局个人偏好设置等需要用vuex来统一管理

不要为了使用vuex而使用vuex！

## Vuex

[Vuex是专门为Vue.js应用程序开发的状态管理模式和库。它采用集中式存储管理应用的所有组件的状态，并以相应的规则保证状态以一种可预测的方式发生变化](https://vuex.vuejs.org/zh/)[1](https://vuex.vuejs.org/zh/)。

具体来说，Vuex能够：

- **集中管理状态**：在大型应用中，多个组件可能需要共享某些状态。Vuex提供了一个集中的地方来存储和管理这些状态，使得状态的变化更加可追踪和可维护。
- **维持状态的一致性**：当多个组件依赖于同一状态时，Vuex确保状态的变化是同步的，防止出现不一致的情况。
- [**调试工具集成**：Vuex集成了Vue的官方调试工具devtools extension，提供了如零配置的time-travel调试、状态快照导入导出等高级调试功能](https://vuex.vuejs.org/zh/)[2](https://bing.com/search?q=Vuex+%E8%83%BD%E5%81%9A%E4%BB%80%E4%B9%88)。

[Vuex的使用场景通常是中到大型的单页应用（SPA），其中组件之间的状态共享较多，需要一个统一的状态管理系统来保持数据的一致性和可维护性。如果您的应用相对简单，可能不需要使用Vuex，可以考虑更简单的状态管理方案](https://vuex.vuejs.org/zh/)[1](https://vuex.vuejs.org/zh/)。但对于复杂的应用，Vuex提供了一种结构化和集中管理状态的有效方式。如果您在构建个人博客时需要管理多个组件共享的状态，如用户认证信息、主题设置等，Vuex将是一个很好的选择。