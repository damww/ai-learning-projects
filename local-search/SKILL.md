# Local Search Skill

本地搜索技能，无需外部API key，使用DuckDuckGo实现。

## 功能

- 执行网络搜索（DuckDuckGo）
- 提取搜索结果标题、URL、摘要
- 支持多语言搜索

## 方法

在Agent中调用此技能即可执行搜索，无需配置任何API key。

## 实现

使用Python requests + BeautifulSoup解析DuckDuckGo HTML搜索结果。
