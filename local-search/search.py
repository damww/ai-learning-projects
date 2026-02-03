#!/usr/bin/env python3
"""
本地搜索工具 - 使用DuckDuckGo无需API key
"""

import sys
import json
import requests
from bs4 import BeautifulSoup

def search(query, max_results=5, language="zh-CN"):
    """
    使用DuckDuckGo进行搜索

    Args:
        query: 搜索关键词
        max_results: 返回结果数量
        language: 语言设置 (zh-CN, en-US)

    Returns:
        JSON格式的搜索结果
    """
    try:
        # DuckDuckGo HTML搜索URL
        url = "https://duckduckgo.com/html/"
        params = {
            "q": query,
            "kl": language,
            "num": max_results
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        # 解析搜索结果
        for result in soup.select(".result"):
            try:
                title_elem = result.select_one(".result__title a")
                snippet_elem = result.select_one(".result__snippet")
                url_elem = result.select_one(".result__url")

                if title_elem:
                    results.append({
                        "title": title_elem.get_text(strip=True),
                        "url": title_elem.get("href", ""),
                        "snippet": snippet_elem.get_text(strip=True) if snippet_elem else "",
                        "display_url": url_elem.get_text(strip=True) if url_elem else ""
                    })

                if len(results) >= max_results:
                    break
            except Exception as e:
                continue

        return {
            "success": True,
            "query": query,
            "results": results,
            "count": len(results)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "query": query,
            "results": []
        }

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "Usage: python search.py <query> [max_results] [language]"
        }, ensure_ascii=False))
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    max_results = 5
    language = "zh-CN"

    # 简单的参数解析
    if "--max=" in query:
        parts = query.split("--max=")
        max_results = int(parts[1].split()[0])
        query = parts[0].strip() + " " + parts[1].split(max_results, 1)[-1]

    if "--lang=" in query:
        parts = query.split("--lang=")
        language = parts[1].split()[0]
        query = parts[0].strip() + " " + parts[1].split(language, 1)[-1]

    result = search(query, max_results, language)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
