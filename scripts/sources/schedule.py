"""GR86が参戦するモータースポーツの年間レース日程を取得する。

Toyota GR Cup(北米, grcupseries.com)は、"GR Corolla Watch"で確認済みのTC America
(tcamerica.us)と全く同じCMSプラットフォームを使っている(2026年8月に実際のHTMLで確認: 同じ
`calendar__date-number`/`calendar__race-header`/`past-events__list-item`/`piped-list-span`
マークアップ)。SKILL.mdの「姉妹サイトの共通CMSを見つけたら使い回す」の教訓どおり、
TC Americaで実証済みの解析ロジックをBASE_URLだけ差し替えて再利用している。

日本(TGR GR86/BRZ Cup)は、2026年8月の再調査でスケジュールの静的HTMLページが見つかった
(`https://toyotagazooracing.com/jp/86brz/calendar/{year}/` — `<li class="cal-list__item">`
の一覧表、ラウンド番号・大会名・開催日・サーキット名を含む)。実HTMLで確認済みのため
fetch_tgr_86brz_cup_schedule()で実データ化している。一方、順位表(ranking)ページは
PDFへのリンクのみでHTML表が存在しない(`https://toyotagazooracing.com/jp/86brz/ranking/{year}/`)
ため、SKILL.mdが警告するPDFの文字化けリスクを避け、順位はスクレイピングせずリンクのみ
提供する。

オーストラリア(GR Cup Australia)は、公式サイト(toyota.com.au)が403を返しスクレイピング
不可。サードパーティのsupercars.com(GR Cupが併催するSupercars選手権の公式サイト)には
セッション単位の実結果ページ(`/results/{year}/{event-slug}/{session-code}`)が存在するが、
シーズン通算のポイントランキング表はどこにも見当たらず、セッションコードもイベントごとに
個別調査が必要で安定した命名規則が確認できなかった。誤ったURL推測によるデータ欠落リスクが
高いため、今回はスクレイピングを見送り公式ページ/検索リンクのみを提供する。
"""

from __future__ import annotations

import html as html_module
import re
from datetime import date

import requests

from .common import REQUEST_TIMEOUT, USER_AGENT

GR_CUP_BASE_URL = "https://www.grcupseries.com"
GR_CUP_CALENDAR_URL = f"{GR_CUP_BASE_URL}/calendar"

JP_86BRZ_CUP_BASE_URL = "https://toyotagazooracing.com"
JP_86BRZ_CUP_URL = "https://toyotagazooracing.com/jp/86brz/about/"
JP_86BRZ_CUP_CALENDAR_URL_TMPL = JP_86BRZ_CUP_BASE_URL + "/jp/86brz/calendar/{year}/"
JP_86BRZ_CUP_RANKING_URL_TMPL = JP_86BRZ_CUP_BASE_URL + "/jp/86brz/ranking/{year}/"

GR_CUP_AUSTRALIA_URL = "https://www.toyota.com.au/gazoo-racing/gr-cup/races"
MX5_CUP_SCHEDULE_URL = "https://www.mx-5cup.com/schedule"

_MONTH_NUM = {
    "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
    "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12,
}

_JP_DATE_RE = re.compile(r"(\d{1,2})月(\d{1,2})日")


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def _month_num(text: str) -> int:
    return _MONTH_NUM.get(text.strip()[:3].upper(), 0)


def _status(sort_key: int) -> str:
    today_key = date.today().year * 10000 + date.today().month * 100 + date.today().day
    return "upcoming" if sort_key >= today_key else "completed"


def _fetch_calendar_platform_schedule(calendar_url: str) -> list[dict]:
    """grcupseries.com/tcamerica.us系CMSの公式カレンダー(開催予定+開催済み)を取得する。"""
    session = _session()
    events: list[dict] = []
    try:
        resp = session.get(calendar_url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        html_text = resp.text

        date_block_re = re.compile(
            r'"calendar__date-number">(\d+)</span>\s*'
            r'<span class="calendar__date-month">([A-Z]+)</span>\s*'
            r'<span class="calendar__date-year">(\d+)</span>',
            re.S,
        )

        # 「開催間近/開催中」の1件だけ class="calendar__list-item full-width" のように
        # 追加クラスが付くことがあるため、単純な文字列split(閉じ引用符まで含む完全一致)ではなく
        # 正規表現でクラス名の前方一致のみで区切る。
        for chunk in re.split(r'<li class="calendar__list-item[^"]*">', html_text)[1:]:
            chunk = chunk[:3000]
            dates = date_block_re.findall(chunk)
            track_m = re.search(r'calendar__race-header">([^<]*)</h3', chunk)
            round_m = re.search(r'calendar__race-text">([^<]*)</span', chunk)
            if not dates or not track_m:
                continue
            s_day, s_month, s_year = dates[0]
            sort_key = int(s_year) * 10000 + _month_num(s_month) * 100 + int(s_day)
            if len(dates) >= 2:
                e_day, e_month, e_year = dates[1]
                date_range = (
                    f"{s_month} {s_day}–{e_day}, {e_year}"
                    if s_month == e_month
                    else f"{s_month} {s_day}–{e_month} {e_day}, {e_year}"
                )
            else:
                date_range = f"{s_month} {s_day}, {s_year}"
            events.append(
                {
                    "round": html_module.unescape(round_m.group(1).strip() if round_m else ""),
                    "track": html_module.unescape(track_m.group(1).strip()),
                    "date_range": date_range,
                    "status": "upcoming",
                    "sort_key": sort_key,
                }
            )

        full_month_re = re.compile(r"(\d{1,2})\s*-\s*(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})")
        single_day_re = re.compile(r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})")

        for chunk in html_text.split('past-events__list-item">')[1:]:
            chunk = chunk[:2000]
            spans = re.findall(r'piped-list-span">(.*?)</span>', chunk, re.S)
            spans = [re.sub(r"<[^>]+>", " ", s).strip() for s in spans]
            if len(spans) < 3:
                continue
            date_text, track_country, round_text = spans[0], spans[1], spans[2]
            m = full_month_re.search(date_text)
            if m:
                s_day, _e_day, month_name, year = m.groups()
            else:
                m = single_day_re.search(date_text)
                if not m:
                    continue
                s_day, month_name, year = m.groups()
            sort_key = int(year) * 10000 + _month_num(month_name) * 100 + int(s_day)
            events.append(
                {
                    "round": html_module.unescape(round_text),
                    "track": html_module.unescape(re.sub(r"\s+", " ", track_country).strip()),
                    "date_range": date_text,
                    "status": "completed",
                    "sort_key": sort_key,
                }
            )
    except Exception:  # noqa: BLE001
        return []

    events.sort(key=lambda e: e["sort_key"])
    return events


def fetch_gr_cup_schedule() -> list[dict]:
    return _fetch_calendar_platform_schedule(GR_CUP_CALENDAR_URL)


def fetch_tgr_86brz_cup_schedule(year: int | None = None) -> list[dict]:
    """TGR GR86/BRZ Cup(日本)公式カレンダーページ(静的HTML)から年間日程を取得する。

    2026年8月にHTMLを実際に確認した際のマークアップ: `<li class="cal-list__item">` の
    リスト内に、ラウンド番号(`cal-list__item__cell__01__rank`)・大会名
    (`cal-list__item__title`)・開催日(`cal-list__item__data__dt`、和暦日付表記のみで
    年は含まれない)・サーキット名(「開催サーキット」の直後の`<span>`)が入っている。
    """
    year = year or date.today().year
    session = _session()
    events: list[dict] = []
    try:
        resp = session.get(JP_86BRZ_CUP_CALENDAR_URL_TMPL.format(year=year), timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding or "utf-8"
        html_text = resp.text

        items = re.findall(r'<li class="cal-list__item">(.*?)</li>', html_text, re.S)
        for item in items:
            rank_m = re.search(r'cal-list__item__cell__01__rank">([^<]*)<', item)
            title_m = re.search(r'cal-list__item__title">([^<]*)<', item)
            dt_m = re.search(r'cal-list__item__data__dt">([^<]*)<', item)
            circuit_m = re.search(r"開催サーキット\s*<span>([^<]*)</span>", item)
            if not (rank_m and dt_m):
                continue

            date_text = html_module.unescape(dt_m.group(1).strip())
            dates = _JP_DATE_RE.findall(date_text)
            if not dates:
                continue
            start_month, start_day = int(dates[0][0]), int(dates[0][1])
            sort_key = year * 10000 + start_month * 100 + start_day

            try:
                round_no = int(rank_m.group(1))
            except ValueError:
                round_no = None

            events.append(
                {
                    "round": f"Round {round_no}" if round_no is not None else "",
                    "name": html_module.unescape(title_m.group(1).strip()) if title_m else "",
                    "track": html_module.unescape(circuit_m.group(1).strip()) if circuit_m else "",
                    "date_range": date_text,
                    "status": "upcoming",
                    "sort_key": sort_key,
                }
            )
    except Exception:  # noqa: BLE001
        return []

    events.sort(key=lambda e: e["sort_key"])
    return events


def _finalize(events: list[dict]) -> list[dict]:
    for e in events:
        e["status"] = _status(e["sort_key"])
        del e["sort_key"]
    return events


def fetch_all() -> dict:
    return {
        "gr_cup": _finalize(fetch_gr_cup_schedule()),
        "tgr_86brz_cup": _finalize(fetch_tgr_86brz_cup_schedule()),
        "gr_cup_australia": {"link": GR_CUP_AUSTRALIA_URL},
        "mx5_cup": {"link": MX5_CUP_SCHEDULE_URL},
    }
