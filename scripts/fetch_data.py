"""GR86 Watchダッシュボード用データ(GR86 / BRZ / ロードスター(MX-5))を収集し、
site/data/latest.jsonへ出力する。

30分おきにGitHub Actionsから実行される想定。
"""

from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

from sources import (
    complaints,
    events,
    media_reviews,
    motorsports,
    participant_roster,
    official_news,
    sentiment,
    social_buzz,
    youtube,
)

JST = timezone(timedelta(hours=9))
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "site" / "data" / "latest.json"

YOUTUBE_QUERIES_GLOBAL = {
    "gr86": ["Toyota GR86", "GR86 Cup Edition"],
    "brz": ["Subaru BRZ"],
    "mx5": ["Mazda MX-5 Miata", "Mazda MX-5"],
}

YOUTUBE_QUERIES_JP = {
    "gr86": ["GR86 トヨタ"],
    "brz": ["BRZ スバル"],
    "mx5": ["ロードスター マツダ"],
}


def _with_sentiment(items: list[dict]) -> list[dict]:
    return sentiment.attach_sentiment(items)


def _motorsports_section() -> dict:
    regions = motorsports.fetch()
    for region in regions.values():
        for s in region["series"]:
            s["topics"] = _with_sentiment(s["topics"])
            s["results"] = _with_sentiment(s["results"])
            s["standings"] = _with_sentiment(s["standings"])
    return {
        "label": "モータースポーツ(GR Cup ほか)",
        "regions": regions,
        "note": (
            "トピックス/レース結果はニュース記事ベースで集約しています。Toyota GR Cup(北米)"
            "のみ公式サイト(grcupseries.com)の実データからチーム/ドライバーズランキングと"
            "年間スケジュールをグラフ・一覧表示しています。他の地域/シリーズは公式サイトの"
            "構造上の理由により実データ化しておらず、各カード内に理由を記載のうえニュース"
            "集約とリンクのみとしています。"
        ),
    }


def _roster_section() -> dict:
    data = participant_roster.fetch()
    return {
        "label": "Toyota GR Cup 参戦チーム名簿(北米)",
        **data,
    }


def build_dashboard() -> dict:
    now_utc = datetime.now(timezone.utc)
    now_jst = now_utc.astimezone(JST)

    youtube_global = youtube.fetch_for_vehicles(YOUTUBE_QUERIES_GLOBAL, hl="en", gl="US")
    youtube_jp = youtube.fetch_for_vehicles(YOUTUBE_QUERIES_JP, hl="ja", gl="JP")
    buzz_data = social_buzz.fetch()
    complaint_data = complaints.fetch()

    return {
        "generated_at_utc": now_utc.isoformat(),
        "generated_at_jst": now_jst.strftime("%Y-%m-%d %H:%M JST"),
        "sections": {
            "official_news": {
                "label": "公式リリース(トヨタ/スバル/マツダ)",
                "items": _with_sentiment(official_news.fetch()),
            },
            "youtube_popular": {
                "label": "YouTube 人気動画(グローバル)",
                "items": _with_sentiment(youtube_global["popular"]),
            },
            "youtube_new": {
                "label": "YouTube 新着動画(グローバル)",
                "items": _with_sentiment(youtube_global["new"]),
            },
            "youtube_popular_jp": {
                "label": "YouTube 人気動画(日本語)",
                "items": _with_sentiment(youtube_jp["popular"]),
            },
            "youtube_new_jp": {
                "label": "YouTube 新着動画(日本語)",
                "items": _with_sentiment(youtube_jp["new"]),
            },
            "social_buzz": {
                "label": "SNSでの話題(X/Facebook 代替指標)",
                "items": _with_sentiment(buzz_data["items"]),
                "note": buzz_data["note"],
            },
            "media_reviews": {
                "label": "自動車メディア評価記事",
                "items": _with_sentiment(media_reviews.fetch()),
            },
            "complaints": {
                "label": "お客様の声・クレーム関連情報",
                "items": _with_sentiment(complaint_data["items_latest"]),
                "items_buzz": _with_sentiment(complaint_data["items_buzz"]),
                "note": complaint_data["note"],
            },
            "motorsports": _motorsports_section(),
            "gr_cup_roster": _roster_section(),
            "events": {
                "label": "世界各地のイベント情報",
                "items": _with_sentiment(events.fetch()),
                "note": (
                    "発売告知やスペック発表などのプレスリリース記事は除外し、オーナーズ"
                    "ミーティング/ミートアップ、試乗会・体験会、著名モーターショーへの展示・"
                    "出展など「人が集まる」イベントに絞ってニュース記事から新着順で集約した"
                    "簡易カレンダーです。正確な日程・開催地は記事本文でしか分からないため"
                    "(Google Newsのリンクは本文取得ができない仕組み)、参加を検討する際は"
                    "必ず元記事を開いて日程・場所をご確認ください。公式のイベント日程一覧では"
                    "ありません。"
                ),
            },
        },
    }


def main() -> None:
    dashboard = build_dashboard()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(dashboard, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Wrote dashboard data to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
