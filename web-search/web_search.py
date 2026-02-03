#!/usr/bin/env python3
"""
Web Search Skill - Free web search without API keys
"""

import sys
import json
import re
import urllib.request
import urllib.parse
import ssl
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []
    
    def handle_data(self, d):
        self.fed.append(d)
    
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    try:
        s.feed(html)
        return s.get_data()
    except:
        return html

def duckduckgo_search(query, num_results=5):
    """Search using DuckDuckGo HTML scraping"""
    results = []
    
    try:
        # Create SSL context that doesn't verify certificates
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # URL encode the query
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, context=ssl_context, timeout=10) as response:
            html = response.read().decode('utf-8')
            
            # Extract results using regex
            # DuckDuckGo result pattern
            result_pattern = r'<div class="result[^"]*"[^>]*>.*?<a[^>]*class="result__a"[^>]*href="([^"]*)"[^>]*>(.*?)</a>.*?<a[^>]*class="result__snippet"[^>]*>(.*?)</a>.*?</div>'
            
            matches = re.findall(result_pattern, html, re.DOTALL)
            
            for i, match in enumerate(matches[:num_results]):
                url = match[0]
                title = strip_tags(match[1])
                snippet = strip_tags(match[2])
                
                results.append({
                    'title': title.strip(),
                    'url': url,
                    'snippet': snippet.strip()
                })
                
    except Exception as e:
        results.append({
            'error': f'Search failed: {str(e)}',
            'title': 'Error',
            'url': '',
            'snippet': ''
        })
    
    return results

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            'error': 'Usage: web_search.py <query>',
            'results': []
        }))
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    results = duckduckgo_search(query)
    
    output = {
        'query': query,
        'results': results
    }
    
    print(json.dumps(output, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
