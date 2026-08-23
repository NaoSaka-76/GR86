(function () {
  "use strict";

  /* ---------------------------------------------------------------------
   * I18N — all dashboard chrome copy lives here, keyed by stable ids that
   * also flow through the JSON (section keys, region keys, series keys,
   * vehicle keys). Scraped article/video titles are NEVER translated —
   * only this chrome. Persisted language choice lives in localStorage.
   * ------------------------------------------------------------------- */

  var I18N = {
    ja: {
      eyebrow: "GR86 / トヨタ86 / BRZ / MX-5 モニタリング",
      title: "GR86 Watch",
      statusLoading: "読み込み中…",
      lastUpdatedPrefix: "最終更新: ",
      lastUpdatedUnknown: "不明",
      cadenceChip: "30分おき",
      cadenceLabel: "自動更新",
      vehicleFilter: {
        all: "すべて",
        gr86: "GR86",
        toyota86: "トヨタ86(GT86/FT86)",
        brz: "BRZ",
        mx5: "ロードスター(MX-5)",
      },
      kind: { official_news: "公式", media_review: "メディア評価" },
      sentiment: { positive: "ポジティブ", negative: "ネガティブ", neutral: "中立" },
      sentimentTipPositive: " という語がポジティブと判定されました",
      sentimentTipNegative: " という語がネガティブと判定されました",
      sentimentReasonPrefix: "判定根拠: ",
      itemUnknownTitle: "(タイトル不明)",
      panelEmpty: "現在、該当する情報はありません。",
      seriesEmpty: "該当情報なし",
      scheduleUnavailable: "日程情報を取得できませんでした。",
      scheduleNext: "次戦",
      scheduleHeading: "レース日程",
      rankingHeading: "シリーズランキング",
      rankingDriversHeading: "ドライバーズランキング",
      topicsHeading: "トピックス",
      resultsHeading: "最新レース結果",
      standingsNewsHeading: "ランキング関連ニュース",
      rosterHeading: "参戦チーム一覧",
      rosterRoundsNote: function (done, total) {
        return "開幕(第1戦)から第" + done + "戦(全" + total + "戦)まで開催済みのエントリーリストを集計した参戦ドライバーです。";
      },
      rosterPointsUnit: "pt",
      rosterNoData: "順位データなし",
      rosterUnverified: "一次資料未裏取り",
      photoPlaceholder: "写真なし",
      photoCredit: function (credit, license) {
        return "写真: " + credit + "（" + license + "、Wikimedia Commons経由）";
      },
      standingsSearchLink: "公式ランキングを検索 ↗",
      scheduleLinkText: "公式スケジュールを見る ↗",
      unitCount: "件",
      unitVideos: "本",
      tabLatest: "最新順",
      tabBuzz: "話題順",
      youtubeGlobalLabel: "グローバル",
      youtubeJpLabel: "日本語",
      statTotal: "本日の総情報件数",
      statSentiment: "評判(公式リリースを除く)",
      statSentimentUnit: "件ポジティブ",
      statYoutube: "YouTube動画(グローバル+日本語)",
      statMotorsports: "モータースポーツ関連話題",
      rivalsUnconfirmed: "reference-only",
      rivalsConfirmed: { official: "公式サイトで確認", media: "報道ベース(公式未直接確認)" },
      rivalsSourceLabel: "情報源: ",
      rivalsPriceBarTitle: "価格帯比較",
      formatsConfidence: {
        official: "一次資料で確認",
        media_report: "報道ベース(未一次確認)",
        unavailable: "情報未公開",
      },
      formatsRows: {
        eligibility: "参戦資格",
        points: "ポイント制度",
        weekend_format: "レースウィークエンド構成",
        classification: "ドライバー区分",
        season_length: "シーズン構成",
      },
      formatsUnavailable: "公開されている競技フォーマットの詳細情報を確認できませんでした。",
      formatsSourcesLabel: "情報源: ",
      sections: {
        news_reviews: "公式リリース & メディア評価",
        youtube: "YouTube",
        social_buzz: "SNSでの話題",
        complaints: "お客様の声・クレーム関連情報",
        events: "世界各地のイベント情報",
        motorsports: "モータースポーツ(GR Cup ほか)",
        motorsports_formats: "各シリーズの競技フォーマット解説",
        rivals: "ライバル車 スペック比較(グレード別・日本/米国/豪州)",
      },
      regions: {
        north_america: "北米",
        japan_asia: "日本・アジア",
        australia: "オーストラリア",
        europe: "欧州",
        mx5_cup: "ロードスター(MX-5)ワンメイク",
      },
      series: {
        gr_cup: "Toyota GR Cup(GR86 Cup Edition ワンメイクレース)",
        tgr_86brz_cup: "TGR GR86/BRZ Cup(スーパーGT併催・日本)",
        super_taikyu_st4: "スーパー耐久 ST-4クラス(多メーカー混走・日本)",
        jaf_rally_jn4: "全日本ラリー選手権 JN-4クラス(GR86参戦確認済み・日本)",
        jaf_gymkhana_pn4: "全日本ジムカーナ選手権 PN4クラス(GR86参戦確認済み・日本)",
        jaf_dirttrial_pn3: "全日本ダートトライアル選手権 PN3クラス(GR86参戦確認済み・日本)",
        gr_cup_australia: "GR Cup Australia(旧Toyota 86 Racing Series)",
        tmg_gt86_cup_vln: "TMG GT86 Cup(独ニュルブルクリンク VLN/NLS内クラス・現行開催は未確認)",
        mx5_cup: "Mazda MX-5 Cup(IMSA主催・北米)",
      },
      footer:
        "本ダッシュボードは公開情報源(Googleニュース検索・YouTube検索結果・各シリーズ公式サイト)を自動集計した非公式のモニタリングツールです。" +
        "トヨタ自動車・SUBARU・マツダの公式発表とは異なる場合があります。X/Facebook/Instagramの投稿本体、および社内クレームシステムのデータは含まれません。" +
        "ポジティブ/ネガティブ表示は見出し文のみに基づく自動推定(簡易辞書・VADER)であり、参考値です。ライバル車スペック比較・モータースポーツ" +
        "競技フォーマット解説は手動調査による静的データで、自動更新の対象外です。トヨタ86(GT86/FT86)はYouTube/SNS話題のみを対象としています" +
        "(生産終了モデルのため公式リリース/メディア評価/クレームの対象外)。",
    },
    en: {
      eyebrow: "GR86 / TOYOTA 86 / BRZ / MX-5 MONITORING",
      title: "GR86 Watch",
      statusLoading: "Loading…",
      lastUpdatedPrefix: "Last updated: ",
      lastUpdatedUnknown: "unknown",
      cadenceChip: "Every 30 min",
      cadenceLabel: "auto-refresh",
      vehicleFilter: {
        all: "All",
        gr86: "GR86",
        toyota86: "Toyota 86 (GT86/FT86)",
        brz: "BRZ",
        mx5: "MX-5 (Roadster)",
      },
      kind: { official_news: "Official", media_review: "Review" },
      sentiment: { positive: "Positive", negative: "Negative", neutral: "Neutral" },
      sentimentTipPositive: " matched as positive",
      sentimentTipNegative: " matched as negative",
      sentimentReasonPrefix: "Matched words: ",
      itemUnknownTitle: "(untitled)",
      panelEmpty: "No items right now.",
      seriesEmpty: "No items right now.",
      scheduleUnavailable: "Could not fetch a schedule.",
      scheduleNext: "Next round",
      scheduleHeading: "Race schedule",
      rankingHeading: "Series standings",
      rankingDriversHeading: "Driver standings",
      topicsHeading: "Topics",
      resultsHeading: "Latest results",
      standingsNewsHeading: "Standings news",
      rosterHeading: "Full Entry List",
      rosterRoundsNote: function (done, total) {
        return "Drivers aggregated from entry lists spanning round 1 through round " + done + " of " + total + " completed so far this season.";
      },
      rosterPointsUnit: "pt",
      rosterNoData: "No standings data",
      rosterUnverified: "not independently verified",
      photoPlaceholder: "No photo",
      photoCredit: function (credit, license) {
        return "Photo: " + credit + " (" + license + "), via Wikimedia Commons";
      },
      standingsSearchLink: "Search official standings ↗",
      scheduleLinkText: "View official schedule ↗",
      unitCount: "",
      unitVideos: "",
      tabLatest: "Latest",
      tabBuzz: "Trending",
      youtubeGlobalLabel: "Global",
      youtubeJpLabel: "Japanese",
      statTotal: "Items tracked today",
      statSentiment: "Sentiment (excl. official releases)",
      statSentimentUnit: " positive",
      statYoutube: "YouTube videos (global + JP)",
      statMotorsports: "Motorsports mentions",
      rivalsUnconfirmed: "reference-only",
      rivalsConfirmed: { official: "Confirmed via official site", media: "Media-sourced (not directly confirmed by manufacturer)" },
      rivalsSourceLabel: "Source: ",
      rivalsPriceBarTitle: "Price range comparison",
      formatsConfidence: {
        official: "Confirmed via primary source",
        media_report: "Media-report based (not primary-confirmed)",
        unavailable: "Not publicly available",
      },
      formatsRows: {
        eligibility: "Eligibility",
        points: "Points system",
        weekend_format: "Race weekend format",
        classification: "Driver classification",
        season_length: "Season length",
      },
      formatsUnavailable: "Could not confirm public details on this series' competition format.",
      formatsSourcesLabel: "Sources: ",
      sections: {
        news_reviews: "Official Release & Media Review",
        youtube: "YouTube",
        social_buzz: "Social Buzz",
        complaints: "Complaints / Owner Feedback",
        events: "Events Worldwide",
        motorsports: "Motorsports (GR Cup and others)",
        motorsports_formats: "Series Format Explainers",
        rivals: "Rival Vehicle Spec Comparison (by Grade, Japan/US/Australia)",
      },
      regions: {
        north_america: "North America",
        japan_asia: "Japan / Asia",
        australia: "Australia",
        europe: "Europe",
        mx5_cup: "MX-5 (Roadster) One-Make",
      },
      series: {
        gr_cup: "Toyota GR Cup (GR86 Cup Edition one-make series)",
        tmg_gt86_cup_vln: "TMG GT86 Cup (class within Germany's Nürburgring VLN/NLS series — current status unconfirmed)",
        tgr_86brz_cup: "TGR GR86/BRZ Cup (Super GT support race, Japan)",
        super_taikyu_st4: "Super Taikyu ST-4 Class (multi-manufacturer, Japan)",
        jaf_rally_jn4: "All Japan Rally Championship JN-4 Class (confirmed GR86 entries, Japan)",
        jaf_gymkhana_pn4: "All Japan Gymkhana Championship PN4 Class (confirmed GR86 entries, Japan)",
        jaf_dirttrial_pn3: "All Japan Dirt Trial Championship PN3 Class (confirmed GR86 entries, Japan)",
        gr_cup_australia: "GR Cup Australia (formerly Toyota 86 Racing Series)",
        mx5_cup: "Mazda MX-5 Cup (IMSA-sanctioned, North America)",
      },
      footer:
        "This dashboard is an unofficial monitoring tool that auto-aggregates public sources (Google News search, YouTube search results, official series sites). " +
        "It may differ from official Toyota, Subaru, or Mazda communications. It does not include raw X/Facebook/Instagram posts or internal complaint-system data. " +
        "Positive/negative labels are automated headline-only estimates (a simple lexicon plus VADER) and should be treated as reference only. The rival vehicle spec " +
        "comparison and motorsports format explainers are hand-researched static data, not part of the 30-minute auto-refresh. Toyota 86 (GT86/FT86) " +
        "is tracked in YouTube/social buzz only (a discontinued model, so it's excluded from official news/reviews/complaints).",
    },
  };

  var LANG_KEY = "gr86watch_lang";
  var VEHICLE_KEYS = ["gr86", "toyota86", "brz", "mx5"];
  // Display buckets used by the per-section すべて/GR86/BRZ/ロードスター filter controls.
  // Toyota86(GT86/FT86) content is folded into the GR86 bucket here (it keeps its own
  // "トヨタ86" badge on individual items, but is not a separate filter button anymore).
  var DISPLAY_VEHICLE_KEYS = ["gr86", "brz", "mx5"];

  function vehicleBucket(vehicle) {
    return vehicle === "toyota86" ? "gr86" : vehicle;
  }

  function filterItemsByBucket(items, bucket) {
    if (!bucket || bucket === "all") return items;
    return items.filter(function (it) { return vehicleBucket(it.vehicle) === bucket; });
  }

  function getLang() {
    try {
      var saved = localStorage.getItem(LANG_KEY);
      if (saved === "ja" || saved === "en") return saved;
    } catch (e) {}
    return "ja";
  }
  function setLang(lang) {
    try { localStorage.setItem(LANG_KEY, lang); } catch (e) {}
  }

  var currentLang = getLang();

  function t() {
    return I18N[currentLang] || I18N.ja;
  }

  /** Resolves a bilingual JSON field ({ja,en}) from the static catalogs (rivals.json,
   * motorsports_formats.json). Plain strings (proper nouns) pass through as-is. */
  function pick(value) {
    if (value === null || value === undefined) return "";
    if (typeof value === "string" || typeof value === "number") return String(value);
    return value[currentLang] || value.ja || value.en || "";
  }

  var ICONS = {
    doc:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4"/>' +
      '<line x1="9.5" y1="12" x2="16" y2="12"/><line x1="9.5" y1="15.5" x2="16" y2="15.5"/><line x1="9.5" y1="19" x2="13" y2="19"/></svg>',
    play:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">' +
      '<circle cx="12" cy="12" r="9"/><path d="M10 8.5l6 3.5-6 3.5z" fill="currentColor" stroke="none"/></svg>',
    chat:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="M4 5h16v11H8l-4 4z"/></svg>',
    star:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round">' +
      '<path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.2 1 5.9-5.2-2.8-5.2 2.8 1-5.9-4.3-4.2 5.9-.8z"/></svg>',
    alert:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="M12 4l9.5 16H2.5z"/><line x1="12" y1="10" x2="12" y2="14.5"/><circle cx="12" cy="17.3" r="0.9" fill="currentColor" stroke="none"/></svg>',
    flag:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="M5 3v18"/><path d="M5 4h14l-3 3.5 3 3.5H5z"/></svg>',
    calendar:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">' +
      '<rect x="3.5" y="5" width="17" height="15" rx="2"/><line x1="3.5" y1="9.5" x2="20.5" y2="9.5"/>' +
      '<line x1="8" y1="3" x2="8" y2="6.5"/><line x1="16" y1="3" x2="16" y2="6.5"/></svg>',
    scale:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="M12 3v18"/><path d="M5 8l-3 6a3 3 0 0 0 6 0z"/><path d="M19 8l-3 6a3 3 0 0 0 6 0z"/><path d="M3 8h18"/><path d="M8 21h8"/></svg>',
    book:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
  };

  /* ---------------------------------------------------------------------
   * Section order (2026-09 restructure: merged news+reviews, per-section
   * vehicle filters instead of one global header control):
   *   1. Official release & media review (merged, すべて/GR86/BRZ/ロードスター filter)
   *   2. YouTube (same filter + trending/latest tabs + global/JP groups)
   *   3. Social buzz (same filter + trending/latest tabs)
   *   4. Complaints (same filter + trending/latest tabs)
   *   5. Events
   *   6. Motorsports -> format explainers -> rivals (grade-level spec comparison)
   * ------------------------------------------------------------------- */
  var LAYOUT = [
    { key: "news_reviews", size: "full", icon: "doc" },
    { key: "youtube", size: "full", icon: "play" },
    { key: "social_buzz", size: "full", icon: "chat" },
    { key: "complaints", size: "full", icon: "alert" },
    { key: "events", size: "full", icon: "calendar" },
    { key: "motorsports", size: "full", icon: "flag" },
    { key: "motorsports_formats", size: "full", icon: "book" },
    { key: "rivals", size: "full", icon: "scale" },
  ];

  var board = document.getElementById("board");
  var statsEl = document.getElementById("stats");
  var lastUpdatedEl = document.getElementById("last-updated");
  var statusDot = document.getElementById("status-dot");
  var langToggleEl = document.getElementById("lang-toggle");

  var lastData = null;
  var lastRivals = null;
  var lastFormats = null;

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function formatPublished(raw) {
    if (!raw) return "";
    var parsed = new Date(raw);
    if (!isNaN(parsed.getTime()) && /\d{4}/.test(raw)) {
      return parsed.toLocaleString(currentLang === "ja" ? "ja-JP" : "en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    }
    return raw;
  }

  function vehicleBadge(vehicle) {
    if (!vehicle || VEHICLE_KEYS.indexOf(vehicle) === -1) return null;
    return el("span", "vehicle-badge vehicle-badge--" + vehicle, t().vehicleFilter[vehicle]);
  }

  function kindBadge(kind) {
    if (!kind || !t().kind[kind]) return null;
    return el("span", "kind-badge kind-badge--" + kind, t().kind[kind]);
  }

  function sentimentPill(sentiment) {
    if (!sentiment || sentiment.label === "neutral") return null;
    var pill = el(
      "span",
      "sentiment-pill sentiment-pill--" + sentiment.label,
      sentiment.label === "positive" ? "▲ " + t().sentiment.positive : "▼ " + t().sentiment.negative
    );
    var reasons = sentiment.reasons || [];
    if (reasons.length > 0) {
      var tip =
        t().sentimentReasonPrefix +
        reasons.join(" / ") +
        (sentiment.label === "positive" ? t().sentimentTipPositive : t().sentimentTipNegative);
      pill.setAttribute("data-tip", tip);
      pill.tabIndex = 0;
    }
    return pill;
  }

  function buildItem(item) {
    var sentimentLabel = item.sentiment ? item.sentiment.label : "neutral";
    var a = el("a", "item item--" + sentimentLabel);
    a.href = item.url || "#";
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    if (item.vehicle) a.dataset.vehicle = item.vehicle;
    if (!item.url) {
      a.removeAttribute("href");
      a.style.cursor = "default";
    }

    if (item.thumbnail) {
      var img = el("img", "item__thumb");
      img.src = item.thumbnail;
      img.alt = "";
      img.loading = "lazy";
      a.appendChild(img);
    }

    var body = el("div", "item__body");
    body.appendChild(el("span", "item__title", item.title || t().itemUnknownTitle));

    var meta = el("div", "item__meta");
    var badge = vehicleBadge(item.vehicle);
    if (badge) meta.appendChild(badge);
    var kb = kindBadge(item.kind);
    if (kb) meta.appendChild(kb);
    var pill = sentimentPill(item.sentiment);
    if (pill) meta.appendChild(pill);
    if (item.source) meta.appendChild(el("span", null, item.source));
    var published = formatPublished(item.published);
    if (published) meta.appendChild(el("span", null, published));
    if (item.view_count_text) {
      meta.appendChild(el("span", "item__metric", item.view_count_text));
    }
    body.appendChild(meta);
    a.appendChild(body);

    return a;
  }

  function buildList(items) {
    var list = el("ul", "panel__list");
    items.forEach(function (item) {
      var li = el("li");
      li.appendChild(buildItem(item));
      list.appendChild(li);
    });
    return list;
  }

  /** A local すべて/GR86/BRZ/ロードスター filter bar, independent per panel (there is no
   * longer a single shared header-level filter). Calls onChange(bucket) whenever the
   * active button changes; the panel that owns this bar re-filters and re-renders its
   * own item list(s) in response — this bar does not touch the DOM outside itself. */
  function buildSectionVehicleFilter(onChange) {
    var bar = el("div", "section-filter");
    var current = "all";
    var buttons = {};
    ["all"].concat(DISPLAY_VEHICLE_KEYS).forEach(function (v) {
      var btn = el("button", "section-filter__btn" + (v === "all" ? " is-active" : ""));
      btn.type = "button";
      btn.dataset.vehicle = v;
      if (v !== "all") {
        var dot = el("span", "section-filter__dot");
        dot.style.color = "var(--veh-" + v + ")";
        btn.appendChild(dot);
      }
      btn.appendChild(document.createTextNode(t().vehicleFilter[v]));
      btn.addEventListener("click", function () {
        if (current === v) return;
        current = v;
        Object.keys(buttons).forEach(function (k) { buttons[k].classList.toggle("is-active", k === v); });
        onChange(v);
      });
      buttons[v] = btn;
      bar.appendChild(btn);
    });
    return bar;
  }

  function buildPanelHeader(icon, label, count) {
    var header = el("div", "panel__header");
    var iconWrap = el("div", "panel__icon");
    iconWrap.innerHTML = ICONS[icon] || "";
    header.appendChild(iconWrap);
    header.appendChild(el("h2", "panel__title", label));
    if (count !== undefined) header.appendChild(el("span", "panel__count", count + (t().unitCount ? " " + t().unitCount : "")));
    return header;
  }

  function buildGenericPanel(icon, sectionKey, section, size) {
    var panel = el("section", "panel panel--" + size);
    var items = section.items || [];
    panel.appendChild(buildPanelHeader(icon, t().sections[sectionKey] || section.label, items.length));

    if (section.note) panel.appendChild(el("p", "panel__note", section.note));

    if (items.length === 0) {
      panel.appendChild(el("p", "panel__empty", t().panelEmpty));
      return panel;
    }
    panel.appendChild(buildList(items));
    return panel;
  }

  /** Merged official-release + media-review panel (すべて/GR86/BRZ/ロードスター filter,
   * no tabs — a single recency-sorted feed covering GR86 + BRZ + ロードスター). */
  function buildNewsReviewsPanel(icon, section) {
    var panel = el("section", "panel panel--full");
    var items = section.items || [];
    panel.appendChild(buildPanelHeader(icon, t().sections.news_reviews || section.label, items.length));
    if (section.note) panel.appendChild(el("p", "panel__note", section.note));

    var listWrap = el("div");
    function renderList(bucket) {
      listWrap.innerHTML = "";
      var filtered = filterItemsByBucket(items, bucket);
      if (filtered.length === 0) {
        listWrap.appendChild(el("p", "panel__empty", t().panelEmpty));
      } else {
        listWrap.appendChild(buildList(filtered));
      }
    }
    panel.appendChild(buildSectionVehicleFilter(renderList));
    renderList("all");
    panel.appendChild(listWrap);
    return panel;
  }

  /** Shared "latest / trending" tabbed panel — used by complaints and social_buzz,
   * which both provide {items (latest), items_buzz (trending), note}. Also carries the
   * すべて/GR86/BRZ/ロードスター filter, which applies within whichever tab is active. */
  function buildTabbedPanel(icon, sectionKey, section) {
    var panel = el("section", "panel panel--full");
    var latestItems = section.items || [];
    var buzzItems = section.items_buzz || [];
    panel.appendChild(buildPanelHeader(icon, t().sections[sectionKey] || section.label, latestItems.length));
    if (section.note) panel.appendChild(el("p", "panel__note", section.note));

    var currentTab = "latest";
    var currentBucket = "all";

    var tabs = el("div", "tab-group");
    var tabLatest = el("button", "tab-group__btn is-active", t().tabLatest);
    var tabBuzz = el("button", "tab-group__btn", t().tabBuzz);
    tabs.appendChild(tabLatest);
    tabs.appendChild(tabBuzz);
    panel.appendChild(tabs);
    panel.appendChild(
      buildSectionVehicleFilter(function (bucket) {
        currentBucket = bucket;
        renderList();
      })
    );

    var listWrap = el("div");
    function renderList() {
      listWrap.innerHTML = "";
      var items = filterItemsByBucket(currentTab === "latest" ? latestItems : buzzItems, currentBucket);
      if (items.length === 0) {
        listWrap.appendChild(el("p", "panel__empty", t().panelEmpty));
      } else {
        listWrap.appendChild(buildList(items));
      }
    }
    renderList();
    panel.appendChild(listWrap);

    tabLatest.addEventListener("click", function () {
      tabLatest.classList.add("is-active");
      tabBuzz.classList.remove("is-active");
      currentTab = "latest";
      renderList();
    });
    tabBuzz.addEventListener("click", function () {
      tabBuzz.classList.add("is-active");
      tabLatest.classList.remove("is-active");
      currentTab = "buzz";
      renderList();
    });

    return panel;
  }

  function buildSubGroup(title, items) {
    var group = el("div", "series-card__group");
    group.appendChild(el("div", "series-card__group-title", title));
    if (items.length === 0) {
      group.appendChild(el("p", "panel__empty", t().seriesEmpty));
    } else {
      group.appendChild(buildList(items));
    }
    return group;
  }

  /** YouTube panel: Trending(popular)/Latest(new) tabs, each split into Global/Japanese
   * sub-groups, plus the すべて/GR86/BRZ/ロードスター filter (applies within whichever
   * tab is active). Covers all 4 raw vehicle tags (GR86/Toyota86/BRZ/MX-5), with
   * Toyota86 folded into the GR86 filter bucket. */
  function buildYoutubePanel(icon, section) {
    var panel = el("section", "panel panel--full");
    var global = section.global || { popular: [], new: [] };
    var jp = section.jp || { popular: [], new: [] };
    var totalCount = global.popular.length + global.new.length + jp.popular.length + jp.new.length;
    panel.appendChild(buildPanelHeader(icon, t().sections.youtube || section.label, totalCount));

    var currentTab = "trending";
    var currentBucket = "all";

    var tabs = el("div", "tab-group");
    var tabTrending = el("button", "tab-group__btn is-active", t().tabBuzz);
    var tabLatest = el("button", "tab-group__btn", t().tabLatest);
    tabs.appendChild(tabTrending);
    tabs.appendChild(tabLatest);
    panel.appendChild(tabs);
    panel.appendChild(
      buildSectionVehicleFilter(function (bucket) {
        currentBucket = bucket;
        renderGroups();
      })
    );

    var listWrap = el("div");
    function renderGroups() {
      listWrap.innerHTML = "";
      var globalItems = filterItemsByBucket(currentTab === "trending" ? global.popular : global.new, currentBucket);
      var jpItems = filterItemsByBucket(currentTab === "trending" ? jp.popular : jp.new, currentBucket);
      listWrap.appendChild(buildSubGroup(t().youtubeGlobalLabel, globalItems));
      listWrap.appendChild(buildSubGroup(t().youtubeJpLabel, jpItems));
    }
    renderGroups();
    panel.appendChild(listWrap);

    tabTrending.addEventListener("click", function () {
      tabTrending.classList.add("is-active");
      tabLatest.classList.remove("is-active");
      currentTab = "trending";
      renderGroups();
    });
    tabLatest.addEventListener("click", function () {
      tabLatest.classList.add("is-active");
      tabTrending.classList.remove("is-active");
      currentTab = "latest";
      renderGroups();
    });

    return panel;
  }

  function buildStandingsChart(rows) {
    var maxPoints = rows.reduce(function (m, r) { return Math.max(m, r.points); }, 1);
    var chart = el("div", "standings-chart");
    rows.forEach(function (row) {
      var rowEl = el("div", "standings-chart__row");
      rowEl.appendChild(el("span", "standings-chart__pos", String(row.position)));

      var main = el("div", "standings-chart__main");
      main.appendChild(el("span", "standings-chart__name", row.name));

      var track = el("div", "standings-chart__track");
      var fill = el("div", "standings-chart__fill");
      fill.style.width = Math.max(4, (100 * row.points) / maxPoints) + "%";
      track.appendChild(fill);
      main.appendChild(track);

      rowEl.appendChild(main);
      rowEl.appendChild(el("span", "standings-chart__points", String(row.points)));
      chart.appendChild(rowEl);
    });
    return chart;
  }

  /** A collapsed-by-default <details>/<summary> block used to hide bulkier real-data
   * displays (schedule lists, standings charts) behind a toggle, so a series card with
   * real data doesn't dominate the page height. Native <details> needs no JS wiring and
   * is keyboard/screen-reader accessible for free. */
  function buildCollapsible(summaryText, count) {
    var details = el("details", "collapsible");
    var summary = el("summary", "collapsible__summary");
    summary.appendChild(document.createTextNode(summaryText));
    if (count !== undefined) summary.appendChild(el("span", "collapsible__count", String(count)));
    details.appendChild(summary);
    var content = el("div", "collapsible__content");
    details.appendChild(content);
    return { details: details, content: content };
  }

  function buildScheduleBlock(s) {
    var wrap = el("div", "series-card__group");

    if (!s.has_real_schedule) {
      wrap.appendChild(el("div", "series-card__group-title", t().scheduleHeading));
      if (s.schedule_chart_note) wrap.appendChild(el("p", "panel__note series-card__chart-note", s.schedule_chart_note));
      if (s.schedule_link) {
        var link = el("a", "series-card__link", t().scheduleLinkText);
        link.href = s.schedule_link;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        wrap.appendChild(link);
      }
      return wrap;
    }

    var rounds = s.schedule || [];
    if (rounds.length === 0) {
      wrap.appendChild(el("div", "series-card__group-title", t().scheduleHeading));
      wrap.appendChild(el("p", "panel__empty", t().scheduleUnavailable));
      return wrap;
    }

    var built = buildCollapsible(t().scheduleHeading, rounds.length);

    var nextRace = rounds.filter(function (r) { return r.status === "upcoming"; })[0];
    if (nextRace) {
      var next = el("div", "schedule-next");
      next.appendChild(el("span", "schedule-next__label", t().scheduleNext));
      next.appendChild(el("span", "schedule-next__date", nextRace.date_range));
      next.appendChild(
        el("span", "schedule-next__track", [nextRace.round, nextRace.name, nextRace.track].filter(Boolean).join(" · "))
      );
      built.content.appendChild(next);
    }

    var list = el("ul", "schedule-list");
    rounds.forEach(function (r) {
      var li = el("li", "schedule-list__item schedule-list__item--" + r.status);
      li.appendChild(el("span", "schedule-list__dot"));
      li.appendChild(el("span", "schedule-list__date", r.date_range));
      li.appendChild(el("span", "schedule-list__label", [r.round, r.name, r.track].filter(Boolean).join(" · ")));
      list.appendChild(li);
    });
    built.content.appendChild(list);
    wrap.appendChild(built.details);

    return wrap;
  }

  function buildRankingBlock(s) {
    var wrap = el("div", "series-card__group");
    var hasTeam = s.standings_chart && s.standings_chart.length > 0;
    var hasDriver = s.driver_standings_chart && s.driver_standings_chart.length > 0;

    if (!hasTeam && !hasDriver) {
      wrap.appendChild(el("div", "series-card__group-title", t().rankingHeading));
      if (s.standings_chart_note) wrap.appendChild(el("p", "panel__note series-card__chart-note", s.standings_chart_note));
      return wrap;
    }

    var count = (hasTeam ? s.standings_chart.length : 0) + (hasDriver ? s.driver_standings_chart.length : 0);
    var built = buildCollapsible(t().rankingHeading, count);
    if (hasTeam) built.content.appendChild(buildStandingsChart(s.standings_chart));
    if (s.standings_chart_note) built.content.appendChild(el("p", "panel__note series-card__chart-note", s.standings_chart_note));
    if (hasDriver) {
      built.content.appendChild(el("div", "series-card__group-title", t().rankingDriversHeading));
      built.content.appendChild(buildStandingsChart(s.driver_standings_chart));
    }
    wrap.appendChild(built.details);
    return wrap;
  }

  /** Full entrant list for a multi-manufacturer class (currently: Super Taikyu ST-4).
   * Unlike the old single-vehicle GR Cup roster (removed), this lists EVERY team in the
   * class regardless of manufacturer, highlighting only the entries that match one of
   * this dashboard's tracked vehicles (GR86/BRZ/ロードスター) — same technique the
   * sibling "Supra GT4 Watch" project uses to highlight one car within a full catalog.
   * Rendered directly (not collapsed) since it's the primary content of this card;
   * schedule/ranking/topics below it use the collapsed-by-default pattern instead. */
  function buildRosterBlock(s) {
    var wrap = el("div", "series-card__group");
    var roster = s.roster || [];

    if (roster.length === 0) {
      wrap.appendChild(el("div", "series-card__group-title", t().rosterHeading));
      wrap.appendChild(el("p", "panel__empty", t().panelEmpty));
      return wrap;
    }

    // Collapsible like schedule/ranking below it — defaults closed, consistent with
    // those blocks.
    var built = buildCollapsible(t().rosterHeading, roster.length);

    if (s.rounds_completed !== undefined && s.rounds_total !== undefined) {
      built.content.appendChild(el("p", "panel__note st4-roster-note", t().rosterRoundsNote(s.rounds_completed, s.rounds_total)));
    }

    var grid = el("div", "st4-roster-grid");
    roster.forEach(function (team) {
      var highlighted = team.vehicle && VEHICLE_KEYS.indexOf(team.vehicle) !== -1;
      var card = el("div", "st4-team-card" + (highlighted ? " st4-team-card--highlight st4-team-card--" + team.vehicle : ""));

      if (team.photo) {
        var img = el("img", "st4-team-card__photo");
        img.src = team.photo.src;
        img.alt = team.team;
        img.loading = "lazy";
        card.appendChild(img);
        var credit = el("a", "st4-team-card__photo-credit");
        credit.href = team.photo.source_url;
        credit.target = "_blank";
        credit.rel = "noopener noreferrer";
        credit.textContent = t().photoCredit(team.photo.credit, team.photo.license);
        card.appendChild(credit);
      } else {
        card.appendChild(el("div", "st4-team-card__photo st4-team-card__photo--placeholder", t().photoPlaceholder));
      }

      var top = el("div", "st4-team-card__top");
      top.appendChild(el("span", "st4-team-card__pos", "#" + team.position));
      var nameWrap = el("div", "st4-team-card__name-wrap");
      nameWrap.appendChild(el("span", "st4-team-card__name", team.team));
      var badge = highlighted ? vehicleBadge(team.vehicle) : null;
      if (badge) nameWrap.appendChild(badge);
      top.appendChild(nameWrap);
      card.appendChild(top);

      card.appendChild(el("div", "st4-team-card__car", team.car + " · #" + team.car_no));

      if (team.points !== null && team.points !== undefined) {
        card.appendChild(el("div", "st4-team-card__points", team.points + t().rosterPointsUnit));
      } else {
        card.appendChild(el("div", "st4-team-card__points", t().rosterNoData));
      }

      if (team.description) {
        card.appendChild(el("p", "st4-team-card__desc", pick(team.description)));
        if (team.verified === "web_search_only") {
          card.appendChild(el("span", "st4-team-card__unverified", t().rosterUnverified));
        }
      }

      var drivers = team.drivers || [];
      if (drivers.length > 0) {
        var driverWrap = el("div", "st4-team-card__drivers");
        drivers.forEach(function (d) {
          driverWrap.appendChild(el("span", "roster-chip", d.name));
        });
        card.appendChild(driverWrap);
      }

      grid.appendChild(card);
    });
    built.content.appendChild(grid);
    wrap.appendChild(built.details);
    return wrap;
  }

  function buildSeriesCard(s) {
    var card = el("div", "series-card series-card--" + s.key);
    var header = el("div", "series-card__header");
    header.appendChild(el("span", null, t().series[s.key] || s.label));
    if (s.vehicle && VEHICLE_KEYS.indexOf(s.vehicle) !== -1) {
      header.appendChild(el("span", "series-card__header-vehicle", t().vehicleFilter[s.vehicle]));
    }
    card.appendChild(header);
    if (s.roster !== null && s.roster !== undefined) {
      card.appendChild(buildRosterBlock(s));
    }
    card.appendChild(buildScheduleBlock(s));
    card.appendChild(buildRankingBlock(s));
    card.appendChild(buildSubGroup(t().topicsHeading, s.topics));
    card.appendChild(buildSubGroup(t().resultsHeading, s.results));
    card.appendChild(buildSubGroup(t().standingsNewsHeading, s.standings));

    var link = el("a", "series-card__link", t().standingsSearchLink);
    link.href = s.standings_search_url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    card.appendChild(link);

    return card;
  }

  function buildMotorsportsPanel(icon, section) {
    var panel = el("section", "panel panel--full");
    var regions = section.regions || {};
    var seriesCount = Object.values(regions).reduce(function (sum, region) {
      return sum + region.series.reduce(function (s2, s) { return s2 + s.topics.length + s.results.length + s.standings.length; }, 0);
    }, 0);
    panel.appendChild(buildPanelHeader(icon, t().sections.motorsports || section.label, seriesCount));
    if (section.note) panel.appendChild(el("p", "panel__note", section.note));

    Object.keys(regions).forEach(function (regionKey) {
      var region = regions[regionKey];
      var regionWrap = el("div", "motorsports-region");
      var title = el("div", "motorsports-region__title");
      title.appendChild(document.createTextNode((region.flag || "") + " " + (t().regions[regionKey] || region.label)));
      regionWrap.appendChild(title);

      var grid = el("div", "motorsports");
      region.series.forEach(function (s) {
        grid.appendChild(buildSeriesCard(s));
      });
      regionWrap.appendChild(grid);
      panel.appendChild(regionWrap);
    });

    return panel;
  }

  function buildFormatCard(series) {
    var card = el("div", "format-card");

    if (series.region) {
      var regionRow = el("div", "format-card__region");
      regionRow.appendChild(el("span", "format-card__region-flag", series.region.flag || ""));
      regionRow.appendChild(el("span", "format-card__region-name", pick(series.region.name)));
      card.appendChild(regionRow);
    }

    card.appendChild(el("div", "format-card__title", t().series[series.key] || pick(series.series_label)));

    var confidence = series.confidence || "unavailable";
    card.appendChild(
      el("span", "format-card__confidence format-card__confidence--" + confidence, t().formatsConfidence[confidence] || confidence)
    );

    if (confidence === "unavailable" || !series.sections) {
      card.appendChild(el("p", "format-card__unavailable", t().formatsUnavailable));
      return card;
    }

    var rowKeys = ["eligibility", "points", "weekend_format", "classification", "season_length"];
    rowKeys.forEach(function (key) {
      var value = series.sections[key];
      if (!value) return;
      var row = el("div", "format-card__row");
      row.appendChild(el("span", "format-card__row-label", t().formatsRows[key]));
      row.appendChild(el("span", "format-card__row-value", pick(value)));
      card.appendChild(row);
    });

    if (series.sources && series.sources.length > 0) {
      var srcWrap = el("div", "format-card__sources");
      srcWrap.appendChild(document.createTextNode(t().formatsSourcesLabel));
      series.sources.forEach(function (src, idx) {
        if (idx > 0) srcWrap.appendChild(document.createTextNode(" / "));
        var a = el("a", null, src.label || src.url);
        a.href = src.url;
        a.target = "_blank";
        a.rel = "noopener noreferrer";
        srcWrap.appendChild(a);
      });
      card.appendChild(srcWrap);
    }
    if (series.primary_source_note) {
      card.appendChild(el("p", "format-card__sources", pick(series.primary_source_note)));
    }

    return card;
  }

  function buildMotorsportsFormatsPanel(icon, formatsData) {
    var panel = el("section", "panel panel--full");
    if (!formatsData || !formatsData.series) {
      panel.appendChild(buildPanelHeader(icon, t().sections.motorsports_formats, 0));
      panel.appendChild(el("p", "panel__empty", t().panelEmpty));
      return panel;
    }
    var series = formatsData.series || [];
    panel.appendChild(buildPanelHeader(icon, t().sections.motorsports_formats, series.length));
    if (formatsData.note) panel.appendChild(el("p", "panel__note", pick(formatsData.note)));

    var grid = el("div", "formats-grid");
    series.forEach(function (s) {
      grid.appendChild(buildFormatCard(s));
    });
    panel.appendChild(grid);
    return panel;
  }

  var RIVALS_VEHICLE_KEYS = ["gr86", "brz", "mx5"];
  var RIVALS_MARKET_KEYS = ["jp", "us", "au"];

  function formatMoney(amount, symbol) {
    return symbol + amount.toLocaleString(currentLang === "ja" ? "ja-JP" : "en-US");
  }

  function vehiclePriceRange(rivalsData, vehicleKey, marketKey) {
    var marketData = rivalsData.vehicles[vehicleKey] && rivalsData.vehicles[vehicleKey].markets[marketKey];
    if (!marketData || !marketData.grades || marketData.grades.length === 0) return null;
    var prices = marketData.grades.map(function (g) { return g.price; });
    return { min: Math.min.apply(null, prices), max: Math.max.apply(null, prices) };
  }

  /** Horizontal price-range bars (min grade price -> max grade price) for GR86/BRZ/MX-5
   * within one market/currency, positioned on a shared scale so relative pricing reads
   * at a glance. Simple CSS bars — no charting library needed for 3 rows. */
  function buildPriceBars(rivalsData, marketKey) {
    var marketMeta = rivalsData.markets[marketKey];
    if (!marketMeta) return null;

    var ranges = {};
    var allPrices = [];
    RIVALS_VEHICLE_KEYS.forEach(function (vk) {
      var r = vehiclePriceRange(rivalsData, vk, marketKey);
      if (!r) return;
      ranges[vk] = r;
      allPrices.push(r.min, r.max);
    });
    if (allPrices.length === 0) return null;

    var globalMin = Math.min.apply(null, allPrices);
    var globalMax = Math.max.apply(null, allPrices);
    var span = globalMax - globalMin || 1;

    var wrap = el("div", "price-bars");
    wrap.appendChild(el("div", "price-bars__title", pick(marketMeta.label) + " (" + marketMeta.currency + ")"));

    RIVALS_VEHICLE_KEYS.forEach(function (vk) {
      var r = ranges[vk];
      if (!r) return;
      var row = el("div", "price-bar-row");
      row.appendChild(el("span", "price-bar-row__label vehicle-badge vehicle-badge--" + vk, t().vehicleFilter[vk]));
      var track = el("div", "price-bar-row__track");
      var fill = el("div", "price-bar-row__fill price-bar-row__fill--" + vk);
      var leftPct = (100 * (r.min - globalMin)) / span;
      var widthPct = Math.max(2, (100 * (r.max - r.min)) / span);
      fill.style.left = leftPct + "%";
      fill.style.width = widthPct + "%";
      track.appendChild(fill);
      row.appendChild(track);
      row.appendChild(el("span", "price-bar-row__value", formatMoney(r.min, marketMeta.symbol) + " – " + formatMoney(r.max, marketMeta.symbol)));
      wrap.appendChild(row);
    });

    return wrap;
  }

  function buildGradeTable(vehicleKey, marketData, marketMeta) {
    var wrap = el("div", "grade-table");
    var header = el("div", "grade-table__header");
    header.appendChild(el("span", "vehicle-badge vehicle-badge--" + vehicleKey, t().vehicleFilter[vehicleKey]));
    if (marketData.confirmed && t().rivalsConfirmed[marketData.confirmed]) {
      header.appendChild(el("span", "grade-table__confidence grade-table__confidence--" + marketData.confirmed, t().rivalsConfirmed[marketData.confirmed]));
    }
    wrap.appendChild(header);

    var list = el("ul", "grade-list");
    (marketData.grades || []).forEach(function (g) {
      var li = el("li", "grade-list__item" + (g.confirmed === false ? " grade-list__item--unconfirmed" : ""));
      var nameWrap = el("span", "grade-list__name", g.name + (g.transmission ? " · " + g.transmission : ""));
      li.appendChild(nameWrap);
      li.appendChild(el("span", "grade-list__price", formatMoney(g.price, marketMeta.symbol)));
      list.appendChild(li);
      if (g.confirmed === false && g.notes) {
        var noteLi = el("li", "grade-list__note");
        noteLi.textContent = pick(g.notes);
        list.appendChild(noteLi);
      }
    });
    wrap.appendChild(list);

    if (marketData.price_basis_note) {
      wrap.appendChild(el("p", "panel__note grade-table__basis-note", pick(marketData.price_basis_note)));
    }
    if (marketData.source) {
      var srcLink = el("a", "grade-table__source", t().rivalsSourceLabel + marketData.source.label);
      srcLink.href = marketData.source.url;
      srcLink.target = "_blank";
      srcLink.rel = "noopener noreferrer";
      wrap.appendChild(srcLink);
    }
    return wrap;
  }

  function buildRivalsPanel(icon, rivalsData) {
    var panel = el("section", "panel panel--full");
    if (!rivalsData || !rivalsData.vehicles) {
      panel.appendChild(buildPanelHeader(icon, t().sections.rivals, 0));
      panel.appendChild(el("p", "panel__empty", t().panelEmpty));
      return panel;
    }
    panel.appendChild(buildPanelHeader(icon, t().sections.rivals, RIVALS_VEHICLE_KEYS.length));
    if (rivalsData.note) panel.appendChild(el("p", "panel__note", pick(rivalsData.note)));

    var barsHeading = el("div", "series-card__group-title", t().rivalsPriceBarTitle);
    barsHeading.style.padding = "14px 20px 4px";
    panel.appendChild(barsHeading);
    var barsWrap = el("div", "price-bars-group");
    RIVALS_MARKET_KEYS.forEach(function (mkt) {
      var bars = buildPriceBars(rivalsData, mkt);
      if (bars) barsWrap.appendChild(bars);
    });
    panel.appendChild(barsWrap);

    var grid = el("div", "rivals-grid");
    RIVALS_MARKET_KEYS.forEach(function (mkt) {
      var marketMeta = rivalsData.markets[mkt];
      if (!marketMeta) return;
      var marketSection = el("div", "rivals-market");
      marketSection.appendChild(el("div", "rivals-market__title", pick(marketMeta.label)));
      RIVALS_VEHICLE_KEYS.forEach(function (vk) {
        var marketData = rivalsData.vehicles[vk] && rivalsData.vehicles[vk].markets[mkt];
        if (!marketData) return;
        marketSection.appendChild(buildGradeTable(vk, marketData, marketMeta));
      });
      grid.appendChild(marketSection);
    });
    panel.appendChild(grid);
    return panel;
  }

  /** Every item tracked anywhere on the board, for the stat strip's total count. */
  function collectAllTrackedItems(data) {
    var all = [];
    ["news_reviews", "social_buzz", "complaints", "events"].forEach(function (key) {
      var section = data.sections[key];
      if (section && section.items) all = all.concat(section.items);
    });
    var yt = data.sections.youtube;
    if (yt) {
      ["global", "jp"].forEach(function (grp) {
        if (yt[grp]) all = all.concat(yt[grp].popular || [], yt[grp].new || []);
      });
    }
    var ms = data.sections.motorsports;
    if (ms && ms.regions) {
      Object.values(ms.regions).forEach(function (region) {
        region.series.forEach(function (s) {
          all = all.concat(s.topics, s.results, s.standings);
        });
      });
    }
    return all;
  }

  function buildStats(data) {
    statsEl.innerHTML = "";

    var allItems = collectAllTrackedItems(data);
    var totalCount = allItems.length;
    // Official-release copy is corporate boilerplate, not organic sentiment — excluded
    // from the breakdown below (but still counted in the total above).
    var sentimentItems = allItems.filter(function (it) { return it.kind !== "official_news"; });

    var counts = { positive: 0, neutral: 0, negative: 0 };
    sentimentItems.forEach(function (item) {
      var label = item.sentiment ? item.sentiment.label : "neutral";
      counts[label] = (counts[label] || 0) + 1;
    });

    var youtubeCount = 0;
    var yt = data.sections.youtube;
    if (yt) {
      ["global", "jp"].forEach(function (grp) {
        if (yt[grp]) youtubeCount += (yt[grp].popular || []).length + (yt[grp].new || []).length;
      });
    }

    var motorsportsCount = 0;
    if (data.sections.motorsports && data.sections.motorsports.regions) {
      Object.values(data.sections.motorsports.regions).forEach(function (region) {
        region.series.forEach(function (s) {
          motorsportsCount += s.topics.length + s.results.length + s.standings.length;
        });
      });
    }

    var t1 = el("div", "stat-tile");
    t1.appendChild(el("div", "stat-tile__label", t().statTotal));
    var v1 = el("div", "stat-tile__value", String(totalCount));
    if (t().unitCount) v1.appendChild(el("small", null, t().unitCount));
    t1.appendChild(v1);
    statsEl.appendChild(t1);

    var t2 = el("div", "stat-tile");
    t2.appendChild(el("div", "stat-tile__label", t().statSentiment));
    var v2 = el("div", "stat-tile__value", String(counts.positive));
    v2.appendChild(el("small", null, t().statSentimentUnit));
    t2.appendChild(v2);
    var total = counts.positive + counts.neutral + counts.negative || 1;
    var bar = el("div", "sentiment-bar");
    bar.appendChild(el("div", "sentiment-bar__seg sentiment-bar__seg--positive")).style.width = (100 * counts.positive / total) + "%";
    bar.appendChild(el("div", "sentiment-bar__seg sentiment-bar__seg--neutral")).style.width = (100 * counts.neutral / total) + "%";
    bar.appendChild(el("div", "sentiment-bar__seg sentiment-bar__seg--negative")).style.width = (100 * counts.negative / total) + "%";
    t2.appendChild(bar);
    var legend = el("div", "sentiment-legend");
    var lp = el("span"); lp.appendChild(el("span", "legend-dot legend-dot--positive")); lp.appendChild(document.createTextNode(counts.positive + ""));
    var ln = el("span"); ln.appendChild(el("span", "legend-dot legend-dot--neutral")); ln.appendChild(document.createTextNode(counts.neutral + ""));
    var lg = el("span"); lg.appendChild(el("span", "legend-dot legend-dot--negative")); lg.appendChild(document.createTextNode(counts.negative + ""));
    legend.appendChild(lp); legend.appendChild(ln); legend.appendChild(lg);
    t2.appendChild(legend);
    statsEl.appendChild(t2);

    var t3 = el("div", "stat-tile");
    t3.appendChild(el("div", "stat-tile__label", t().statYoutube));
    var v3 = el("div", "stat-tile__value", String(youtubeCount));
    if (t().unitVideos) v3.appendChild(el("small", null, t().unitVideos));
    t3.appendChild(v3);
    statsEl.appendChild(t3);

    var t4 = el("div", "stat-tile");
    t4.appendChild(el("div", "stat-tile__label", t().statMotorsports));
    var v4 = el("div", "stat-tile__value", String(motorsportsCount));
    if (t().unitCount) v4.appendChild(el("small", null, t().unitCount));
    t4.appendChild(v4);
    statsEl.appendChild(t4);
  }

  function buildLangToggle() {
    var btns = langToggleEl.querySelectorAll(".lang-toggle__btn");
    btns.forEach(function (btn) {
      btn.classList.toggle("is-active", btn.dataset.lang === currentLang);
      btn.onclick = function () {
        currentLang = btn.dataset.lang;
        setLang(currentLang);
        render(lastData, lastRivals, lastFormats);
      };
    });
  }

  function render(data, rivalsData, formatsData) {
    lastData = data;
    lastRivals = rivalsData;
    lastFormats = formatsData;

    document.getElementById("eyebrow-text").textContent = t().eyebrow;
    document.getElementById("chip-cadence").textContent = t().cadenceChip;
    document.getElementById("chip-label").textContent = t().cadenceLabel;
    document.documentElement.lang = currentLang;

    buildLangToggle();
    buildStats(data);

    board.innerHTML = "";
    LAYOUT.forEach(function (entry) {
      if (entry.key === "rivals") {
        board.appendChild(buildRivalsPanel(entry.icon, rivalsData));
        return;
      }
      if (entry.key === "motorsports_formats") {
        board.appendChild(buildMotorsportsFormatsPanel(entry.icon, formatsData));
        return;
      }
      var section = data.sections && data.sections[entry.key];
      if (!section) return;
      var panel;
      if (entry.key === "motorsports") {
        panel = buildMotorsportsPanel(entry.icon, section);
      } else if (entry.key === "news_reviews") {
        panel = buildNewsReviewsPanel(entry.icon, section);
      } else if (entry.key === "youtube") {
        panel = buildYoutubePanel(entry.icon, section);
      } else if (entry.key === "complaints" || entry.key === "social_buzz") {
        panel = buildTabbedPanel(entry.icon, entry.key, section);
      } else {
        panel = buildGenericPanel(entry.icon, entry.key, section, entry.size);
      }
      board.appendChild(panel);
    });

    lastUpdatedEl.textContent = t().lastUpdatedPrefix + (data.generated_at_jst || t().lastUpdatedUnknown);

    var generatedAt = data.generated_at_utc ? new Date(data.generated_at_utc) : null;
    if (generatedAt) {
      // 30分おき更新なので、90分(3サイクル分)を超えて更新が止まっていたら注意表示にする
      var minutesSince = (Date.now() - generatedAt.getTime()) / 6e4;
      statusDot.classList.toggle("is-stale", minutesSince > 90);
    }
  }

  function renderError(message) {
    statsEl.innerHTML = "";
    board.innerHTML = "";
    board.appendChild(el("p", "board__error", message));
    lastUpdatedEl.textContent = t().lastUpdatedUnknown;
    statusDot.classList.add("is-error");
  }

  document.getElementById("footer-text").textContent = t().footer;

  Promise.all([
    fetch("data/latest.json", { cache: "no-store" }).then(function (res) {
      if (!res.ok) throw new Error("HTTP " + res.status + " (latest.json)");
      return res.json();
    }),
    fetch("data/rivals.json", { cache: "no-store" })
      .then(function (res) {
        if (!res.ok) throw new Error("HTTP " + res.status + " (rivals.json)");
        return res.json();
      })
      .catch(function () {
        return null; // static, non-critical catalog — degrade gracefully
      }),
    fetch("data/motorsports_formats.json", { cache: "no-store" })
      .then(function (res) {
        if (!res.ok) throw new Error("HTTP " + res.status + " (motorsports_formats.json)");
        return res.json();
      })
      .catch(function () {
        return null; // static, non-critical catalog — degrade gracefully
      }),
  ])
    .then(function (results) {
      render(results[0], results[1], results[2]);
      document.getElementById("footer-text").textContent = t().footer;
    })
    .catch(function (err) {
      renderError(
        (currentLang === "ja" ? "ダッシュボードデータの読み込みに失敗しました(" : "Failed to load dashboard data (") +
          err.message +
          ")。"
      );
    });
})();
