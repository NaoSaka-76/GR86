"""JAF(日本自動車連盟)公式サイトが運営する全日本選手権(ラリー/ジムカーナ/ダートトライアル)の
年間日程・クラス別ランキングを取得する。

## 2026年8月の実データ確認結果

motorsports.jaf.or.jp は3競技(ラリー/ジムカーナ/ダートトライアル)とも同一のCMS基盤で
運営されており、以下の共通構造を実HTMLで確認済み:

- カレンダーページ(`/calendar/{year}/{discipline_path}`)は `scheduleCard` という単位で
  各ラウンドが並ぶ静的HTML(開催日・大会名・開催地を含む)。
- 現在シーズンのクラス別ランキングページ(`/results/standings/{discipline_path}?class={id}`)
  は `table-point` というクラスの静的HTML表(順位・ドライバー名・ラウンドごとの得点・合計得点)。
  ページ内には対象クラスを切り替えるリンク一覧(`?class=class1`, `class2`, ...)があり、
  クラス名とIDの対応はJAFサイト自身の`l-localNavigation`ブロックから確認する(ハードコードすると
  クラス区分の変更で対応がずれるリスクがあるため、本モジュールでは事前に実HTMLで確認した
  IDを定数として持つが、値自体はコメントで出典を明記している)。

## GR86が実際に参戦しているクラス(2026年8月、実データ・報道で確認済み)

- **全日本ラリー選手権**: JN-4クラス(2026年シーズンより、2025年までのJN-3クラスが再編・
  改称されたもの。1500〜2500cc・FF/FR混走)。クラスIDは `class4`
  (JAFサイトの表記は「クラス4」で、JRCA側のJN-4呼称と対応)。2026年第1戦(ラリー三河湾)で
  GR86が優勝、BRZも表彰台に入ったことをWeb CARTOP等の報道で確認。
- **全日本ジムカーナ選手権**: PN4クラス(2026年シーズンよりクラス区分が9→11クラスに再編され、
  旧PN3クラスがPN4/PN5に分離。PN4は2000cc以上・FIA/JAF公認2010年以降のFF/FR車両)。
  クラスIDは `class7`。2026年第1戦(GYMKHANA IN TSUKUBA)でGR86ドライバーの野島俊哉選手が
  優勝したことをJAF公式トピックス記事で確認。
- **全日本ダートトライアル選手権**: PN3クラス(2WD・FR・1600cc超)。JDCEA公式のクラス区分
  ガイドが例示車種として「トヨタGR86」を明記。クラスIDは `class5`。2026年第1戦の実結果
  (mos.dunlop.co.jp掲載)でPN3クラス出走18台中約11台がGR86/86バッジ車両であることを確認。

いずれのクラスも、JAF公式の順位表にはドライバー名と得点のみが掲載され、使用車種(車両モデル)の
列がないため、本モジュールの順位表自体からはGR86車両を個別特定できない(車種別のハイライトは
行わない。上記の参戦クラス自体がGR86が確認されているクラスであることを根拠としている)。
"""

from __future__ import annotations

import html as html_module
import re
from datetime import date

import requests

from .common import REQUEST_TIMEOUT, USER_AGENT

JAF_BASE_URL = "https://motorsports.jaf.or.jp"

# 2026年8月に実HTML(l-localNavigationのクラス切替リンク)で確認したクラスID。
RALLY_JN4_CLASS_ID = "class4"          # JAF表記「クラス4」= JN-4(2025年までのJN-3が再編・改称)
GYMKHANA_PN4_CLASS_ID = "class7"       # JAF表記「PN4」(2026年よりクラス区分再編、旧PN3相当)
DIRTTRIAL_PN3_CLASS_ID = "class5"      # JAF表記「PN3」


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def _status(sort_key: int) -> str:
    today_key = date.today().year * 10000 + date.today().month * 100 + date.today().day
    return "upcoming" if sort_key >= today_key else "completed"


def fetch_calendar(discipline_path: str, year: int | None = None) -> list[dict]:
    """JAF公式カレンダーページ(静的HTML)から年間日程を取得する。

    discipline_path例: "gymkhana/jgc", "rally/jrc", "dirt-trial/jdc"
    """
    year = year or date.today().year
    session = _session()
    events: list[dict] = []
    try:
        resp = session.get(f"{JAF_BASE_URL}/calendar/{year}/{discipline_path}", timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding or "utf-8"
        html_text = resp.text

        blocks = html_text.split('<div class="scheduleCard">')[1:]
        for block in blocks:
            chunk = block[:4000]
            year_m = re.search(r'_year">(\d+)年', chunk)
            start_m = re.search(
                r'_start">\s*<span class="_num">(\d+)</span>\s*<span>月</span>\s*<span class="_num">(\d+)</span>',
                chunk,
            )
            title_m = re.search(r'scheduleCard-titleText">(.*?)</p>', chunk, re.S)
            venue_m = re.search(r'scheduleCard-detailList-content">([^<]*)</div>', chunk)
            if not (year_m and start_m and title_m):
                continue

            y = int(year_m.group(1))
            month, day = int(start_m.group(1)), int(start_m.group(2))
            sort_key = y * 10000 + month * 100 + day

            title = re.sub(r"<[^>]+>", " ", title_m.group(1)).strip()
            title = html_module.unescape(re.sub(r"\s+", " ", title))
            round_m = re.search(r"第(\d+)戦", title)

            events.append(
                {
                    "round": f"第{round_m.group(1)}戦" if round_m else "",
                    "name": title,
                    "track": html_module.unescape(venue_m.group(1).strip()) if venue_m else "",
                    "date_range": f"{month}/{day}",
                    "status": "upcoming",
                    "sort_key": sort_key,
                }
            )
    except Exception:  # noqa: BLE001
        return []

    events.sort(key=lambda e: e["sort_key"])
    return events


def finalize_calendar(events: list[dict]) -> list[dict]:
    for e in events:
        e["status"] = _status(e["sort_key"])
        del e["sort_key"]
    return events


def fetch_class_standings(discipline_path: str, class_id: str, limit: int = 20) -> dict:
    """JAF公式サイトの、指定クラスの現在シーズン ドライバーズランキングを取得する。

    discipline_path例: "gymkhana/2026/jgc", "rally/2026/jrc", "dirt-trial/2026/jdc"
    (年度を含むパス。standings用のURLはcalendar用と異なり年度がパスに入る)
    """
    session = _session()
    try:
        resp = session.get(
            f"{JAF_BASE_URL}/results/standings/{discipline_path}",
            params={"class": class_id},
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding or "utf-8"
        html_text = resp.text

        table_m = re.search(r'<table class="table-point.*?</table>', html_text, re.S)
        if not table_m:
            return {"standings": [], "error": "順位表が見つかりませんでした"}
        tbody_m = re.search(r"<tbody>(.*?)</tbody>", table_m.group(0), re.S)
        if not tbody_m:
            return {"standings": [], "error": "順位表本体が見つかりませんでした"}

        rows = re.findall(r"<tr>(.*?)</tr>", tbody_m.group(0), re.S)
        results: list[dict] = []
        for row in rows:
            cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)
            cells = [html_module.unescape(re.sub(r"<[^>]+>", "", c).strip()) for c in cells]
            if len(cells) < 3 or not cells[0].isdigit():
                continue
            points_raw = re.sub(r"[^\d.]", "", cells[-1]) or "0"
            results.append({"position": int(cells[0]), "name": cells[1], "points": float(points_raw)})

        rows_limited = results[:limit]
        return {
            "standings": rows_limited,
            "error": None if rows_limited else "現在、順位データが空です(シーズン開幕前などの可能性があります)",
        }
    except Exception as exc:  # noqa: BLE001
        return {"standings": [], "error": f"取得エラー: {exc}"}
