"""自動車メディアによるGR86/BRZ/ロードスター(MX-5)評価記事の収集。"""

from __future__ import annotations

from .common import dedupe_by_url, fetch_google_news_rss, sort_by_recency
from .vehicles import build_queries

TOPIC_TERMS = {
    "jp": "試乗 OR インプレッション OR レビュー",
    "us": (
        "review (site:caranddriver.com OR site:motortrend.com OR site:topgear.com "
        "OR site:roadandtrack.com OR site:thedrive.com OR site:carbuzz.com OR site:autoblog.com)"
    ),
    "eu": "review (site:topgear.com OR site:autocar.co.uk OR site:parkers.co.uk OR site:evo.co.uk)",
    "au": "review (site:carsguide.com.au OR site:whichcar.com.au OR site:drive.com.au)",
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
