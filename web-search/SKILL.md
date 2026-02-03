# Web Search Skill

A skill for performing web searches without requiring API keys.

## Description

This skill provides web search functionality using free search services (SearX or DuckDuckGo scraping). No API keys required!

## Usage

### Search

```
/web-search <query>
```

Examples:
```
/web-search OpenClaw documentation
/web-search Python best practices
```

### Fetch and Summarize

```
/web-fetch <url>
```

Fetches a webpage and extracts readable content.

## Configuration

No configuration required! The skill will automatically use available free search services.

## Dependencies

- Python 3.8+
- requests
- beautifulsoup4

## Notes

- Free search services may have rate limits
- Results may vary depending on the service availability
- For production use with high volume, consider using a paid search API
