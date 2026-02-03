# 浏览器自动化速查表

## 状态管理
```bash
openclaw-cn browser status    # 查看状态
openclaw-cn browser start       # 启动
openclaw-cn browser stop        # 停止
```

## 页面操作
```bash
openclaw-cn browser open <url>              # 打开网页
openclaw-cn browser navigate <url>           # 导航
openclaw-cn browser snapshot                 # 获取快照
openclaw-cn browser screenshot              # 截当前视窗
openclaw-cn browser screenshot --full-page    # 整页截图
```

## 交互操作（需要先 snapshot 获取 ref）
```bash
openclaw-cn browser click <ref>              # 点击
openclaw-cn browser type <ref> "text"         # 输入文本
openclaw-cn browser type <ref> "text" --submit  # 输入并提交
openclaw-cn browser select <ref> "option"     # 选择下拉框
openclaw-cn browser press Enter               # 按键
```

## 标签页管理
```bash
openclaw-cn browser tabs          # 列出所有标签
openclaw-cn browser tab new       # 新建标签
openclaw-cn browser tab select 2  # 选择第2个标签
```

## 调试工具
```bash
openclaw-cn browser console --level error   # 查看控制台错误
openclaw-cn browser errors                 # 查看页面错误
openclaw-cn browser requests --filter api    # 查看网络请求
```

## 配置文件
- `clawd` - 独立管理的浏览器（默认）
- `chrome` - 通过扩展连接你的系统浏览器

## 多配置文件
```bash
openclaw-cn browser --browser-profile work start
openclaw-cn browser --browser-profile work open <url>
```
