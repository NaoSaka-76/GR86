"""X(旧Twitter)/Facebook/Instagram的な「バズ」の代替情報を収集する。

X API・Facebook Graph API・Instagram Graph APIの公式キーを利用しないため、SNS投稿そのものは
取得できない。代替として、ニュース/ブログでの言及(Google News RSS)を「話題度」の指標として
使う。(Reddit公開検索APIは2025年時点でボット判定によりブロックされるため不採用)

対象車種はGR86・トヨタ86(GT86/FT86)・BRZ・ロードスター(MX-5)の4車種
(vehicles.VEHICLES_WITH_TOYOTA86)。トヨタ86は生産終了モデルのため公式リリース/メディア評価
セクションには含めないが、SNS話題・YouTubeでは今なお言及が多いため対象に含める。

complaints.pyと同様、検索結果内での上位表示度(_rank)を「話題順(トレンド)」の代替指標として
使い、"latest"(新着順)と"buzz"(話題順)の2ビューをタブ切り替えできるようにしている。
"""

from __future__ import annotations

from .common import dedupe_by_url, fetch_google_news_rss, sort_by_recency
from .vehicles import VEHICLES_WITH_TOYOTA86, build_queries

TOPIC_TERMS = {
    "jp": "話題 OR バズ OR SNS",
    "us": "viral OR trending OR buzz OR \"social media\"",
    "eu": "viral OR trending OR buzz OR \"social media\"",
    "au": "viral OR trending OR buzz OR \"social media\"",
}

QUERIES = build_queries(TOPIC_TERMS, vehicles=VEHICLES_WITH_TOYOTA86)


def _dedupe_keep_best_rank(items: list[dict]) -> list[dict]:
    """URL重複時は、より上位(_rankが小さい=検索結果内で目立つ)の方を残す。"""
    best: dict[str, dict] = {}
    for item in items:
        key = item.get("url") or item.get("title")
        if not key:
            continue
        if key not in best or item["_rank"] < best[key]["_rank"]:
            best[key] = item
    return list(best.values())


def fetch(limit_per_query: int = 6) -> dict:
    items: list[dict] = []
    for query, hl, gl, ceid, vehicle in QUERIES:
        results = fetch_google_news_rss(query, hl=hl, gl=gl, ceid=ceid, limit=limit_per_query)
        for rank, r in enumerate(results):
            r["vehicle"] = vehicle
            r["_rank"] = rank
        items.extend(results)

    deduped = _dedupe_keep_best_rank(items)
    items_latest = sort_by_recency(deduped)
    items_buzz = sorted(deduped, key=lambda x: x["_rank"])
    for item in deduped:
        item.pop("_rank", None)

    return {
        "items_latest": items_latest,
        "items_buzz": items_buzz,
        "note": (
            "X/Facebook/Instagramの公式APIキーが未設定のため、投稿本体は取得できません。"
            "ニュース・ブログでの言及を話題性の代替指標として表示しています。"
            "「話題順」は検索結果内での上位表示度を注目度の代替指標として用いています"
            "(実際のSNS拡散数やエンゲージメント数ではありません)。"
        ),
    }
