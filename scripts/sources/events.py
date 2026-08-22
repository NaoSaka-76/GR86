"""世界各地で開催・企画されている、GR86/BRZ/ロードスター(MX-5)に関する
「人が集まる」イベント情報の収集。

オーナーズミーティング/ミートアップ、試乗会・体験会、著名モーターショーへの展示・出展のみに
絞って集約する。「event」「unveil」「showcase」のような一般的すぎる語だけの検索は、発売告知・
スペック発表などのプレスリリース記事まで拾ってしまうため使わない(SKILL.mdの教訓)。

Google News RSSは見出し文のみで、記事本文・実際の日程/開催地はリンク先を開かないと
分からない(Googleの記事リンクはJavaScriptによるリダイレクトが必要でRSS側からは
本文取得ができない)。参加を検討する場合は必ず元記事で日程・開催地を確認すること。
公式のイベントカレンダーではなく、ニュース記事ベースの簡易集約。新着順で表示する。
"""

from __future__ import annotations

from .common import dedupe_by_url, fetch_google_news_rss, sort_by_recency
from .vehicles import build_queries

# オーナーズミーティング/ミートアップ
_MEET_TERMS = {
    "jp": "(オーナーズミーティング OR オーナーミーティング OR オーナー会 OR ミートアップ)",
    "us": '("owners meet" OR "owners club" OR "car meet" OR meetup OR "owners gathering")',
    "eu": '("owners meet" OR "owners club" OR "car meet" OR meetup OR "owners gathering")',
    "au": '("owners meet" OR "owners club" OR "car meet" OR meetup OR "owners gathering")',
}

# 試乗会・体験会・お披露目会
_TEST_DRIVE_TERMS = {
    "jp": "(試乗会 OR 体験会 OR お披露目会 OR 試乗イベント)",
    "us": '("test drive event" OR "ride and drive" OR "meet and greet")',
    "eu": '("test drive event" OR "ride and drive" OR "meet and greet")',
    "au": '("test drive event" OR "ride and drive" OR "meet and greet")',
}

# 著名モーターショーでの展示・出展(発表記事ではなく会場での展示に限定)
_SHOW_TERMS = {
    "jp": "(オートサロン OR モーターショー OR モータショー) (出展 OR 展示)",
    "us": '("Tokyo Auto Salon" OR "SEMA Show" OR "Goodwood Festival of Speed") (display OR exhibit OR exhibiting)',
    "eu": '("Goodwood Festival of Speed" OR "Goodwood Speed Week") (display OR exhibit OR exhibiting)',
    "au": '("Australian Auto Show" OR "Motorclassica") (display OR exhibit OR exhibiting)',
}


def fetch(limit_per_query: int = 5) -> list[dict]:
    items: list[dict] = []
    for topic_terms in (_MEET_TERMS, _TEST_DRIVE_TERMS, _SHOW_TERMS):
        for query, hl, gl, ceid, vehicle in build_queries(topic_terms):
            results = fetch_google_news_rss(query, hl=hl, gl=gl, ceid=ceid, limit=limit_per_query)
            for r in results:
                r["vehicle"] = vehicle
            items.extend(results)
    return sort_by_recency(dedupe_by_url(items))
