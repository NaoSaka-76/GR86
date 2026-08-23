"""GR86(および追跡対象のBRZ・ロードスター/MX-5)が参戦するモータースポーツ情報。

REGIONS -> series のネスト構造を使う(SKILL.md「Motorsports: many series, grouped by
region」参照)。GR86が実際に参戦を確認できたのは以下:

  - 北米: Toyota GR Cup(grcupseries.com) — GR86 Cup Editionのワンメイクレース。
    公式サイトがTC Americaと同一CMS基盤のため、スケジュール/ランキングとも実データを
    schedule.py/standings.py で取得している(2026年8月に実HTML確認済み)。
  - 日本・アジア: TGR GR86/BRZ Cup(スーパーGT併催、2026年は全7戦)。2026年8月の再調査で
    スケジュールの静的HTMLページ(`/jp/86brz/calendar/{year}/`)が見つかり、実データ化した。
    一方、順位表(`/jp/86brz/ranking/{year}/`)はPDFへのリンクのみでHTML表が存在しないため、
    SKILL.mdが警告する文字化けリスクを避けスクレイピング対象外(ニュース集約+検索リンクの
    まま)。
  - 日本・アジア(追加): スーパー耐久 ST-4クラス — 複数メーカーの市販車ベース車両が混走する
    クラスで、GR86(7チーム)・ロードスター(現行ND型RF、1チーム)が2026年8月時点で実際に
    参戦していることを確認した(BRZの参戦は確認できず)。姉妹プロジェクト"Supra GT4 Watch"の
    `st_supra_teams.py`と同じ技術基盤(supertaikyu.com)で、ST-4クラスの全10チームを一覧
    表示し、該当車種のみハイライトする(`super_taikyu_st4.py`)。日程・チームランキング・
    参戦ドライバーはいずれも公式サイトの実データ。
  - オーストラリア: GR Cup Australia(旧Toyota 86 Racing Series。2024年からGR86に更新)。
    公式サイト(toyota.com.au/gazoo-racing/gr-cup)がHTTP 403を返しスクレイピング不可。
    サードパーティのsupercars.comにセッション単位の実結果ページはあるが、シーズン通算の
    ポイントランキングはどこにも見当たらず、セッションコードの命名規則も安定しないため、
    誤ったURL推測のリスクを避けスクレイピングは見送り(ニュース集約+検索リンクのみ)。
  - 欧州: 2026年8月に前回より広く再調査(GR86 Cup/Trophy Europe、BRZ Cup Europe、独ADAC/
    英750MC・BRSCC等のクラブレース、ニュルブルクリンクVLN/NLSの各クラス、マレーシア含む
    アジア圏の類似名称シリーズとの区別、などを個別に検索)した結果、GR86/BRZの現行ワンメイク
    選手権や、既存クラブレース内の専用クラスは見つからなかった。ただし旧型GT86時代には
    ドイツ・ニュルブルクリンクのVLN(現NLS)耐久シリーズ内に「TMG GT86 Cup」という専用クラス
    が実在した(トヨタ欧州公式発表で2013年開幕・2019年時点でも継続を確認)。現行(2024〜2026年)
    NLSの公式クラス一覧にGT86/BRZ名称は見当たらず、現在もブランド化された独立クラスとして
    継続しているかは確認できなかったため、「現状不明の可能性がある過去実績」として参考掲載
    している(SKILL.mdの「除外の結論は再調査で覆りうる」を踏まえ、前回の簡易調査より広く
    探した結果)。

加えて、ユーザー要望により追跡対象のロードスター(MX-5)が参戦する Mazda MX-5 Cup
(IMSA主催)も1枠設けている。ただしmx-5cup.comはGR CupやTC Americaと異なるCMSで
静的HTMLの型が確認できなかった(構造化データではなくJS描画寄り)ため、スケジュール/
順位表は実データ化せず、ニュース記事集約 + 公式サイトへのリンクのみとしている。

(2026年8月: 参戦チーム名簿セクション(旧participant_roster.py)は削除。スケジュール/
ランキングの実データ表示は引き続きGR Cup北米のみschedule.py/standings.pyで取得している。)
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
from .super_taikyu_st4 import fetch as fetch_super_taikyu_st4


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
                "has_real_schedule": True,
                "has_real_standings": False,
            },
            {
                "key": "super_taikyu_st4",
                "label": "スーパー耐久 ST-4クラス(多メーカー混走・日本)",
                "vehicle": None,
                "queries": {
                    "topics": [
                        ("スーパー耐久 ST-4クラス GR86 OR BRZ OR ロードスター", "ja", "JP", "JP:ja"),
                        ("スーパー耐久 ST4 GR86", "ja", "JP", "JP:ja"),
                    ],
                    "results": [
                        ("スーパー耐久 ST-4クラス 決勝 OR レース結果 OR 優勝", "ja", "JP", "JP:ja"),
                    ],
                    "standings": [
                        ("スーパー耐久 ST-4クラス シリーズランキング OR ポイントランキング", "ja", "JP", "JP:ja"),
                    ],
                },
                "standings_search": "スーパー耐久 ST-4クラス 2026 シリーズランキング",
                "schedule_link": "https://supertaikyu.com/race/index.html",
                "has_real_schedule": True,
                "has_real_standings": True,
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
            }
        ],
    },
    "europe": {
        "label": "欧州",
        "flag": "🇪🇺",
        "series": [
            {
                "key": "tmg_gt86_cup_vln",
                "label": "TMG GT86 Cup(独ニュルブルクリンク VLN/NLS内クラス・現行開催は未確認)",
                "vehicle": "toyota86",
                "queries": {
                    "topics": [
                        ('"GT86 Cup" VLN OR NLS OR Nürburgring', "en-GB", "GB", "GB:en"),
                        ('"GT86 Cup" Nürburgring', "de", "DE", "DE:de"),
                    ],
                    "results": [
                        ('"GT86 Cup" Nürburgring race result OR podium OR win', "en-GB", "GB", "GB:en"),
                    ],
                    "standings": [
                        ('"GT86 Cup" VLN OR NLS standings OR Meisterschaft', "de", "DE", "DE:de"),
                    ],
                },
                "standings_search": "TMG GT86 Cup VLN NLS Nürburgring 2026 status",
                "schedule_link": "https://www.nuerburgring-langstrecken-serie.de/",
                "has_real_schedule": False,
                "has_real_standings": False,
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

    # GR Cup(北米)は、公式サイトの実データでスケジュール/ランキングを埋める。
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

    # 日本(TGR GR86/BRZ Cup)は、公式カレンダーページの実データでスケジュールのみ埋める
    # (順位表はPDFのみのため引き続きリンクアウト)。
    jp = result["japan_asia"]["series"][0]
    jp["schedule"] = schedules["tgr_86brz_cup"]
    jp["standings_chart_note"] = (
        "公式サイトの順位表(ランキング)ページはPDFファイルへのリンクのみで、HTML形式の"
        "順位表が存在しません。ドライバー氏名の文字化けリスク(SKILL.md記載のPDF抽出時の"
        "既知の問題)を避けるため、順位のスクレイピングは行っていません。正式な順位は"
        "「公式ランキングを検索」または公式サイトのPDFでご確認ください。"
    )

    # スーパー耐久 ST-4クラスは、公式サイトの実データでスケジュール・全参戦チーム・
    # ドライバー・ランキングを埋める(GR86/ロードスターのみハイライト、BRZは今季参戦なし)。
    st4 = result["japan_asia"]["series"][1]
    st4["schedule"] = schedules["super_taikyu"]
    st4_data = fetch_super_taikyu_st4()
    st4["roster"] = st4_data["teams"]
    st4["rounds_completed"] = st4_data["rounds_completed"]
    st4["rounds_total"] = st4_data["rounds_total"]
    st4["standings_chart"] = [
        {"position": t["position"], "name": t["team"], "points": t["points"]} for t in st4_data["teams"]
    ]
    st4["standings_chart_note"] = st4_data["error"] or st4_data["note"]

    # 豪州/MX-5 Cupはスクレイピングせずリンクアウトのみである理由を明示する。
    result["australia"]["series"][0]["schedule_chart_note"] = (
        "公式サイトがボット対策等でスクレイピングできなかった(HTTP 403)ため、"
        "ニュース記事の集約と検索リンクのみとしています。"
    )
    result["europe"]["series"][0]["schedule_chart_note"] = (
        "2026年8月の再調査で、旧型GT86時代にドイツ・ニュルブルクリンクのVLN(現NLS)耐久"
        "シリーズ内に「TMG GT86 Cup」という専用クラスが実在したことを確認(2013年開幕、"
        "2019年時点でも継続をトヨタ欧州公式発表で確認)。ただし現行(2024〜2026年)NLSの"
        "公式クラス一覧にGT86/BRZ名称は見当たらず、現在もブランド化された独立クラスとして"
        "継続しているかは確認できませんでした。GR86/BRZの現行ワンメイク選手権・専用クラスは"
        "欧州で見つかっていません(詳細は下記「各シリーズの競技フォーマット解説」参照)。"
    )
    result["mx5_cup"]["series"][0]["schedule_chart_note"] = (
        "mx-5cup.comはGR Cup/TC Americaと異なる基盤で運用されており静的HTMLでの安定した"
        "スケジュール/順位表取得ができなかったため、ニュース記事の集約と公式サイトへの"
        "リンクのみとしています(ロードスター/MX-5は本ダッシュボードの追跡対象車両です)。"
    )

    return result
