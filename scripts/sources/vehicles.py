"""GR86 Watchが追跡する3車種(GR86 / BRZ / ロードスター(MX-5))共通のクエリ設定。

このダッシュボードは元々「トヨタ GR86」単体を追うために計画されたが、ユーザーの要望により
以下3車種を対等な「追跡対象車両」として扱う:

  - gr86: トヨタ GR86(グレード: 素GR86 + "GR86 Cup Edition")。日本国内でも同じ"GR86"の
    呼称(旧86の実質後継)。
  - brz : スバル BRZ(GR86の兄弟車)。"BRZ"は単独では一般名詞的で曖昧(他業界の略称と衝突)
    なため、必ずメーカー名(スバル/Subaru)と組み合わせてクエリを組む。
  - mx5 : マツダ ロードスター(北米/欧州/豪州では「MX-5 Miata」「Mazda MX-5」表記)。
    日本語の「ロードスター」は単独では一般名詞(遊覧船・観覧車メーカー名等とも衝突しうる)
    のため、必ず「マツダ」と組み合わせる。

各車種・各地域(JP/US/EU/AU)ごとに、車種を一意に特定する「本体クエリ」を持たせ、
それぞれのソースモジュール(ニュース/レビュー/SNS話題/クレーム/イベント)が
トピック固有のキーワード(発表・レビュー・話題・不具合等)を末尾に付加してクエリを
組み立てる。結果には必ず "vehicle" キー(gr86/brz/mx5)を付与し、フロントエンド側で
車種別フィルタ・タグ表示に使う。

トリム名は完全一致検索では別グレードとしてヒットしないため("GR86"の完全一致検索は
"GR86 Cup Edition"を含まない語順のクエリと混同しないこと)、GR86は素グレードと
Cup Editionを別クエリとして両方実行し、結果をマージする(SKILL.mdの教訓どおり)。
"""

from __future__ import annotations

REGIONS: dict[str, dict[str, str]] = {
    "jp": {"hl": "ja", "gl": "JP", "ceid": "JP:ja", "label": "日本"},
    "us": {"hl": "en-US", "gl": "US", "ceid": "US:en", "label": "米国"},
    "eu": {"hl": "en-GB", "gl": "GB", "ceid": "GB:en", "label": "欧州"},
    "au": {"hl": "en-AU", "gl": "AU", "ceid": "AU:en", "label": "豪州"},
}

VEHICLES: list[str] = ["gr86", "brz", "mx5"]

VEHICLE_LABELS: dict[str, dict[str, str]] = {
    "gr86": {"ja": "トヨタ GR86", "en": "Toyota GR86"},
    "brz": {"ja": "スバル BRZ", "en": "Subaru BRZ"},
    "mx5": {"ja": "マツダ ロードスター(MX-5)", "en": "Mazda MX-5 (Roadster)"},
}

# 車種ごと・地域ごとの「本体クエリ」候補(複数ある場合はグレード違いなどをすべて実行する)。
VEHICLE_QUERY_TERMS: dict[str, dict[str, list[str]]] = {
    "gr86": {
        "jp": ['"GR86" トヨタ', '"GR86 Cup Edition" トヨタ'],
        "us": ['"GR86" Toyota', '"GR86 Cup Edition" Toyota'],
        "eu": ['"GR86" Toyota', '"GR86 Cup Edition" Toyota'],
        "au": ['"GR86" Toyota', '"GR86 Cup Edition" Toyota'],
    },
    "brz": {
        "jp": ['"BRZ" スバル'],
        "us": ['"BRZ" Subaru'],
        "eu": ['"BRZ" Subaru'],
        "au": ['"BRZ" Subaru'],
    },
    "mx5": {
        # 日本語の「ロードスター」は単独では曖昧なため必ず「マツダ」とAND検索する。
        "jp": ["ロードスター マツダ"],
        "us": ['"MX-5 Miata" Mazda', '"Mazda MX-5" Miata'],
        "eu": ['"MX-5" Mazda', '"Mazda MX-5"'],
        "au": ['"MX-5" Mazda', '"Mazda MX-5"'],
    },
}


def build_queries(topic_terms: dict[str, str], vehicles: list[str] | None = None) -> list[tuple[str, str, str, str, str]]:
    """全車種 × 全地域のクエリタプル (query, hl, gl, ceid, vehicle) を返す。

    topic_terms: 地域キー(jp/us/eu/au) -> そのトピック固有のキーワード文字列。
    vehicles: 対象車種を絞りたい場合に指定(省略時は3車種すべて)。
    """
    out: list[tuple[str, str, str, str, str]] = []
    for vehicle in vehicles or VEHICLES:
        for region_key, region in REGIONS.items():
            suffix = topic_terms.get(region_key, "")
            for base in VEHICLE_QUERY_TERMS[vehicle][region_key]:
                query = f"{base} {suffix}".strip()
                out.append((query, region["hl"], region["gl"], region["ceid"], vehicle))
    return out


def tag_and_extend(items_out: list[dict], results: list[dict], vehicle: str) -> None:
    """fetch_google_news_rss()の結果に vehicle タグを付けてitems_outへ追加する。"""
    for r in results:
        r["vehicle"] = vehicle
    items_out.extend(results)
