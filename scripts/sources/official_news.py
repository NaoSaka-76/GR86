"""トヨタ(GR86)・スバル(BRZ)・マツダ(ロードスター/MX-5)、および各地域販売会社からの
公式リリース情報。日本(GR86/BRZ)・北米・欧州・豪州の4地域すべてでクエリを組む。
"""

from __future__ import annotations

from .common import dedupe_by_url, fetch_google_news_rss, sort_by_recency
from .vehicles import build_queries

TOPIC_TERMS = {
    "jp": "発表 OR 発売 OR 新型 OR 一部改良",
    "us": "press release OR announcement OR debut",
    "eu": "press release OR announcement OR debut",
    "au": "press release OR announcement OR debut",
}

QUERIES = build_queries(TOPIC_TERMS)


def fetch(limit_per_query: int = 6) -> list[dict]:
    items: list[dict] = []
    for query, hl, gl, ceid, vehicle in QUERIES:
        results = fetch_google_news_rss(query, hl=hl, gl=gl, ceid=ceid, limit=limit_per_query)
        for r in results:
            r["vehicle"] = vehicle
        items.extend(results)
    return sort_by_recency(dedupe_by_url(items))
