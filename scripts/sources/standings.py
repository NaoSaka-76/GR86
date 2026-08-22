"""モータースポーツのシリーズランキング(実データ)を取得する。

Toyota GR Cup公式サイト(grcupseries.com)は、"GR Corolla Watch"で確認済みのTC America
(tcamerica.us)と同一のCMSプラットフォームを使っている(2026年8月に実HTMLで確認: 同一の
`<select name="filter_season_id">`/`<select name="filter_standing_type">`、同一の
`<table class="table standing">` マークアップ)。TC Americaで実証済みの解析ロジックを
そのまま再利用し、URL/対象クラスラベルのみ差し替えている。

現在の値(2026年8月時点で実サイトから確認済み):
  - filter_season_id: "4" が season label "2026" に対応
  - filter_standing_type: "0_5_teams" = "GR Cup AM Teams", "0_5_drivers" = "GR Cup AM Drivers"
    ("GR Cup Legends Drivers" というクラスも別途存在するが、GR86 Cup Editionのメインクラスは
    AM。値は年ごとに変わりうるため、ハードコードせずページ自身の<select>から都度解決する)。
"""

from __future__ import annotations

import html as html_module
import re
from datetime import datetime, timezone, timedelta

import requests

from .common import REQUEST_TIMEOUT, USER_AGENT

BASE_URL = "https://www.grcupseries.com"
STANDINGS_URL = f"{BASE_URL}/standings"
TARGET_TEAMS_LABEL = "GR Cup AM Teams"
TARGET_DRIVERS_LABEL = "GR Cup AM Drivers"
JST = timezone(timedelta(hours=9))


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def _extract_select_options(html_text: str, select_name: str) -> list[tuple[str, str]]:
    block = re.search(rf'<select[^>]*name="{select_name}"[^>]*>(.*?)</select>', html_text, re.S)
    if not block:
        return []
    options = re.findall(r'<option[^>]*\bvalue="([^"]*)"[^>]*>([^<]*)</option>', block.group(1))
    return [(value, html_module.unescape(label.strip())) for value, label in options]


def _current_season_id(html_text: str, year: int) -> str | None:
    for value, label in _extract_select_options(html_text, "filter_season_id"):
        if str(year) in label:
            return value
    return None


def _standing_type_id(html_text: str, target_label: str) -> str | None:
    for value, label in _extract_select_options(html_text, "filter_standing_type"):
        if label.strip() == target_label:
            return value
    return None


def _parse_standings_table(html_text: str) -> list[dict]:
    table = re.search(r'<table class="table standing".*?</table>', html_text, re.S)
    if not table:
        return []
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", table.group(0), re.S)
    results: list[dict] = []
    for row in rows[1:]:
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)
        cells = [re.sub(r"<[^>]+>", "", c).strip() for c in cells]
        if len(cells) < 3 or not cells[0].isdigit():
            continue
        points_raw = re.sub(r"[^\d]", "", cells[2]) or "0"
        results.append({"position": int(cells[0]), "name": cells[1], "points": int(points_raw)})
    return results


def _fetch_gr_cup_standings(target_label: str, limit: int) -> dict:
    session = _session()
    try:
        base_resp = session.get(STANDINGS_URL, timeout=REQUEST_TIMEOUT)
        base_resp.raise_for_status()
        base_html = base_resp.text

        season_id = _current_season_id(base_html, datetime.now(JST).year)
        standing_type_id = _standing_type_id(base_html, target_label)
        if not season_id or not standing_type_id:
            return {"standings": [], "error": "対象シーズン/クラスを公式サイト上で特定できませんでした"}

        resp = session.get(
            STANDINGS_URL,
            params={"filter_standing_type": standing_type_id, "filter_season_id": season_id},
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        rows = _parse_standings_table(resp.text)[:limit]

        return {
            "standings": rows,
            "error": None if rows else "現在、順位データが空です(シーズン開幕前などの可能性があります)",
        }
    except Exception as exc:  # noqa: BLE001
        return {"standings": [], "error": f"取得エラー: {exc}"}


def fetch_gr_cup_team_standings(limit: int = 15) -> dict:
    """Toyota GR Cup「GR Cup AM」クラス チームズランキング(公式サイト実データ)。"""
    return _fetch_gr_cup_standings(TARGET_TEAMS_LABEL, limit)


def fetch_gr_cup_driver_standings(limit: int = 15) -> dict:
    """Toyota GR Cup「GR Cup AM」クラス ドライバーズランキング(公式サイト実データ)。"""
    return _fetch_gr_cup_standings(TARGET_DRIVERS_LABEL, limit)
