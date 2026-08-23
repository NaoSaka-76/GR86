"""GR86 Watchダッシュボード用データ(GR86 / トヨタ86 / BRZ / ロードスター(MX-5))を収集し、
site/data/latest.jsonへ出力する。

30分おきにGitHub Actionsから実行される想定。

セクション構成(2026年9月の再編後):
  1. news_reviews  — GR86/BRZ/ロードスター(MX-5)の公式リリース+メディア評価記事を統合した
                      1パネル(以前はGR86グループ/BRZ・MX-5グループの2パネルに分割していたが、
                      1パネル+フロントエンド側の すべて/GR86/BRZ/ロードスター フィルタに統合)
  2. youtube        — GR86/トヨタ86/BRZ/ロードスターの人気(トレンド)/新着(最新)動画
  3. social_buzz    — 同4車種のSNS話題(トレンド/最新タブ切替)
  4. complaints     — GR86/BRZ/ロードスターのお客様の声・クレーム(トレンド/最新タブ切替)
  5. events         — 世界各地のイベント情報(従来どおり)
  6. motorsports    — GR86モータースポーツ(トピックス速報 + フォーマット静的解説)

(2026年8月: GR Cup北米の参戦チーム名簿セクションは削除。スケジュール/ランキングの実データ
表示は引き続きmotorsportsセクション内に残す。)

トヨタ86(GT86/FT86)はYouTube/SNS話題のみを対象とする(生産終了モデルのため公式リリース/
メディア評価/クレームは対象外。events/motorsportsも対象外)。フロントエンドの すべて/GR86/
BRZ/ロードスター フィルタでは、トヨタ86はGR86バケットに統合して表示する(バックエンド側の
"vehicle"タグ自体は"toyota86"のまま保持し、個別バッジ表示にも使う)。
"""

from __future__ import annotations

from datetime import datetime, timezone, timedelta
import json
from pathlib import Path

from sources import (
    complaints,
    events,
    media_reviews,
    motorsports,
    official_news,
    sentiment,
    social_buzz,
    youtube,
)
from sources.common import sort_by_recency

JST = timezone(timedelta(hours=9))
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "site" / "data" / "latest.json"

YOUTUBE_QUERIES_GLOBAL = {
    "gr86": ["Toyota GR86", "GR86 Cup Edition"],
    "toyota86": ["Toyota 86 GT86", "Toyota FT86"],
    "brz": ["Subaru BRZ"],
    "mx5": ["Mazda MX-5 Miata", "Mazda MX-5"],
}

YOUTUBE_QUERIES_JP = {
    "gr86": ["GR86 トヨタ"],
    "toyota86": ["トヨタ86 GT86", "FT86"],
    "brz": ["BRZ スバル"],
    "mx5": ["ロードスター マツダ"],
}

def _with_sentiment(items: list[dict]) -> list[dict]:
    return sentiment.attach_sentiment(items)


def _news_reviews_section() -> dict:
    """公式リリース(official_news)とメディア評価(media_reviews)をGR86/BRZ/ロードスター
    全車種横断で1つのフィードに統合する。各項目には "kind" (official_news / media_review)
    を付与し、フロントエンド側で種別バッジ・すべて/GR86/BRZ/ロードスターフィルタを出せる
    ようにする(車種別の絞り込みはフロントエンドのフィルタボタンが担い、バックエンド側では
    グループ分けしない)。
    """
    official_items = _with_sentiment(official_news.fetch())
    for item in official_items:
        item["kind"] = "official_news"

    media_items = _with_sentiment(media_reviews.fetch())
    for item in media_items:
        item["kind"] = "media_review"

    combined = sort_by_recency(official_items + media_items)

    return {
        "label": "公式リリース & メディア評価",
        "items": combined,
    }


def _youtube_section() -> dict:
    youtube_global = youtube.fetch_for_vehicles(YOUTUBE_QUERIES_GLOBAL, hl="en", gl="US")
    youtube_jp = youtube.fetch_for_vehicles(YOUTUBE_QUERIES_JP, hl="ja", gl="JP")
    return {
        "label": "YouTube(GR86 / トヨタ86 / BRZ / ロードスター)",
        "global": {
            "popular": _with_sentiment(youtube_global["popular"]),
            "new": _with_sentiment(youtube_global["new"]),
        },
        "jp": {
            "popular": _with_sentiment(youtube_jp["popular"]),
            "new": _with_sentiment(youtube_jp["new"]),
        },
    }


def _social_buzz_section() -> dict:
    buzz_data = social_buzz.fetch()
    return {
        "label": "SNSでの話題(GR86 / トヨタ86 / BRZ / ロードスター)",
        "items": _with_sentiment(buzz_data["items_latest"]),
        "items_buzz": _with_sentiment(buzz_data["items_buzz"]),
        "note": buzz_data["note"],
    }


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
            "トピックス/レース結果はニュース記事ベースで集約しています。Toyota GR Cup(北米)は"
            "チーム/ドライバーズランキングと年間スケジュール、TGR GR86/BRZ Cup(日本)は年間"
            "スケジュール、スーパー耐久 ST-4クラス(日本)は全参戦チーム一覧・参戦ドライバー・"
            "チームランキング・年間スケジュールを、いずれも各公式サイトの実データから取得して"
            "います。それ以外の地域/シリーズは公式サイトの構造上の理由により実データ化しておらず、"
            "各カード内に理由を記載のうえニュース集約とリンクのみとしています。各シリーズの"
            "競技フォーマット(参戦資格・ポイント制度・レースウィークエンド構成)は手動調査の"
            "静的解説(site/data/motorsports_formats.json)を別途ご参照ください。"
        ),
    }


def build_dashboard() -> dict:
    now_utc = datetime.now(timezone.utc)
    now_jst = now_utc.astimezone(JST)

    complaint_data = complaints.fetch()

    sections = {}
    sections["news_reviews"] = _news_reviews_section()
    sections["youtube"] = _youtube_section()
    sections["social_buzz"] = _social_buzz_section()
    sections["complaints"] = {
        "label": "お客様の声・クレーム関連情報(GR86 / BRZ / ロードスター)",
        "items": _with_sentiment(complaint_data["items_latest"]),
        "items_buzz": _with_sentiment(complaint_data["items_buzz"]),
        "note": complaint_data["note"],
    }
    sections["events"] = {
        "label": "世界各地のイベント情報",
        "items": _with_sentiment(events.fetch()),
        "note": (
            "発売告知やスペック発表などのプレスリリース記事は除外し、オーナーズミーティング/"
            "ミートアップ、試乗会・体験会、著名モーターショーへの展示・出展など「人が集まる」"
            "イベントに絞ってニュース記事から新着順で集約した簡易カレンダーです。正確な日程・"
            "開催地は記事本文でしか分からないため(Google Newsのリンクは本文取得ができない"
            "仕組み)、参加を検討する際は必ず元記事を開いて日程・場所をご確認ください。公式の"
            "イベント日程一覧ではありません。"
        ),
    }
    sections["motorsports"] = _motorsports_section()

    return {
        "generated_at_utc": now_utc.isoformat(),
        "generated_at_jst": now_jst.strftime("%Y-%m-%d %H:%M JST"),
        "sections": sections,
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
