# 01 中文编码错误
日期：240927

源码：
```C
#include <stdio.h>

int main() {
    int a = 10;
    char c = 'a';
    printf("变量c的ASCII码为：%d", c);
}
```
```output
C:\Users\23203\CLionProjects\untitled\cmake-build-debug\untitled.exe
鍙橀噺c鐨凙SCII鐮佷负锛?7
进程已结束，退出代码为 0
```
## 解决方法：

修改文件编码格式：

1. 打开 File -> Settings -> Editor -> File Encodings。
将 Global Encoding、Project Encoding 和 Default encoding for properties files 全部设置为 UTF-8。
修改注册表信息：

2. 在 CLion 中，按住 Ctrl+Shift+Alt+/，在弹出的小窗口中选择 Registry。
找到 run.processes.with.pty 选项，取消勾选状态12。
确保源代码文件的编码格式为 UTF-8：

3. 在 CLion 中，点击底部状态栏中的文件编码格式，确保其为 UTF-83。

这样设置后，中文输出应该会正常显示。

经实测**方案二**是可行的