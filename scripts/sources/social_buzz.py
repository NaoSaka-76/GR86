"""X(旧Twitter)/Facebookのバズ記事の代替情報を収集する。

X API・Facebook Graph APIの公式キーを利用しないため、SNS投稿そのものは取得できない。
代替として、ニュース/ブログでの言及(Google News RSS)を「話題度」の指標として使う。
(Reddit公開検索APIは2025年時点でボット判定によりブロックされるため不採用)
"""

from __future__ import annotations

from .common import dedupe_by_url, fetch_google_news_rss, sort_by_recency
from .vehicles import build_queries

TOPIC_TERMS = {
    "jp": "話題 OR バズ OR SNS",
    "us": "viral OR trending OR buzz OR \"social media\"",
    "eu": "viral OR trending OR buzz OR \"social media\"",
    "au": "viral OR trending OR buzz OR \"social media\"",
}

QUERIES = build_queries(TOPIC_TERMS)


def fetch(limit_per_query: int = 6) -> dict:
    items: list[dict] = []
    for query, hl, gl, ceid, vehicle in QUERIES:
        results = fetch_google_news_rss(query, hl=hl, gl=gl, ceid=ceid, limit=limit_per_query)
        for r in results:
            r["vehicle"] = vehicle
        items.extend(results)

    return {
        "items": sort_by_recency(dedupe_by_url(items)),
        "note": (
            "X/Facebookの公式APIキーが未設定のため、投稿本体は取得できません。"
            "ニュース・ブログでの言及数を話題性の代替指標として表示しています。"
        ),
    }
