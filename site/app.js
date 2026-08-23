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
      rosterRoundsNote: function (done, total) {
        return "今シーズン第" + done + "戦(全" + total + "戦)まで開催済みのエントリーリストを集計。";
      },
      rosterPositionUnit: "位",
      rosterPointsUnit: "pt",
      rosterNoData: "順位データなし",
      rosterOfficialLink: "公式チームページ ↗",
      rosterUnverified: "一次資料未裏取り",
      rivalsUnconfirmed: "reference-only",
      rivalsSpecs: {
        price: "価格(参考)",
        engine: "エンジン",
        power: "馬力",
        torque: "トルク",
        zeroToSixty: "0-60mph",
        drivetrain: "駆動方式",
        transmission: "トランスミッション",
        weight: "車重",
      },
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
        news_reviews_gr86: "GR86 公式リリース & メディア評価",
        news_reviews_other: "BRZ / ロードスター(MX-5) 公式リリース & メディア評価",
        youtube: "YouTube",
        social_buzz: "SNSでの話題",
        complaints: "お客様の声・クレーム関連情報",
        events: "世界各地のイベント情報",
        motorsports: "モータースポーツ(GR Cup ほか)",
        motorsports_formats: "各シリーズの競技フォーマット解説",
        gr_cup_roster: "Toyota GR Cup 参戦チーム名簿(北米)",
        rivals: "ライバル車 スペック比較",
      },
      regions: {
        north_america: "北米",
        japan_asia: "日本・アジア",
        australia: "オーストラリア",
        mx5_cup: "ロードスター(MX-5)ワンメイク",
      },
      series: {
        gr_cup: "Toyota GR Cup(GR86 Cup Edition ワンメイクレース)",
        tgr_86brz_cup: "TGR GR86/BRZ Cup(スーパーGT併催・日本)",
        gr_cup_australia: "GR Cup Australia(旧Toyota 86 Racing Series)",
        mx5_cup: "Mazda MX-5 Cup(IMSA主催・北米)",
      },
      footer:
        "本ダッシュボードは公開情報源(Googleニュース検索・YouTube検索結果・各シリーズ公式サイト)を自動集計した非公式のモニタリングツールです。" +
        "トヨタ自動車・SUBARU・マツダの公式発表とは異なる場合があります。X/Facebook/Instagramの投稿本体、および社内クレームシステムのデータは含まれません。" +
        "ポジティブ/ネガティブ表示は見出し文のみに基づく自動推定(簡易辞書・VADER)であり、参考値です。ライバル車スペック・GR Cup参戦チーム背景・モータースポーツ" +
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
      rosterRoundsNote: function (done, total) {
        return "Aggregated from entry lists through round " + done + " of " + total + " completed so far this season.";
      },
      rosterPositionUnit: "",
      rosterPointsUnit: "pt",
      rosterNoData: "No standings data",
      rosterOfficialLink: "Official team page ↗",
      rosterUnverified: "not independently verified",
      rivalsUnconfirmed: "reference-only",
      rivalsSpecs: {
        price: "Price (from)",
        engine: "Engine",
        power: "Power",
        torque: "Torque",
        zeroToSixty: "0-60 mph",
        drivetrain: "Drivetrain",
        transmission: "Transmission",
        weight: "Curb weight",
      },
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
        news_reviews_gr86: "GR86 Official Releases & Media Reviews",
        news_reviews_other: "BRZ / MX-5 (Roadster) Official Releases & Media Reviews",
        youtube: "YouTube",
        social_buzz: "Social Buzz",
        complaints: "Complaints / Owner Feedback",
        events: "Events Worldwide",
        motorsports: "Motorsports (GR Cup and others)",
        motorsports_formats: "Series Format Explainers",
        gr_cup_roster: "Toyota GR Cup Team Roster (North America)",
        rivals: "Rival Vehicle Spec Comparison",
      },
      regions: {
        north_america: "North America",
        japan_asia: "Japan / Asia",
        australia: "Australia",
        mx5_cup: "MX-5 (Roadster) One-Make",
      },
      series: {
        gr_cup: "Toyota GR Cup (GR86 Cup Edition one-make series)",
        tgr_86brz_cup: "TGR GR86/BRZ Cup (Super GT support race, Japan)",
        gr_cup_australia: "GR Cup Australia (formerly Toyota 86 Racing Series)",
        mx5_cup: "Mazda MX-5 Cup (IMSA-sanctioned, North America)",
      },
      footer:
        "This dashboard is an unofficial monitoring tool that auto-aggregates public sources (Google News search, YouTube search results, official series sites). " +
        "It may differ from official Toyota, Subaru, or Mazda communications. It does not include raw X/Facebook/Instagram posts or internal complaint-system data. " +
        "Positive/negative labels are automated headline-only estimates (a simple lexicon plus VADER) and should be treated as reference only. Rival vehicle specs, " +
        "GR Cup team background, and motorsports format explainers are hand-researched static data, not part of the 30-minute auto-refresh. Toyota 86 (GT86/FT86) " +
        "is tracked in YouTube/social buzz only (a discontinued model, so it's excluded from official news/reviews/complaints).",
    },
  };

  var LANG_KEY = "gr86watch_lang";
  var VEHICLE_KEY = "gr86watch_vehicle_filter";
  var VEHICLE_KEYS = ["gr86", "toyota86", "brz", "mx5"];

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
  function getVehicleFilter() {
    try {
      var saved = localStorage.getItem(VEHICLE_KEY);
      if (saved === "all" || VEHICLE_KEYS.indexOf(saved) !== -1) return saved;
    } catch (e) {}
    return "all";
  }
  function setVehicleFilter(v) {
    try { localStorage.setItem(VEHICLE_KEY, v); } catch (e) {}
  }

  var currentLang = getLang();
  var currentVehicle = getVehicleFilter();

  function t() {
    return I18N[currentLang] || I18N.ja;
  }

  /** Resolves a bilingual JSON field ({ja,en}) from the static catalogs (rivals.json,
   * gr_cup_roster team descriptions, motorsports_formats.json). Plain strings (proper
   * nouns) pass through as-is. */
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
    users:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="M17 20v-1.5a3.5 3.5 0 0 0-3.5-3.5h-4A3.5 3.5 0 0 0 6 18.5V20"/><circle cx="11" cy="7.5" r="3.5"/>' +
      '<path d="M20.5 20v-1.2a3 3 0 0 0-2-2.8"/><path d="M15.5 4.2a3.5 3.5 0 0 1 0 6.6"/></svg>',
    scale:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="M12 3v18"/><path d="M5 8l-3 6a3 3 0 0 0 6 0z"/><path d="M19 8l-3 6a3 3 0 0 0 6 0z"/><path d="M3 8h18"/><path d="M8 21h8"/></svg>',
    book:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
  };

  /* ---------------------------------------------------------------------
   * New section order (2026-08 restructure):
   *   1. GR86 news+reviews combined  2. BRZ/MX-5 news+reviews combined
   *   3. YouTube (4 vehicles)        4. Social buzz (4 vehicles)
   *   5. Complaints (3 vehicles)     6. Events
   *   7. Motorsports -> format explainers -> GR Cup roster -> rivals
   * ------------------------------------------------------------------- */
  var LAYOUT = [
    { key: "news_reviews_gr86", size: "full", icon: "doc" },
    { key: "news_reviews_other", size: "full", icon: "doc" },
    { key: "youtube", size: "full", icon: "play" },
    { key: "social_buzz", size: "full", icon: "chat" },
    { key: "complaints", size: "full", icon: "alert" },
    { key: "events", size: "full", icon: "calendar" },
    { key: "motorsports", size: "full", icon: "flag" },
    { key: "motorsports_formats", size: "full", icon: "book" },
    { key: "gr_cup_roster", size: "full", icon: "users" },
    { key: "rivals", size: "full", icon: "scale" },
  ];

  var board = document.getElementById("board");
  var statsEl = document.getElementById("stats");
  var lastUpdatedEl = document.getElementById("last-updated");
  var statusDot = document.getElementById("status-dot");
  var vehicleFilterEl = document.getElementById("vehicle-filter");
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

  function applyVehicleFilterToList(listEl) {
    var lis = listEl.querySelectorAll("li");
    var visibleCount = 0;
    lis.forEach(function (li) {
      var a = li.querySelector(".item");
      var veh = a ? a.dataset.vehicle : null;
      var show = currentVehicle === "all" || !veh || veh === currentVehicle;
      li.style.display = show ? "" : "none";
      if (show) visibleCount++;
    });
    return visibleCount;
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
    var list = buildList(items);
    panel.appendChild(list);
    applyVehicleFilterToList(list);
    return panel;
  }

  /** Shared "latest / trending" tabbed panel — used by complaints and social_buzz,
   * which both provide {items (latest), items_buzz (trending), note}. */
  function buildTabbedPanel(icon, sectionKey, section) {
    var panel = el("section", "panel panel--full");
    var latestItems = section.items || [];
    var buzzItems = section.items_buzz || [];
    panel.appendChild(buildPanelHeader(icon, t().sections[sectionKey] || section.label, latestItems.length));
    if (section.note) panel.appendChild(el("p", "panel__note", section.note));

    var tabs = el("div", "tab-group");
    var tabLatest = el("button", "tab-group__btn is-active", t().tabLatest);
    var tabBuzz = el("button", "tab-group__btn", t().tabBuzz);
    tabs.appendChild(tabLatest);
    tabs.appendChild(tabBuzz);
    panel.appendChild(tabs);

    var listWrap = el("div");
    function renderList(items) {
      listWrap.innerHTML = "";
      if (items.length === 0) {
        listWrap.appendChild(el("p", "panel__empty", t().panelEmpty));
      } else {
        var list = buildList(items);
        listWrap.appendChild(list);
        applyVehicleFilterToList(list);
      }
    }
    renderList(latestItems);
    panel.appendChild(listWrap);

    tabLatest.addEventListener("click", function () {
      tabLatest.classList.add("is-active");
      tabBuzz.classList.remove("is-active");
      renderList(latestItems);
    });
    tabBuzz.addEventListener("click", function () {
      tabBuzz.classList.add("is-active");
      tabLatest.classList.remove("is-active");
      renderList(buzzItems);
    });

    return panel;
  }

  function buildSubGroup(title, items) {
    var group = el("div", "series-card__group");
    group.appendChild(el("div", "series-card__group-title", title));
    if (items.length === 0) {
      group.appendChild(el("p", "panel__empty", t().seriesEmpty));
    } else {
      var list = buildList(items);
      group.appendChild(list);
      applyVehicleFilterToList(list);
    }
    return group;
  }

  /** YouTube panel: Trending(popular)/Latest(new) tabs, each split into Global/Japanese
   * sub-groups, covering all 4 vehicles (GR86/Toyota86/BRZ/MX-5). */
  function buildYoutubePanel(icon, section) {
    var panel = el("section", "panel panel--full");
    var global = section.global || { popular: [], new: [] };
    var jp = section.jp || { popular: [], new: [] };
    var totalCount = global.popular.length + global.new.length + jp.popular.length + jp.new.length;
    panel.appendChild(buildPanelHeader(icon, t().sections.youtube || section.label, totalCount));

    var tabs = el("div", "tab-group");
    var tabTrending = el("button", "tab-group__btn is-active", t().tabBuzz);
    var tabLatest = el("button", "tab-group__btn", t().tabLatest);
    tabs.appendChild(tabTrending);
    tabs.appendChild(tabLatest);
    panel.appendChild(tabs);

    var listWrap = el("div");
    function renderGroups(globalItems, jpItems) {
      listWrap.innerHTML = "";
      listWrap.appendChild(buildSubGroup(t().youtubeGlobalLabel, globalItems));
      listWrap.appendChild(buildSubGroup(t().youtubeJpLabel, jpItems));
    }
    renderGroups(global.popular, jp.popular);
    panel.appendChild(listWrap);

    tabTrending.addEventListener("click", function () {
      tabTrending.classList.add("is-active");
      tabLatest.classList.remove("is-active");
      renderGroups(global.popular, jp.popular);
    });
    tabLatest.addEventListener("click", function () {
      tabLatest.classList.add("is-active");
      tabTrending.classList.remove("is-active");
      renderGroups(global.new, jp.new);
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

  function buildScheduleBlock(s) {
    var wrap = el("div", "series-card__group");
    wrap.appendChild(el("div", "series-card__group-title", t().scheduleHeading));

    if (!s.has_real_schedule) {
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
      wrap.appendChild(el("p", "panel__empty", t().scheduleUnavailable));
      return wrap;
    }

    var nextRace = rounds.filter(function (r) { return r.status === "upcoming"; })[0];
    if (nextRace) {
      var next = el("div", "schedule-next");
      next.appendChild(el("span", "schedule-next__label", t().scheduleNext));
      next.appendChild(el("span", "schedule-next__date", nextRace.date_range));
      next.appendChild(
        el("span", "schedule-next__track", [nextRace.round, nextRace.name, nextRace.track].filter(Boolean).join(" · "))
      );
      wrap.appendChild(next);
    }

    var list = el("ul", "schedule-list");
    rounds.forEach(function (r) {
      var li = el("li", "schedule-list__item schedule-list__item--" + r.status);
      li.appendChild(el("span", "schedule-list__dot"));
      li.appendChild(el("span", "schedule-list__date", r.date_range));
      li.appendChild(el("span", "schedule-list__label", [r.round, r.name, r.track].filter(Boolean).join(" · ")));
      list.appendChild(li);
    });
    wrap.appendChild(list);

    return wrap;
  }

  function buildRankingBlock(s) {
    var wrap = el("div", "series-card__group");
    wrap.appendChild(el("div", "series-card__group-title", t().rankingHeading));
    if (s.standings_chart && s.standings_chart.length > 0) {
      wrap.appendChild(buildStandingsChart(s.standings_chart));
    }
    if (s.standings_chart_note) {
      wrap.appendChild(el("p", "panel__note series-card__chart-note", s.standings_chart_note));
    }
    if (s.driver_standings_chart && s.driver_standings_chart.length > 0) {
      wrap.appendChild(el("div", "series-card__group-title", t().rankingDriversHeading));
      wrap.appendChild(buildStandingsChart(s.driver_standings_chart));
    }
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

  function buildRosterCard(team) {
    var card = el("div", "roster-card");
    var top = el("div", "roster-card__top");
    var nameWrap = el("div");
    nameWrap.appendChild(el("div", "roster-card__name", team.name));
    if (team.points !== null && team.points !== undefined) {
      nameWrap.appendChild(el("div", "roster-card__points", team.points + t().rosterPointsUnit));
    } else {
      nameWrap.appendChild(el("div", "roster-card__points", t().rosterNoData));
    }
    top.appendChild(nameWrap);
    if (team.position) {
      top.appendChild(el("div", "roster-card__pos", "#" + team.position));
    }
    card.appendChild(top);

    if (team.verified === "web_search_only") {
      card.appendChild(el("span", "roster-card__badge", t().rosterUnverified));
    }

    card.appendChild(el("p", "roster-card__desc", pick(team.description)));

    var drivers = team.drivers || [];
    if (drivers.length > 0) {
      var driverWrap = el("div", "roster-card__drivers");
      drivers.forEach(function (d) {
        driverWrap.appendChild(el("span", "roster-chip", d.name + (d.car_no ? " #" + d.car_no : "")));
      });
      card.appendChild(driverWrap);
    }

    if (team.official_url) {
      var link = el("a", "roster-card__link", t().rosterOfficialLink);
      link.href = team.official_url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      card.appendChild(link);
    }

    return card;
  }

  function buildRosterPanel(icon, section) {
    var panel = el("section", "panel panel--full");
    var teams = section.teams || [];
    panel.appendChild(buildPanelHeader(icon, t().sections.gr_cup_roster || section.label, teams.length));

    var note = section.note || "";
    if (section.rounds_completed !== undefined) {
      note = t().rosterRoundsNote(section.rounds_completed, section.rounds_total) + " " + note;
    }
    if (note) panel.appendChild(el("p", "panel__note", note));

    if (teams.length === 0) {
      panel.appendChild(el("p", "panel__empty", t().panelEmpty));
      return panel;
    }

    var grid = el("div", "roster-grid");
    teams.forEach(function (team) {
      grid.appendChild(buildRosterCard(team));
    });
    panel.appendChild(grid);
    return panel;
  }

  function buildRivalCard(rival) {
    var card = el("div", "rival-card");
    card.appendChild(el("div", "rival-card__make", pick(rival.make)));
    card.appendChild(el("div", "rival-card__model", pick(rival.model) + (rival.year ? " (" + rival.year + ")" : "")));

    var specs = el("div", "rival-card__specs");
    function addSpec(label, value, note) {
      if (value === null || value === undefined || value === "") return;
      specs.appendChild(el("span", "rival-card__spec-label", label));
      var v = el("span", "rival-card__spec-value", String(value));
      specs.appendChild(v);
      if (note) {
        specs.appendChild(el("span", "rival-card__spec-label"));
        specs.appendChild(el("span", "rival-card__spec-value rival-card__unconfirmed", pick(note)));
      }
    }
    var S = t().rivalsSpecs;
    addSpec(S.price, rival.price_usd_from ? "$" + rival.price_usd_from.toLocaleString(currentLang === "ja" ? "ja-JP" : "en-US") : null);
    addSpec(S.engine, pick(rival.engine));
    addSpec(S.power, rival.horsepower_hp ? rival.horsepower_hp + " hp" : null, rival.horsepower_note);
    addSpec(S.torque, rival.torque_lb_ft ? rival.torque_lb_ft + " lb-ft" : null);
    addSpec(S.zeroToSixty, rival.zero_to_60_sec ? rival.zero_to_60_sec + "s" : null, rival.zero_to_60_note);
    addSpec(S.drivetrain, rival.drivetrain);
    addSpec(S.transmission, pick(rival.transmission));
    addSpec(
      S.weight,
      rival.curb_weight_lb ? rival.curb_weight_lb.toLocaleString(currentLang === "ja" ? "ja-JP" : "en-US") + " lb" : null,
      rival.curb_weight_confirmed === false ? { ja: "(" + t().rivalsUnconfirmed + ")", en: "(" + t().rivalsUnconfirmed + ")" } : null
    );
    card.appendChild(specs);

    if (rival.why_rival) {
      card.appendChild(el("p", "rival-card__why", pick(rival.why_rival)));
    }
    return card;
  }

  function buildRivalsPanel(icon, rivalsData) {
    var panel = el("section", "panel panel--full");
    if (!rivalsData || !rivalsData.rivals) {
      panel.appendChild(buildPanelHeader(icon, t().sections.rivals, 0));
      panel.appendChild(el("p", "panel__empty", t().panelEmpty));
      return panel;
    }
    var rivals = rivalsData.rivals || [];
    panel.appendChild(buildPanelHeader(icon, t().sections.rivals, rivals.length));
    if (rivalsData.note) panel.appendChild(el("p", "panel__note", pick(rivalsData.note)));

    var grid = el("div", "rivals-grid");
    rivals.forEach(function (rival) {
      grid.appendChild(buildRivalCard(rival));
    });
    panel.appendChild(grid);
    return panel;
  }

  function collectSentimentItems(data) {
    var all = [];
    ["news_reviews_gr86", "news_reviews_other", "social_buzz", "complaints", "events"].forEach(function (key) {
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

    var officialCount = ((data.sections.news_reviews_gr86 && data.sections.news_reviews_gr86.items) || []).length;
    var sentimentItems = collectSentimentItems(data);
    var totalCount = officialCount + sentimentItems.length;

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

  function buildVehicleFilter() {
    vehicleFilterEl.innerHTML = "";
    var options = ["all"].concat(VEHICLE_KEYS);
    options.forEach(function (v) {
      var btn = el("button", "vehicle-filter__btn" + (currentVehicle === v ? " is-active" : ""));
      btn.type = "button";
      btn.dataset.vehicle = v;
      if (v !== "all") {
        var dot = el("span", "vehicle-filter__dot");
        dot.style.color = "var(--veh-" + v + ")";
        btn.appendChild(dot);
      }
      btn.appendChild(document.createTextNode(t().vehicleFilter[v]));
      btn.addEventListener("click", function () {
        currentVehicle = v;
        setVehicleFilter(v);
        render(lastData, lastRivals, lastFormats);
      });
      vehicleFilterEl.appendChild(btn);
    });
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
    buildVehicleFilter();
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
      } else if (entry.key === "gr_cup_roster") {
        panel = buildRosterPanel(entry.icon, section);
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
