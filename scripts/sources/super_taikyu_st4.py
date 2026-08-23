"""スーパー耐久 ST-4クラスの全参戦チーム一覧を取得する(GR86/BRZ/ロードスターをハイライト)。

姉妹プロジェクト"Supra GT4 Watch"の `st_supra_teams.py`(ST-Zクラス、対象車両のみ抽出)と
同じ技術基盤(supertaikyu.com の実データスクレイピング)を使うが、本モジュールはスコープが
逆で、ST-4クラスの**全チーム**を列挙したうえで、その中からGR86/BRZ/ロードスター(MX-5)の
エントリーだけを視覚的にハイライトする(車種カタログの「全10メーカー中Supra GT4のみ
ハイライト」と同じ技法を、参戦車両一覧に適用したもの)。

## 2026年8月の実データ確認結果

- 順位表ページ(race/standing.html)ではクラスごとに `<li class="mix stN">` という連番の
  ラッパーが振られているが、Nの並び順とクラス名(ST-1〜ST-5, ST-Q, ST-TCR, ST-USA, ST-X,
  ST-Z)は一致しない(実際にHTMLを確認したところ ST-4 は `mix st8`)。ハードコードすると
  シーズンをまたいで振り直された際に静かに別クラスを拾ってしまうため、各ブロック内の
  `Standing_Class` 見出しテキストが実際に"ST-4"と一致するブロックを毎回探索して使う。
- 各ラウンドのエントリーリストページ(race/round_XX.html)では `Standing_Class"> ST-4` が
  そのままテキストとして埋め込まれており、順位表ページのような対応表なしで直接検索できる。
- ST-4クラスの参戦車両は2026年8月時点で10チーム。トヨタGR86が7台、マツダ ロードスター
  (現行ND型、RFボディの1台のみ)が1台、旧型ロードスター(NC型、明示的に車名に"NC"と
  記載)が1台、スズキ スイフトスポーツが1台。**スバルBRZの参戦は確認できなかった**
  (2026年8月時点)。
- ジェントルマンドライバー登録義務のレギュレーションは公式サイト・モータースポーツ規則
  解説サイトで確認した限りST-X/ST-Z/ST-TCRクラスのみに適用され、ST-4クラスには同様の
  規定が見当たらなかったため、ST-Zクラス(`st_supra_teams.py`)のようなプロ/アマ推定は
  行わない(規定がない車種にレギュレーション由来の区分を創作しない)。
- ドライバー欄の列数(スロット数)はラウンドによって4列(A〜D)または6列(A〜F)と変動する
  ことを実データで確認済み(第3戦・富士は6列)。空きスロットは"TBN"または"&nbsp;"で
  表記される。
- 全ラウンドでST-4クラスが開催されるとは限らない(2026年8月確認時点で第5戦オートポリスは
  ST-4クラスの開催がなく、順位表側でもR5列が空欄だった)。該当ラウンドにクラスブロックが
  見つからない場合は空辞書を返して静かにスキップする設計にしている(誤って別クラスを
  拾わないようにするため)。

## 2026年9月追加: チーム背景・写真(全10チーム)

チーム運営母体/オーナーの背景情報は、Web検索による手動調査の静的データとして TEAM_BACKGROUND
定数に保持する(公式サイトに構造化データがないため、GR Cup北米・Supra GT4 ST-Zチームカードと
同じパターン)。一次資料での裏取りができていない項目は `"verified": "web_search_only"` と
明示する。

写真はSKILL.mdの「Sourcing many photos safely: Wikimedia Commons」に従い、Wikimedia Commons
APIで許諾ライセンス(CC BY-*/CC0)の画像のみを使用し、artist/license/descriptionurlを
すべて記録して表示側でクレジット表記する。2026年9月の調査時点で10チーム中5チーム
(SHADE RACING・OVER DRIVE・TEAM NOPRO・チーム ジーモーション・浅野レーシングサービス)で
許諾ライセンス画像を確認できた。写真はいずれも撮影者「Tokumeigakarinoaoshima」による
2022年または2025年のスーパー耐久大会後撮影で、車番は現行シーズンと一致することを確認済み
(チーム ジーモーションのみ、写真のチーム名義が現行と異なる旧称「Zenyaku Kogyo with TEAM
G MOTION」だが車番60で一致)。残り5チーム(ENDLESS SPORTS・TRACY SPORTS・HMR Racing・
木附製作所モータースポーツ事業部・AutoLabo)は許諾ライセンス画像が見つからずプレースホルダー
表示とする。
"""

from __future__ import annotations

import re
from datetime import date

import requests

from .common import REQUEST_TIMEOUT, USER_AGENT

STANDINGS_URL = "https://supertaikyu.com/race/standing.html"
ROUND_ENTRY_LIST_URL = "https://supertaikyu.com/race/round_{num:02d}.html"
CLASS_LABEL = "ST-4"

# 2026年シーズンの各ラウンド最終日(schedule.pyのSuper Taikyu日程取得と同一の実データに基づく)。
ROUND_END_DATES = [
    (1, date(2026, 3, 22)),
    (2, date(2026, 4, 19)),
    (3, date(2026, 6, 7)),
    (4, date(2026, 7, 5)),
    (5, date(2026, 7, 26)),
    (6, date(2026, 10, 25)),
    (7, date(2026, 11, 15)),
]

_SLOT_LABELS = ["A", "B", "C", "D", "E", "F"]
_TBN_MARKERS = ("tbn", "※", "&nbsp;", "")

# チーム名(順位表・エントリーリストの表記と一致させるキー)ごとの手動収集背景データ。
# "verified": "official" は一次資料(公式サイト等)で確認済み、"web_search_only" は
# 複数の報道・ブログ等の検索結果を突き合わせたが一次資料での裏取りは未実施であることを示す。
TEAM_BACKGROUND = {
    "ENDLESS SPORTS": {
        "description": {
            "ja": "ブレーキ・サスペンションメーカー「エンドレス」直系のワークス系チーム。"
            "2024年ST-4シリーズチャンピオン(134点、2勝、全6戦表彰台)。前身の車両(GR YARIS等)"
            "では2016年にも王座獲得歴がある。",
            "en": "A works-affiliated team backed directly by Endless, the brake and suspension "
            "manufacturer. Won the 2024 ST-4 series championship (134 points, 2 wins, podium in "
            "all 6 rounds). An earlier-generation Endless entry also won a title back in 2016.",
        },
        "verified": "web_search_only",
    },
    "TRACY SPORTS": {
        "description": {
            "ja": "TRACY SPORTSが技術面を担当し、HC GALLERYがタイトルスポンサーを務める2026年"
            "新規参戦チーム。監督は山本智広氏(TRACY SPORTS)。2026年の富士24時間レースで"
            "ST-4クラス優勝。",
            "en": "A new entrant for 2026, with TRACY SPORTS handling the technical/engineering "
            "side and HC GALLERY as title sponsor. Team principal Tomohiro Yamamoto (TRACY "
            "SPORTS). Won the ST-4 class at the 2026 Fuji 24 Hours.",
        },
        "verified": "web_search_only",
    },
    "SHADE RACING": {
        "description": {
            "ja": "自動車内装部品メーカー「林テレンプ株式会社」を母体とするチーム。2018年に"
            "86/BRZでスーパー耐久参戦を開始し、2022年からはSUPER GTにも参戦。富士スピードウェイ"
            "13コーナー外側に自社ファクトリーを構える。",
            "en": "Backed by Hayashi Telempu Corporation, an automotive interior parts maker. "
            "Started racing an 86/BRZ in Super Taikyu in 2018, and has also competed in Super GT "
            "since 2022. Operates its own factory just outside Turn 13 at Fuji Speedway.",
        },
        "verified": "web_search_only",
    },
    "OVER DRIVE": {
        "description": {
            "ja": "大阪府八尾市のマツダ専門チューニングショップ「odula」を母体とするチーム。"
            "代表は武地隆行氏。2021年にST-5クラスで王座獲得、2024年11月にST-4クラス初優勝。",
            "en": "Backed by odula, a Mazda-specialist tuning shop in Yao, Osaka. Led by "
            "representative Takayuki Takechi. Won the ST-5 class title in 2021, and took its "
            "first ST-4 class win in November 2024.",
        },
        "verified": "web_search_only",
    },
    "TEAM NOPRO": {
        "description": {
            "ja": "神奈川県葉山町のロードスター専門店「野上プロジェクト」代表・野上敏彦氏が率いる"
            "チーム。2024年はMAZDA2でST-5クラス王座を獲得。旧型(NC型)ロードスターでGR86勢と"
            "互角に渡り合っている。",
            "en": "Led by Toshihiko Nogami, representative of Nogami Project, a Mazda Roadster "
            "specialist shop in Hayama, Kanagawa. Won the ST-5 class title in 2024 with a Mazda2. "
            "Runs an older-generation (NC-chassis) Roadster that has been competitive against the "
            "class's GR86 entries.",
        },
        "verified": "web_search_only",
    },
    "HMR Racing": {
        "description": {
            "ja": "東京都西多摩郡の中古スポーツカー専門販売店「HMR」が運営するチーム。自社整備士の"
            "育成を目的にマシンを自社製作しており、製作過程を自社ブログで詳しく公開している。",
            "en": "Run by HMR, a used sports car dealership in Nishitama, Tokyo. Built the race car "
            "in-house partly as a training exercise for its own mechanics, and has documented the "
            "build process in detail on its own blog.",
        },
        "verified": "web_search_only",
    },
    "木附製作所モータースポーツ事業部": {
        "description": {
            "ja": "神奈川県綾瀬市の精密板金加工会社「木附製作所」(半導体製造装置・紙幣読取機・"
            "郵便区分機・医療機器向け部品等を製造)のモータースポーツ事業部。代表取締役・梅原洋一氏"
            "とその息子でチーム代表兼監督兼ドライバーの梅原拓臣氏が運営。燃料タンク等を自社の"
            "精密板金技術で内製している。",
            "en": "The motorsports division of Kizuke Seisakusho, a precision sheet-metal "
            "fabricator in Ayase, Kanagawa (makes parts for semiconductor equipment, banknote "
            "counters, postal sorting machines, and medical devices). Run by company president "
            "Yoichi Umehara and his son Takuomi Umehara, who serves as team principal, manager, "
            "and driver. The team builds parts like the fuel tank in-house using the company's "
            "own sheet-metal expertise.",
        },
        "verified": "web_search_only",
    },
    "チーム ジーモーション": {
        "description": {
            "ja": "医薬品メーカー「全薬工業(全薬グループ)」がスポンサーを務めるチーム。2023年"
            "シリーズ2位・富士24時間優勝歴があり、2026年シーズンはST-4クラス王座を目標に掲げている。",
            "en": "Sponsored by Zenyaku Kogyo (the Zenyaku Group), a pharmaceutical company. "
            "Finished 2nd in the 2023 series and won the Fuji 24 Hours that year; targeting the "
            "ST-4 class championship for 2026.",
        },
        "verified": "web_search_only",
    },
    "浅野レーシングサービス": {
        "description": {
            "ja": "茨城県桜川市の老舗チーム。代表の浅野武夫氏(73歳)は1975年からドライバー活動を"
            "続けており、スーパー耐久創設初年度から参戦している。2026年シーズンが同氏にとって"
            "最後のシーズンになる予定と報じられている。",
            "en": "A long-running team based in Sakuragawa, Ibaraki. Representative Takeo Asano "
            "(73) has been racing since 1975 and has competed since Super Taikyu's inaugural "
            "season. Reportedly set to make 2026 his final season.",
        },
        "verified": "web_search_only",
    },
    "AutoLabo": {
        "description": {
            "ja": "スズキ・スイフトスポーツ(ZC33S)で参戦する、スーパー耐久史上初のスズキ車。"
            "ST-4クラス唯一のFF・ターボ車で、信頼性重視の開発方針を掲げている。",
            "en": "Fields a Suzuki Swift Sport (ZC33S) — the first Suzuki entry in Super Taikyu "
            "history. The only FWD/turbo car in the ST-4 class, developed with an emphasis on "
            "reliability.",
        },
        "verified": "web_search_only",
    },
}

# Wikimedia Commonsで許諾ライセンス(CC BY-*/CC0)の写真が見つかったチームのみ(2026年9月調査)。
# 2026年8月にCommons APIで実際にthumburl/license/artistを取得・確認済み。
TEAM_PHOTOS = {
    "SHADE RACING": {
        "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/No.884_SHADE_RACING_GR86_after_2022_ENEOS_Super_Taikyu_Series_Powered_by_Hankook.jpg/500px-No.884_SHADE_RACING_GR86_after_2022_ENEOS_Super_Taikyu_Series_Powered_by_Hankook.jpg",
        "credit": "Tokumeigakarinoaoshima",
        "license": "CC BY-SA 4.0",
        "source_url": "https://commons.wikimedia.org/wiki/File:No.884_SHADE_RACING_GR86_after_2022_ENEOS_Super_Taikyu_Series_Powered_by_Hankook.jpg",
    },
    "OVER DRIVE": {
        "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/No.66_odula_TONE_MOTUL_ROADSTER_after_2022_ENEOS_Super_Taikyu_Series_Powered_by_Hankook.jpg/500px-No.66_odula_TONE_MOTUL_ROADSTER_after_2022_ENEOS_Super_Taikyu_Series_Powered_by_Hankook.jpg",
        "credit": "Tokumeigakarinoaoshima",
        "license": "CC BY-SA 4.0",
        "source_url": "https://commons.wikimedia.org/wiki/File:No.66_odula_TONE_MOTUL_ROADSTER_after_2022_ENEOS_Super_Taikyu_Series_Powered_by_Hankook.jpg",
    },
    "TEAM NOPRO": {
        "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/No.37_DXL_POWER_MINERAL_EVO%E2%98%86NOPRO%E2%98%86NC_Roadster_after_2025_S-tai_Suzuka.jpg/500px-No.37_DXL_POWER_MINERAL_EVO%E2%98%86NOPRO%E2%98%86NC_Roadster_after_2025_S-tai_Suzuka.jpg",
        "credit": "Tokumeigakarinoaoshima",
        "license": "CC0 1.0",
        "source_url": "https://commons.wikimedia.org/wiki/File:No.37_DXL_POWER_MINERAL_EVO%E2%98%86NOPRO%E2%98%86NC_Roadster_after_2025_S-tai_Suzuka.jpg",
    },
    "チーム ジーモーション": {
        "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/No.60_Zenyaku_Kogyo_with_TEAM_G_MOTION%27_GR86_after_2022_ENEOS_Super_Taikyu_Series_Powered_by_Hankook_%281%29.jpg/500px-No.60_Zenyaku_Kogyo_with_TEAM_G_MOTION%27_GR86_after_2022_ENEOS_Super_Taikyu_Series_Powered_by_Hankook_%281%29.jpg",
        "credit": "Tokumeigakarinoaoshima",
        "license": "CC BY-SA 4.0",
        "source_url": "https://commons.wikimedia.org/wiki/File:No.60_Zenyaku_Kogyo_with_TEAM_G_MOTION%27_GR86_after_2022_ENEOS_Super_Taikyu_Series_Powered_by_Hankook_(1).jpg",
    },
    "浅野レーシングサービス": {
        "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/No.18_WedsSport_GR86_after_2022_ENEOS_Super_Taikyu_Series_Powered_by_Hankook.jpg/500px-No.18_WedsSport_GR86_after_2022_ENEOS_Super_Taikyu_Series_Powered_by_Hankook.jpg",
        "credit": "Tokumeigakarinoaoshima",
        "license": "CC BY-SA 4.0",
        "source_url": "https://commons.wikimedia.org/wiki/File:No.18_WedsSport_GR86_after_2022_ENEOS_Super_Taikyu_Series_Powered_by_Hankook.jpg",
    },
}


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def _latest_completed_round(today: date | None = None) -> int | None:
    today = today or date.today()
    completed = [n for n, end in ROUND_END_DATES if today >= end]
    return max(completed) if completed else None


def _find_class_block(html_text: str, class_label: str, max_n: int = 12) -> str | None:
    """順位表ページの `<li class="mix stN">` はNとクラス名の対応がシーズン内でも一定しない
    可能性があるため、各ブロック内の見出しテキストが実際にclass_labelと一致するものを探す。
    """
    for n in range(1, max_n):
        m = re.search(rf'<li class="mix st{n}">.*?</table>', html_text, re.S)
        if not m:
            continue
        label_m = re.search(r'Standing_Class[^>]*>\s*([^<]+)<', m.group(0))
        if label_m and label_m.group(1).strip() == class_label:
            return m.group(0)
    return None


def _classify_vehicle(car: str) -> str | None:
    """車両名テキストから、本ダッシュボードの追跡対象車両(gr86/mx5/brz)かどうかを判定する。

    ロードスター(MX-5)は現行ND型のみを追跡対象としており、旧型(NC型)は車名に明示的に
    "NC"と記載される慣行があるため、その表記があるものは除外する。BRZは現時点でST-4への
    参戦を確認できていないが、将来の参戦に備えて判定ロジック自体は用意しておく。
    """
    upper = car.upper()
    if "GR86" in upper or "GR 86" in upper:
        return "gr86"
    if "BRZ" in upper:
        return "brz"
    if ("ロードスター" in car or "ROADSTER" in upper or "MX-5" in upper or "MX5" in upper) and "NC" not in upper:
        return "mx5"
    return None


def fetch_full_standings(limit: int = 30) -> dict:
    """ST-4クラスの現在の順位表全体(順位/車番/チーム名/使用車種/ポイント)を実データで取得する。"""
    session = _session()
    try:
        resp = session.get(STANDINGS_URL, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding or "utf-8"
        html_text = resp.text

        block = _find_class_block(html_text, CLASS_LABEL)
        if not block:
            return {"standings": [], "error": f"{CLASS_LABEL}クラスの順位表が見つかりませんでした"}

        rows = re.findall(r"<tr>(.*?)</tr>", block, re.S)
        results: list[dict] = []
        for row in rows[1:]:
            cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)
            cells = [re.sub(r"<[^>]+>", "", c).strip() for c in cells]
            if len(cells) < 4 or not cells[0].isdigit():
                continue
            car_no, team, car = cells[1], cells[2], cells[3]
            points_raw = re.sub(r"[^\d.]", "", cells[-1]) or "0"
            results.append(
                {
                    "position": int(cells[0]),
                    "car_no": car_no,
                    "team": team,
                    "car": car,
                    "points": float(points_raw),
                    "vehicle": _classify_vehicle(car),
                }
            )
        rows_limited = results[:limit]
        return {
            "standings": rows_limited,
            "error": None if rows_limited else "現在、順位データが空です(シーズン開幕前などの可能性があります)",
        }
    except Exception as exc:  # noqa: BLE001
        return {"standings": [], "error": f"取得エラー: {exc}"}


def fetch_round_drivers(round_no: int) -> dict[str, list[dict]]:
    """指定ラウンドの公式エントリーリストから、ST-4クラスの car_no -> ドライバー一覧を返す。

    そのラウンドでST-4クラスが開催されなかった場合は空辞書を返す(実データで確認済み:
    全ラウンドがST-4を含むとは限らない)。
    """
    session = _session()
    try:
        resp = session.get(ROUND_ENTRY_LIST_URL.format(num=round_no), timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding or "utf-8"
        html_text = resp.text

        block_match = re.search(rf'Standing_Class"> {CLASS_LABEL}.*?</table>', html_text, re.S)
        if not block_match:
            return {}
        rows = re.findall(r"<tr>(.*?)</tr>", block_match.group(0), re.S)
        result: dict[str, list[dict]] = {}
        for row in rows[1:]:
            cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)
            cells = [re.sub(r"<[^>]+>", "", c).strip() for c in cells]
            if len(cells) < 5:
                continue
            car_no = cells[1].lstrip("0") or "0"
            driver_names = cells[4:]
            drivers: list[dict] = []
            for i, name in enumerate(driver_names):
                if i >= len(_SLOT_LABELS):
                    break
                if name.strip().lower() in _TBN_MARKERS:
                    continue
                drivers.append({"slot": _SLOT_LABELS[i], "name": name.strip()})
            if drivers:
                result[car_no] = drivers
        return result
    except Exception:  # noqa: BLE001
        return {}


def fetch_season_drivers() -> dict[str, list[dict]]:
    """開幕(第1戦)から直近の開催済みラウンドまでの全エントリーリストを集計し、
    car_no -> 今シーズンここまでに参戦した全ドライバー(重複除去済み)を返す。

    表記ゆれのある同一人物名は統合しない(公式データの表記のまま、ソースの正確性を優先する)。
    """
    latest = _latest_completed_round()
    if latest is None:
        return {}

    seen: dict[str, dict[str, dict]] = {}  # car_no -> {name: driver_dict}
    for round_no in range(1, latest + 1):
        round_drivers = fetch_round_drivers(round_no)
        for car_no, drivers in round_drivers.items():
            bucket = seen.setdefault(car_no, {})
            for driver in drivers:
                if driver["name"] not in bucket:
                    bucket[driver["name"]] = dict(driver)

    result: dict[str, list[dict]] = {}
    for car_no, bucket in seen.items():
        drivers = list(bucket.values())
        for driver in drivers:
            driver.pop("slot", None)
        result[car_no] = drivers
    return result


def fetch() -> dict:
    """ST-4クラスの全参戦チーム(GR86/BRZ/ロードスターはvehicleキーでハイライト対象を明示)、
    現在のシリーズ順位/ポイント、開幕から直近開催済みラウンドまでの全参戦ドライバー、
    手動収集のチーム背景・Wikimedia Commons写真(見つかったチームのみ)を返す。
    """
    standings = fetch_full_standings(limit=30)
    season_drivers = fetch_season_drivers()
    latest_round = _latest_completed_round()

    teams: list[dict] = []
    for row in standings["standings"]:
        entry = dict(row)
        lookup_no = row["car_no"].lstrip("0") or "0"
        entry["drivers"] = season_drivers.get(lookup_no, [])
        background = TEAM_BACKGROUND.get(row["team"])
        entry["description"] = background["description"] if background else None
        entry["verified"] = background["verified"] if background else None
        entry["photo"] = TEAM_PHOTOS.get(row["team"])
        teams.append(entry)

    return {
        "teams": teams,
        "rounds_completed": latest_round or 0,
        "rounds_total": len(ROUND_END_DATES),
        "error": standings["error"],
        "note": (
            "ST-4クラスは複数メーカーの市販車ベース車両が混走するクラスで、GR86/BRZ/ロード"
            "スターに限らずST-4クラスの全参戦チームを一覧表示しています(該当車種はハイライト"
            "表示)。順位/ポイント・チーム一覧・ドライバー名はいずれも公式サイト"
            "(supertaikyu.com)の実データです。ジェントルマンドライバー登録義務のレギュレー"
            "ションが確認できるのはST-X/ST-Z/ST-TCRクラスのみのため、ST-4クラスについては"
            "プロ/アマ区分の推定表示は行っていません。"
        ),
    }
