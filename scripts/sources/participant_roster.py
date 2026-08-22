"""Toyota GR Cup(北米, GR86 Cup Edition ワンメイクレース)の参戦チーム名簿。

背景情報(運営母体・実績)は静的な手動収集データとして PARTICIPANTS に持ち、現在の
チームズランキング/ポイントは standings.py 経由で毎回実データを取得する(2026年8月に
grcupseries.com/standings で実際に確認済み)。

「今シーズンここまでに参加した全ドライバー」は、開幕から直近の開催済みラウンドまでの
公式エントリーリスト(HTML)を集計してユニオンする。grcupseries.com/entry-lists に
ラウンドごとのHTML表(車番/ドライバー名/チーム名/車種/クラス)が公開されており、
PDFではないため氏名抽出の信頼性が高い(SKILL.mdが警告するPDF文字化けの罠を回避できる)。
ラウンドをまたいで表記が微妙に異なる可能性のある同一人物名を勝手に統合することはせず、
公式データの表記のまま(重複があれば重複のまま)保持する。

チーム名をキーにチームズランキングとエントリーリストを突き合わせている(GR Cupは
1チームが複数台をエントリーすることがあり、車番単位ではなくチーム名単位でのマッチングの方が
実態に合う)。
"""

from __future__ import annotations

import re
from datetime import date

import requests

from .common import REQUEST_TIMEOUT, USER_AGENT
from .standings import fetch_gr_cup_team_standings

BASE_URL = "https://www.grcupseries.com"
ENTRY_LIST_URL = BASE_URL + "/entry-list/2026/{slug}"

# 2026シーズンの開催ラウンド(週末単位。1週末に2レースが組まれる)。
# エントリーリストは週末単位で1枚しか公開されないため、ラウンド番号ではなく週末単位で扱う。
# 終了日は schedule.py が公式カレンダーから取得する日程と揃えている(2026年8月時点)。
ROUND_WEEKENDS = [
    {"round_label": "Round 1 & 2", "slug": "grand-prix-of-arlington", "track": "Grand Prix of Arlington", "end_date": date(2026, 3, 15)},
    {"round_label": "Round 3 & 4", "slug": "sonoma-raceway", "track": "Sonoma Raceway", "end_date": date(2026, 3, 29)},
    {"round_label": "Round 5 & 6", "slug": "Circuit-of-the-Americas", "track": "Circuit of The Americas", "end_date": date(2026, 4, 26)},
    {"round_label": "Round 7 & 8", "slug": "road-atlanta", "track": "Michelin Raceway Road Atlanta", "end_date": date(2026, 6, 14)},
    {"round_label": "Round 9 & 10", "slug": "road-america", "track": "Road America", "end_date": date(2026, 8, 30)},
]

# 背景情報(運営母体・実績)は手動収集の静的データ。公開情報(公式サイト・レポート記事)を
# 元にしているが、一次資料での全項目の裏取りまではしていない旨を "verified" で明示する。
PARTICIPANTS = [
    {
        "key": "techsport_racing",
        "name": "TechSport Racing",
        "description": {
            "ja": "米ノースカロライナ州拠点のレーシングチーム。公開情報によれば2014年設立の家族経営チームで、"
            "2023年シーズンのGR Cup(旧TGR North America GR Cup)初代チャンピオンチームとされる。",
            "en": "A North Carolina-based racing team. Publicly available sources describe it as a family-run "
            "operation founded in 2014, and reportedly the inaugural GR Cup (formerly TGR North America GR Cup) "
            "championship-winning team in the 2023 season.",
        },
        "verified": "web_search_only",
        "official_url": f"{BASE_URL}/team/57/techsport-racing",
    },
    {
        "key": "copeland_motorsports",
        "name": "Copeland Motorsports",
        "description": {
            "ja": "公開情報によれば2023・2024年と2年連続でGR Cupのチームタイトルを獲得したとされる有力チーム。",
            "en": "A leading team publicly reported to have won back-to-back GR Cup team championships in the "
            "2023 and 2024 seasons.",
        },
        "verified": "web_search_only",
        "official_url": f"{BASE_URL}/team/52/copeland-motorsports",
    },
    {
        "key": "rva_graphics_speed_syndicate",
        "name": "RVA Graphics Motorsports by Speed Syndicate",
        "description": {
            "ja": "Speed Syndicateが運営母体となるチーム。2026年シーズン序盤よりGR Cup AMクラス上位を争っている。",
            "en": "A team operated under the Speed Syndicate organization, running near the front of the GR Cup "
            "AM class through the early part of the 2026 season.",
        },
        "verified": "standings_only",
        "official_url": None,
    },
    {
        "key": "bsi_racing",
        "name": "BSI Racing",
        "description": {
            "ja": "GR Cup AMクラスに参戦するチーム。詳細な運営母体情報は未確認。",
            "en": "A team competing in the GR Cup AM class. Detailed background on the operating organization is unconfirmed.",
        },
        "verified": "standings_only",
        "official_url": None,
    },
]


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def _latest_completed_weekends(today: date | None = None) -> list[dict]:
    today = today or date.today()
    return [w for w in ROUND_WEEKENDS if today >= w["end_date"]]


def fetch_round_entry_list(slug: str) -> list[dict]:
    """1週末分のエントリーリストHTMLから [{car_no, driver, team, car, class}, ...] を返す。"""
    session = _session()
    try:
        resp = session.get(ENTRY_LIST_URL.format(slug=slug), timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding or "utf-8"
        html_text = resp.text

        table_m = re.search(r"<table[^>]*>.*?</table>", html_text, re.S)
        if not table_m:
            return []
        rows = re.findall(r"<tr[^>]*>(.*?)</tr>", table_m.group(0), re.S)
        entries: list[dict] = []
        for row in rows[1:]:
            cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)
            cells = [re.sub(r"<[^>]+>", " ", c) for c in cells]
            cells = [re.sub(r"\s+", " ", c).strip() for c in cells]
            if len(cells) < 5:
                continue
            car_no, driver, team, car, grade = cells[0], cells[1], cells[2], cells[3], cells[4]
            if not driver or not team:
                continue
            entries.append({"car_no": car_no, "driver": driver, "team": team, "car": car, "class": grade})
        return entries
    except Exception:  # noqa: BLE001
        return []


def fetch_season_roster() -> dict[str, dict]:
    """開幕から直近の開催済み週末までの全エントリーリストを集計し、
    team名 -> {drivers: [...], car_numbers: [...]} を返す(名寄せはしない)。
    """
    completed = _latest_completed_weekends()
    roster: dict[str, dict] = {}
    for weekend in completed:
        for entry in fetch_round_entry_list(weekend["slug"]):
            bucket = roster.setdefault(entry["team"], {"drivers": {}, "car_numbers": set(), "class": entry["class"]})
            bucket["drivers"][entry["driver"]] = {"name": entry["driver"], "car_no": entry["car_no"], "class": entry["class"]}
            bucket["car_numbers"].add(entry["car_no"])
    return {
        team: {
            "drivers": list(info["drivers"].values()),
            "car_numbers": sorted(info["car_numbers"]),
            "class": info["class"],
        }
        for team, info in roster.items()
    }


def fetch() -> dict:
    standings = fetch_gr_cup_team_standings(limit=20)
    roster = fetch_season_roster()
    completed = _latest_completed_weekends()

    team_rows: list[dict] = []
    standings_by_name = {row["name"]: row for row in standings["standings"]}

    # 静的な背景情報を持つチーム + 順位表・エントリーリストにのみ登場するその他全チームを統合する。
    known_keys = {p["name"] for p in PARTICIPANTS}
    all_team_names = set(standings_by_name.keys()) | set(roster.keys())

    for participant in PARTICIPANTS:
        name = participant["name"]
        entry = dict(participant)
        st = standings_by_name.get(name)
        entry["position"] = st["position"] if st else None
        entry["points"] = st["points"] if st else None
        entry["drivers"] = roster.get(name, {}).get("drivers", [])
        entry["car_numbers"] = roster.get(name, {}).get("car_numbers", [])
        team_rows.append(entry)

    for name in sorted(all_team_names - known_keys):
        st = standings_by_name.get(name)
        team_rows.append(
            {
                "key": re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_"),
                "name": name,
                "description": {
                    "ja": "背景情報は未収集です(公式順位表/エントリーリストにのみ登場)。",
                    "en": "No hand-researched background collected yet (appears only in the official standings/entry list).",
                },
                "verified": "standings_only",
                "official_url": None,
                "position": st["position"] if st else None,
                "points": st["points"] if st else None,
                "drivers": roster.get(name, {}).get("drivers", []),
                "car_numbers": roster.get(name, {}).get("car_numbers", []),
            }
        )

    team_rows.sort(key=lambda r: (r["position"] is None, r["position"] or 999))

    return {
        "teams": team_rows,
        "rounds_completed": len(completed),
        "rounds_total": len(ROUND_WEEKENDS),
        "standings_error": standings["error"],
        "note": (
            "チーム背景は公開情報を元にした手動調査です(一次資料での全項目裏取りは未実施の"
            "ものを含みます)。順位/ポイント・エントリーリストは公式サイト(grcupseries.com)の"
            "実データです。ラウンドをまたいだ同一人物と思われる表記ゆれは統合せず、公式データの"
            "まま表示しています。"
        ),
    }
