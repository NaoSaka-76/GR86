"""GR86(および追跡対象のBRZ・ロードスター/MX-5)が参戦するモータースポーツ情報。

REGIONS -> series のネスト構造を使う(SKILL.md「Motorsports: many series, grouped by
region」参照)。GR86が実際に参戦を確認できたのは以下:

  - 北米: Toyota GR Cup(grcupseries.com) — GR86 Cup Editionのワンメイクレース。
    公式サイトがTC Americaと同一CMS基盤のため、スケジュール/ランキングとも実データを
    scheduke.py/standings.py/participant_roster.py で取得している(2026年8月に実HTML確認済み)。
  - 日本・アジア: TGR GR86/BRZ Cup(スーパーGT併催、2026年は全7戦)。
    toyotagazooracing.com/jp/86brz/about/ に概要はあるが、静的HTMLのスケジュール表/順位表
    ページは確認できなかった(2026年8月時点)ため、ニュース記事集約 + 公式ページへの
    リンクのみ。
  - オーストラリア: GR Cup Australia(旧Toyota 86 Racing Series。2024年からGR86に更新)。
    公式サイト(toyota.com.au/gazoo-racing/gr-cup)がHTTP 403を返しスクレイピング不可のため、
    ニュース記事集約 + 検索リンクのみ。
  - 欧州: 2026年8月時点でGR86の現行ワンメイク/プロダクションクラス選手権は確認できず、
    セクション自体を設けていない(SKILL.mdの「参戦していないシリーズのセクションは
    作らない」の教訓どおり)。

加えて、ユーザー要望により追跡対象のロードスター(MX-5)が参戦する Mazda MX-5 Cup
(IMSA主催)も1枠設けている。ただしmx-5cup.comはGR CupやTC Americaと異なるCMSで
静的HTMLの型が確認できなかった(構造化データではなくJS描画寄り)ため、スケジュール/
順位表は実データ化せず、ニュース記事集約 + 公式サイトへのリンクのみとしている
(GR86のロースター/参戦チーム名簿はGR Cupのみ構築 — 参戦車種が異なるMX-5 Cupまで
同水準の名簿調査を行うとスコープが膨らみすぎるため、SKILL.mdの「ロースターは
実際に要望された場合のみ」の原則に従いリンクアウトに留めている)。
"""

from __future__ import annotations

import urllib.parse

from .common import dedupe_by_url, fetch_google_news_rss, sort_by_recency
from .schedule import (
    GR_CUP_AUSTRALIA_URL,
    GR_CUP_CALENDAR_URL,
    JP_86BRZ_CUP_URL,
    MX5_CUP_SCHEDULE_URL,
)
from .schedule import fetch_all as fetch_all_schedules
from .standings import fetch_gr_cup_driver_standings, fetch_gr_cup_team_standings


def _search_link(query: str) -> str:
    return "https://www.google.com/search?q=" + urllib.parse.quote(query)


REGIONS = {
    "north_america": {
        "label": "北米",
        "flag": "🇺🇸",
        "series": [
            {
                "key": "gr_cup",
                "label": "Toyota GR Cup(GR86 Cup Edition ワンメイクレース)",
                "vehicle": "gr86",
                "queries": {
                    "topics": [
                        ('"GR Cup" "GR86" Toyota', "en-US", "US", "US:en"),
                        ('"GR Cup" GR86 series news', "en-US", "US", "US:en"),
                    ],
                    "results": [
                        ('"GR Cup" GR86 race result OR podium OR win OR finish', "en-US", "US", "US:en"),
                    ],
                    "standings": [
                        ('"GR Cup" championship standings GR86', "en-US", "US", "US:en"),
                    ],
                },
                "standings_search": "Toyota GR Cup GR86 championship standings 2026",
                "schedule_link": GR_CUP_CALENDAR_URL,
                "has_real_schedule": True,
                "has_real_standings": True,
                "has_roster": True,
            }
        ],
    },
    "japan_asia": {
        "label": "日本・アジア",
        "flag": "🇯🇵",
        "series": [
            {
                "key": "tgr_86brz_cup",
                "label": "TGR GR86/BRZ Cup(スーパーGT併催・日本)",
                "vehicle": "gr86",
                "queries": {
                    "topics": [
                        ("GR86 BRZ Cup TOYOTA GAZOO Racing", "ja", "JP", "JP:ja"),
                        ("86 BRZ レース スーパーGT 併催", "ja", "JP", "JP:ja"),
                    ],
                    "results": [
                        ("GR86 BRZ Cup 決勝 OR レース結果 OR 優勝", "ja", "JP", "JP:ja"),
                    ],
                    "standings": [
                        ("GR86 BRZ Cup シリーズランキング OR ポイントランキング", "ja", "JP", "JP:ja"),
                    ],
                },
                "standings_search": "TGR GR86 BRZ Cup 2026 シリーズランキング",
                "schedule_link": JP_86BRZ_CUP_URL,
                "has_real_schedule": False,
                "has_real_standings": False,
                "has_roster": False,
            }
        ],
    },
    "australia": {
        "label": "オーストラリア",
        "flag": "🇦🇺",
        "series": [
            {
                "key": "gr_cup_australia",
                "label": "GR Cup Australia(旧Toyota 86 Racing Series)",
                "vehicle": "gr86",
                "queries": {
                    "topics": [
                        ('"GR Cup" Australia Toyota GR86', "en-AU", "AU", "AU:en"),
                        ("Toyota 86 Racing Series Australia", "en-AU", "AU", "AU:en"),
                    ],
                    "results": [
                        ('"GR Cup" Australia race result OR podium OR win', "en-AU", "AU", "AU:en"),
                    ],
                    "standings": [
                        ('"GR Cup" Australia championship standings', "en-AU", "AU", "AU:en"),
                    ],
                },
                "standings_search": "GR Cup Australia 2026 championship standings",
                "schedule_link": GR_CUP_AUSTRALIA_URL,
                "has_real_schedule": False,
                "has_real_standings": False,
                "has_roster": False,
            }
        ],
    },
    "mx5_cup": {
        "label": "ロードスター(MX-5)ワンメイク",
        "flag": "🇺🇸",
        "series": [
            {
                "key": "mx5_cup",
                "label": "Mazda MX-5 Cup(IMSA主催・北米)",
                "vehicle": "mx5",
                "queries": {
                    "topics": [
                        ('"MX-5 Cup" Mazda', "en-US", "US", "US:en"),
                    ],
                    "results": [
                        ('"MX-5 Cup" race result OR podium OR win OR finish', "en-US", "US", "US:en"),
                    ],
                    "standings": [
                        ('"MX-5 Cup" championship standings', "en-US", "US", "US:en"),
                    ],
                },
                "standings_search": "Mazda MX-5 Cup 2026 championship standings",
                "schedule_link": MX5_CUP_SCHEDULE_URL,
                "has_real_schedule": False,
                "has_real_standings": False,
                "has_roster": False,
            }
        ],
    },
}


def _fetch_group(query_list: list[tuple], limit: int = 5, vehicle: str | None = None) -> list[dict]:
    items: list[dict] = []
    for query, hl, gl, ceid in query_list:
        results = fetch_google_news_rss(query, hl=hl, gl=gl, ceid=ceid, limit=limit)
        for r in results:
            r["vehicle"] = vehicle
        items.extend(results)
    return sort_by_recency(dedupe_by_url(items))


def fetch() -> dict:
    result: dict = {}
    for region_key, region in REGIONS.items():
        series_out = []
        for series in region["series"]:
            series_out.append(
                {
                    "key": series["key"],
                    "label": series["label"],
                    "vehicle": series["vehicle"],
                    "topics": _fetch_group(series["queries"]["topics"], vehicle=series["vehicle"]),
                    "results": _fetch_group(series["queries"]["results"], vehicle=series["vehicle"]),
                    "standings": _fetch_group(series["queries"]["standings"], vehicle=series["vehicle"]),
                    "standings_search_url": _search_link(series["standings_search"]),
                    "schedule_link": series["schedule_link"],
                    "has_real_schedule": series["has_real_schedule"],
                    "has_real_standings": series["has_real_standings"],
                    "schedule": [],
                    "standings_chart": None,
                    "standings_chart_note": None,
                    "roster": None,
                }
            )
        result[region_key] = {"label": region["label"], "flag": region["flag"], "series": series_out}

    # GR Cup(北米)のみ、公式サイトの実データでスケジュール/ランキング/名簿を埋める。
    gr_cup = result["north_america"]["series"][0]
    schedules = fetch_all_schedules()
    gr_cup["schedule"] = schedules["gr_cup"]

    team_standings = fetch_gr_cup_team_standings(limit=15)
    driver_standings = fetch_gr_cup_driver_standings(limit=15)
    gr_cup["standings_chart"] = team_standings["standings"]
    gr_cup["driver_standings_chart"] = driver_standings["standings"]
    gr_cup["standings_chart_note"] = (
        team_standings["error"]
        or "Toyota GR Cup「GR Cup AM」クラス チームズランキング(公式サイト実データ)。"
        "ドライバーズランキングも別枠で表示しています。"
    )

    # 日本/豪州/MX-5 Cupはスクレイピングせずリンクアウトのみである理由を明示する。
    result["japan_asia"]["series"][0]["schedule_chart_note"] = (
        "公式ページに静的HTMLのスケジュール表/順位表が見当たらなかったため、"
        "ニュース記事の集約と公式ページへのリンクのみとしています。"
    )
    result["australia"]["series"][0]["schedule_chart_note"] = (
        "公式サイトがボット対策等でスクレイピングできなかった(HTTP 403)ため、"
        "ニュース記事の集約と検索リンクのみとしています。"
    )
    result["mx5_cup"]["series"][0]["schedule_chart_note"] = (
        "mx-5cup.comはGR Cup/TC Americaと異なる基盤で運用されており静的HTMLでの安定した"
        "スケジュール/順位表取得ができなかったため、ニュース記事の集約と公式サイトへの"
        "リンクのみとしています(ロードスター/MX-5は本ダッシュボードの追跡対象車両です)。"
    )

    return result
