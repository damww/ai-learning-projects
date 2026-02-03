# Browser Helper Skill

浏览器自动化助手 - 帮助AI使用浏览器工具

## 快速开始

### 基础命令

```bash
# 查看浏览器状态
openclaw-cn browser status

# 启动浏览器
openclaw-cn browser start

# 打开网页
openclaw-cn browser open https://example.com

# 获取页面快照
openclaw-cn browser snapshot

# 截图
openclaw-cn browser screenshot
```

### 常用场景

**场景1：搜索内容**
1. 打开搜索引擎
2. 输入搜索关键词
3. 获取结果
4. 提取有用信息

**场景2：表单提交**
1. 打开表单页面
2. 填写表单字段
3. 提交
4. 验证结果

## 注意事项

- 浏览器与个人浏览器完全隔离
- 使用 `--browser-profile` 可以切换不同配置
- 元素操作需要先获取快照（ref）
