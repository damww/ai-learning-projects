#!/bin/bash
# 本地搜索脚本 - 使用浏览器自动化
# 无需API key，通过浏览器搜索引擎获取结果

QUERY="$1"
MAX_RESULTS="${2:-5}"

if [ -z "$QUERY" ]; then
    cat << EOF
Usage: ./browser-search.sh "搜索关键词" [结果数量]

示例：
  ./browser-search.sh "中电金信 面试题" 5
  ./browser-search.sh "PyTorch 教程" 3
EOF
    exit 1
fi

echo "🔍 正在搜索: $QUERY"
echo "📊 最大结果数: $MAX_RESULTS"
echo ""

# 启动浏览器
echo "1️⃣  启动浏览器..."
openclaw-cn browser start

# 打开搜索页面
echo "2️⃣  打开搜索页面..."
SEARCH_URL="https://www.bing.com/search?q=$(echo "$QUERY" | sed 's/ /+/g')"
openclaw-cn browser open "$SEARCH_URL"

# 等待页面加载
sleep 3

# 获取页面快照
echo "3️⃣  获取搜索结果..."
openclaw-cn browser snapshot --interactive

echo ""
echo "✅ 搜索完成！"
echo ""
echo "提示："
echo "  - 使用 openclaw-cn browser screenshot 截图"
echo "  - 使用 openclaw-cn browser snapshot --interactive 查看可交互元素"
