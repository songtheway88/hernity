# -*- coding: utf-8 -*-
"""
분양소식 게시판 정적 생성기.

  python3 tools/build_board.py

생성/갱신 대상:
  board/index.html, board/<slug>/index.html, sitemap.xml, rss.xml,
  index.html 의 <!-- BOARD:START --> ~ <!-- BOARD:END --> 최신글 블록
"""
import html
import json
import os
import re
from datetime import datetime, timezone, timedelta

from board_posts import POSTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.xn--q20b93bn3jn0if7fdzvexe.com"
SITE_NAME = "남성역 헤르니티"
TEL = "1844-0147"
KST = timezone(timedelta(hours=9))
ASSET_VER = "21"

PHONE_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="{cls}"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>'

NAV = [
    ("/#overview", "사업개요"),
    ("/#premium", "입지환경"),
    ("/#units", "타입안내"),
    ("/#development", "개발호재"),
    ("/board/", "분양소식"),
    ("/#contact", "관심고객등록"),
]

POSTS_SORTED = sorted(POSTS, key=lambda p: p["date"], reverse=True)
BY_SLUG = {p["slug"]: p for p in POSTS}


def esc(s):
    return html.escape(s, quote=True)


def post_url(p):
    return f"{SITE}/board/{p['slug']}/"


def fmt_date(d):
    return d.replace("-", ".")


def head(title, description, canonical, keywords="", og_image=f"{SITE}/img/og-image.jpg", og_type="website", ld=(), robots="index, follow"):
    ld_html = "\n".join(
        f'  <script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=2)}\n  </script>' for x in ld
    )
    kw = f'\n  <meta name="keywords" content="{esc(keywords)}">' if keywords else ""
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-YJTFFVD8ZL"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-YJTFFVD8ZL');
  </script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <meta name="theme-color" content="#ffffff">
  <meta name="robots" content="{robots}">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">{kw}
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" type="application/rss+xml" title="남성역 헤르니티 분양소식" href="{SITE}/rss.xml">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:image" content="{og_image}">
  <meta property="twitter:card" content="summary_large_image">
  <meta property="twitter:title" content="{esc(title)}">
  <meta property="twitter:description" content="{esc(description)}">
  <meta property="twitter:image" content="{og_image}">
  <link rel="icon" type="image/png" href="/favicon.png">
  <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css" />
  <link rel="stylesheet" href="/style.css?v={ASSET_VER}">
  <link rel="stylesheet" href="/board/board.css?v={ASSET_VER}1">
{ld_html}
</head>
<body class="board-page">
"""


def header():
    links = "\n".join(f'        <a href="{h}" class="nav-link{" highlight-menu" if t == "관심고객등록" else ""}">{t}</a>' for h, t in NAV)
    mlinks = "\n".join(f'        <a href="{h}" class="mobile-link">{t}</a>' for h, t in NAV)
    return f"""
  <header class="header scrolled" id="header">
    <div class="header-container">
      <a href="/" class="logo"><span class="gold-text">남성역</span> 헤르니티</a>
      <nav class="nav-menu">
{links}
      </nav>
      <div class="header-right">
        <a href="tel:{TEL}" class="phone-btn header-consult-btn">
          {PHONE_SVG.format(cls="phone-icon")}
          <span>{TEL} 지금 상담</span>
        </a>
        <button class="mobile-menu-btn" aria-label="메뉴 열기"><span></span><span></span><span></span></button>
      </div>
    </div>
  </header>

  <div class="mobile-overlay" id="mobile-overlay">
    <div class="mobile-menu-container">
      <nav class="mobile-nav">
{mlinks}
      </nav>
      <a href="tel:{TEL}" class="mobile-call-btn">
        {PHONE_SVG.format(cls="phone-icon")}
        <span>대표번호 {TEL}</span>
      </a>
    </div>
  </div>
"""


def footer():
    return f"""
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-top">
        <div class="footer-brand">
          <h2>남성역 헤르니티</h2>
          <p class="brand-sub">NAMSUNG STATION HERNITY</p>
        </div>
        <div class="footer-links">
          <a href="/#overview">사업개요</a>
          <a href="/#units">타입안내</a>
          <a href="/board/">분양소식</a>
          <a href="/#contact">관심고객등록</a>
          <a href="/privacy/"><strong>개인정보처리방침</strong></a>
        </div>
      </div>
      <hr class="footer-divider">
      <div class="footer-bottom">
        <div class="footer-info">
          <p><strong>대표전화:</strong> <a href="tel:{TEL}">{TEL}</a> (무료 통화 연결)</p>
          <p><strong>광고대행:</strong> 바이럴러스 | <strong>대표:</strong> 송덕일 | <strong>사업자등록번호:</strong> 302-08-96000 | <strong>연락처:</strong> 010-4487-4468 | <strong>이메일:</strong> viralers@naver.com</p>
          <p><strong>사업지 위치:</strong> 서울시 동작구 사당동 235-53 일원 (구 남성역 동양라파크 사당)</p>
          <p class="disclaimer">※ 본 사이트는 남성역헤르니티(구 동양라파크 사당) 지역주택조합 및 시공예정사의 이해를 돕기 위해 기존 배포 정보를 바탕으로 제작된 분양 정보 홈페이지입니다. 인허가 과정에 따라 이미지, 면적, 규모, 세대배치, 금액 등은 변경되거나 상이할 수 있습니다. 상기 기재된 내용은 법적 효력을 발휘하지 않습니다.</p>
        </div>
        <div class="footer-copy">
          <p>&copy; 2026 남성역 헤르니티. All rights reserved. Managed by Viralus.</p>
        </div>
      </div>
    </div>
  </footer>

  <div class="mobile-sticky-bar">
    <a href="tel:{TEL}" class="sticky-call">
      {PHONE_SVG.format(cls="phone-icon-sm")}
      <span>전화연결: {TEL}</span>
    </a>
    <a href="/#contact" class="sticky-reg">관심고객 등록</a>
  </div>

  <div class="toast-container" id="toast-container"></div>
  <button class="top-btn" id="top-btn" aria-label="맨 위로 가기">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="top-icon"><polyline points="18 15 12 9 6 15"></polyline></svg>
  </button>
  <script src="/script.js?v={ASSET_VER}"></script>
</body>
</html>
"""


def cta_box():
    return f"""
      <aside class="post-cta">
        <p class="post-cta-title">남성역 헤르니티 상담 · 방문 예약</p>
        <p class="post-cta-desc">타입별 예상 공급가, 조합원 자격, 사업 진행 단계를 1:1로 안내해 드립니다.</p>
        <div class="post-cta-btns">
          <a href="tel:{TEL}" class="btn btn-primary">{PHONE_SVG.format(cls="phone-icon")}<span>{TEL} 전화상담</span></a>
          <a href="/#contact" class="btn btn-outline">관심고객 등록</a>
        </div>
      </aside>"""


def board_table(posts):
    rows = "\n".join(
        f"""          <tr>
            <td class="col-tag"><span class="notice-tag">공지</span></td>
            <td class="col-title"><a href="/board/{p['slug']}/">{esc(p['title'])}</a></td>
            <td class="col-date">{fmt_date(p['date'])}</td>
          </tr>"""
        for p in posts
    )
    return f"""<table class="board-table">
        <thead><tr><th class="col-tag">구분</th><th class="col-title">제목</th><th class="col-date">작성일</th></tr></thead>
        <tbody>
{rows}
        </tbody>
      </table>"""


def build_post(p):
    url = post_url(p)
    img = f"{SITE}/{p['image']}"
    related = [BY_SLUG[s] for s in p.get("related", []) if s in BY_SLUG]
    others = [x for x in POSTS_SORTED if x["slug"] != p["slug"]][:8]
    ld = [
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": p["title"],
            "description": p["description"],
            "image": img,
            "datePublished": f"{p['date']}T09:00:00+09:00",
            "dateModified": f"{p.get('updated', p['date'])}T09:00:00+09:00",
            "mainEntityOfPage": url,
            "author": {"@type": "Organization", "name": SITE_NAME},
            "publisher": {"@type": "Organization", "name": SITE_NAME, "logo": {"@type": "ImageObject", "url": f"{SITE}/favicon.png"}},
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": SITE_NAME, "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "분양소식", "item": f"{SITE}/board/"},
                {"@type": "ListItem", "position": 3, "name": p["title"], "item": url},
            ],
        },
    ]
    rel_html = "\n".join(
        f'          <li><a href="/board/{r["slug"]}/"><img src="/{r["image"]}" alt="{esc(r["title"])}" loading="lazy"><span>{esc(r["title"])}</span></a></li>'
        for r in related
    )
    out = head(p["title"], p["description"], url, p.get("keywords", ""), og_image=img, og_type="article", ld=ld)
    out += header()
    out += f"""
  <main class="board-main">
    <div class="board-container">
      <nav class="breadcrumb" aria-label="breadcrumb"><a href="/">홈</a> › <a href="/board/">분양소식</a> › <span>공지</span></nav>
      <article class="post">
        <header class="post-header">
          <span class="notice-tag">공지</span>
          <h1 class="post-title">{esc(p['title'])}</h1>
          <p class="post-meta"><time datetime="{p['date']}">{fmt_date(p['date'])}</time>{f" · 수정 {fmt_date(p['updated'])}" if p.get('updated') else ""} · 남성역 헤르니티 분양소식</p>
        </header>
        <figure class="post-figure"><img src="/{p['image']}" alt="{esc(p['title'])}"></figure>
        <div class="post-body">
{p['body'].strip()}
        </div>
{cta_box()}
      </article>

      <section class="post-related">
        <h2 class="post-related-title">함께 보면 좋은 글</h2>
        <ul class="related-cards">
{rel_html}
        </ul>
      </section>

      <section class="post-list-more">
        <h2 class="post-related-title">분양소식 최신글</h2>
        {board_table(others)}
        <p class="board-more"><a href="/board/">전체 글 보기 →</a></p>
      </section>
    </div>
  </main>
"""
    out += footer()
    return out


def build_index():
    url = f"{SITE}/board/"
    title = "남성역 헤르니티 분양소식 | 모델하우스·분양가·평면도·사업진행 공지"
    desc = "남성역 헤르니티 모델하우스, 분양가, 타입별 평면도, 조합원 자격, 사업진행 상황 등 최신 분양소식과 공지 모음."
    ld = [
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": title,
            "url": url,
            "hasPart": [{"@type": "Article", "headline": p["title"], "url": post_url(p)} for p in POSTS_SORTED],
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": SITE_NAME, "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "분양소식", "item": url},
            ],
        },
    ]
    out = head(title, desc, url, "남성역 헤르니티, 남성역 헤르니티 모델하우스, 남성역 헤르니티 분양가, 남성역 헤르니티 공지", ld=ld)
    out += header()
    out += f"""
  <main class="board-main">
    <div class="board-container">
      <nav class="breadcrumb" aria-label="breadcrumb"><a href="/">홈</a> › <span>분양소식</span></nav>
      <div class="board-head">
        <span class="section-badge">NOTICE BOARD</span>
        <h1 class="board-title">남성역 헤르니티 <span class="gold-text">분양소식</span></h1>
        <p class="board-desc">모델하우스, 분양가, 평면도, 조합원 자격, 사업진행 상황 등 남성역 헤르니티의 주요 정보를 공지로 정리했습니다.</p>
      </div>
      {board_table(POSTS_SORTED)}
{cta_box()}
    </div>
  </main>
"""
    out += footer()
    return out


def build_sitemap():
    today = max(p.get("updated", p["date"]) for p in POSTS)
    urls = [(f"{SITE}/", today, "daily", "1.0"), (f"{SITE}/board/", today, "daily", "0.9")]
    urls += [(post_url(p), p.get("updated", p["date"]), "weekly", "0.8") for p in POSTS_SORTED]
    body = "\n".join(
        f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{d}</lastmod>\n    <changefreq>{c}</changefreq>\n    <priority>{pr}</priority>\n  </url>"
        for u, d, c, pr in urls
    )
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n'


def rfc822(d):
    return datetime.strptime(d, "%Y-%m-%d").replace(hour=9, tzinfo=KST).strftime("%a, %d %b %Y %H:%M:%S +0900")


def build_rss():
    items = "\n".join(
        f"""    <item>
      <title>{esc(p['title'])}</title>
      <link>{post_url(p)}</link>
      <description><![CDATA[{p['description']}]]></description>
      <pubDate>{rfc822(p['date'])}</pubDate>
      <guid isPermaLink="true">{post_url(p)}</guid>
    </item>"""
        for p in POSTS_SORTED
    )
    latest = rfc822(POSTS_SORTED[0]["date"])
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>남성역 헤르니티 분양소식</title>
    <link>{SITE}/board/</link>
    <description>남성역 헤르니티 모델하우스, 분양가, 평면도, 조합원 자격, 사업진행 상황 공지</description>
    <language>ko</language>
    <pubDate>{latest}</pubDate>
    <lastBuildDate>{latest}</lastBuildDate>
    <atom:link href="{SITE}/rss.xml" rel="self" type="application/rss+xml" />
{items}
  </channel>
</rss>
"""


def update_home():
    path = os.path.join(ROOT, "index.html")
    with open(path, encoding="utf-8") as f:
        src = f.read()
    rows = "\n".join(
        f'            <li><span class="notice-tag">공지</span><a href="/board/{p["slug"]}/">{esc(p["title"])}</a><time datetime="{p["date"]}">{fmt_date(p["date"])}</time></li>'
        for p in POSTS_SORTED[:6]
    )
    block = f"""<!-- BOARD:START (tools/build_board.py 가 자동 생성) -->
  <section class="home-board-section" id="board">
    <div class="section-container">
      <div class="section-header">
        <span class="section-badge">NOTICE</span>
        <h2 class="section-title">남성역 헤르니티 <span class="gold-text">분양소식</span></h2>
        <div class="title-bar"></div>
      </div>
      <ul class="home-board-list">
{rows}
      </ul>
      <p class="board-more"><a href="/board/">분양소식 전체 보기 →</a></p>
    </div>
  </section>
  <!-- BOARD:END -->"""
    pattern = re.compile(r"<!-- BOARD:START.*?<!-- BOARD:END -->", re.S)
    if pattern.search(src):
        src = pattern.sub(lambda _: block, src)
    else:
        anchor = "  <!-- Contact Form Section -->"
        assert anchor in src, "index.html 에서 Contact Form Section 마커를 찾지 못했습니다"
        src = src.replace(anchor, "  " + block + "\n\n" + anchor, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(src)


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


PRIVACY_EFFECTIVE = "2026-10-26"


def build_privacy():
    url = f"{SITE}/privacy/"
    title = "개인정보처리방침 | 남성역 헤르니티"
    desc = "남성역 헤르니티 홈페이지 및 Meta(페이스북·인스타그램) 인스턴트 양식 광고의 개인정보 수집·이용·보관·파기 안내."
    out = head(title, desc, url, robots="noindex, follow")
    out += header()
    out += f"""
  <main class="board-main">
    <div class="board-container">
      <nav class="breadcrumb" aria-label="breadcrumb"><a href="/">홈</a> › <span>개인정보처리방침</span></nav>
      <article class="post privacy">
        <header class="post-header">
          <h1 class="post-title">개인정보처리방침</h1>
          <p class="post-meta">시행일: {fmt_date(PRIVACY_EFFECTIVE)}</p>
        </header>
        <div class="post-body">
<p class="lead">바이럴러스(이하 "회사")는 남성역 헤르니티 조합원 모집 홍보를 위해 운영하는 홈페이지(www.남성역헤르니티.com) 및 Meta(페이스북·인스타그램) 인스턴트 양식 광고를 통해 수집하는 개인정보를 「개인정보 보호법」 등 관련 법령에 따라 안전하게 처리합니다.</p>

<h2>1. 수집하는 개인정보 항목 및 수집 방법</h2>
<table class="post-table">
  <tbody>
    <tr><th>필수 항목</th><td>이름, 휴대전화번호</td></tr>
    <tr><th>선택 항목</th><td>관심 평형, 거주 지역, 방문 희망 일시, 문의 내용, 인입 경로</td></tr>
    <tr><th>수집 방법</th><td>Meta 인스턴트 양식(리드 광고), 홈페이지 관심고객 등록·질문하기 양식, 전화 상담</td></tr>
  </tbody>
</table>
<p class="note">※ 실제 수집 항목은 각 양식에 표시된 항목에 한합니다.</p>

<h2>2. 개인정보의 수집·이용 목적</h2>
<ul>
  <li>남성역 헤르니티 조합원 모집 관련 상담 및 문의 답변</li>
  <li>홍보관 방문 예약 안내 및 일정 연락</li>
  <li>사업 진행 소식 등 관련 정보 안내(전화·문자)</li>
</ul>

<h2>3. 개인정보의 보유 및 이용 기간</h2>
<p>수집한 개인정보는 <strong>조합원 모집 종료 시 또는 정보주체가 삭제를 요청한 때 지체 없이 파기</strong>합니다. 다만 관계 법령에 따라 보존이 필요한 경우 해당 법령에서 정한 기간 동안 보관합니다.</p>

<h2>4. 개인정보의 제3자 제공</h2>
<p>회사는 정보주체의 동의를 받은 범위 안에서만 개인정보를 제공하며, 상담 진행을 위해 아래와 같이 제공합니다.</p>
<table class="post-table">
  <thead><tr><th>제공받는 자</th><th>제공 목적</th><th>제공 항목</th><th>보유 기간</th></tr></thead>
  <tbody>
    <tr><td>남성역지역주택조합추진위원회 및 홍보관 상담 담당자</td><td>조합원 모집 상담 및 방문 예약 안내</td><td>이름, 휴대전화번호, 문의 내용 등 양식 입력 항목</td><td>모집 종료 또는 삭제 요청 시까지</td></tr>
  </tbody>
</table>

<h2>5. 개인정보 처리의 위탁</h2>
<table class="post-table">
  <thead><tr><th>수탁자</th><th>위탁 업무</th></tr></thead>
  <tbody>
    <tr><td>Meta Platforms, Inc.</td><td>인스턴트 양식(리드 광고)을 통한 정보 수집 및 전달</td></tr>
    <tr><td>Vercel Inc.</td><td>홈페이지 호스팅 및 양식 전송 처리</td></tr>
    <tr><td>고객관리(CRM)·문자 알림 시스템 운영사</td><td>상담 신청 정보 저장 및 담당자 알림</td></tr>
  </tbody>
</table>
<p>일부 수탁자는 해외에 서버를 두고 있어 정보가 국외로 이전될 수 있으며, 회사는 수탁자가 개인정보를 안전하게 처리하도록 관리·감독합니다.</p>

<h2>6. 개인정보의 파기 절차 및 방법</h2>
<p>보유 기간이 끝나거나 처리 목적이 달성된 개인정보는 지체 없이 파기합니다. 전자적 파일은 복구할 수 없는 방법으로 삭제하고, 종이 문서는 분쇄하거나 소각합니다.</p>

<h2>7. 정보주체의 권리와 행사 방법</h2>
<p>정보주체는 언제든지 자신의 개인정보 열람, 정정, 삭제, 처리정지 및 동의 철회를 요구할 수 있습니다. 아래 개인정보 보호책임자에게 전화나 이메일로 요청하시면 지체 없이 조치합니다. 동의를 거부할 권리가 있으며, 거부 시 상담 신청이 제한될 수 있습니다.</p>

<h2>8. 개인정보의 안전성 확보 조치</h2>
<ul>
  <li>개인정보 접근 권한을 상담 담당자로 최소화</li>
  <li>전송 구간 암호화(HTTPS) 적용</li>
  <li>접근 기록 관리 및 담당자 교육</li>
</ul>

<h2>9. 개인정보 보호책임자</h2>
<table class="post-table">
  <tbody>
    <tr><th>성명</th><td>송덕일 (바이럴러스 대표)</td></tr>
    <tr><th>연락처</th><td><a href="tel:010-4487-4468">010-4487-4468</a></td></tr>
    <tr><th>이메일</th><td><a href="mailto:viralers@naver.com">viralers@naver.com</a></td></tr>
    <tr><th>사업자등록번호</th><td>302-08-96000</td></tr>
  </tbody>
</table>
<p>개인정보 침해에 대한 신고나 상담이 필요하시면 개인정보침해신고센터(국번 없이 118, privacy.kisa.or.kr), 개인정보분쟁조정위원회(1833-6972, www.kopico.go.kr)에 문의하실 수 있습니다.</p>

<h2>10. 개인정보처리방침의 변경</h2>
<p>이 개인정보처리방침은 {fmt_date(PRIVACY_EFFECTIVE)}부터 적용되며, 내용이 변경되는 경우 홈페이지를 통해 공지합니다.</p>
        </div>
      </article>
    </div>
  </main>
"""
    out += footer()
    return out


def main():
    slugs = [p["slug"] for p in POSTS]
    assert len(slugs) == len(set(slugs)), "slug 중복"
    for p in POSTS:
        assert os.path.exists(os.path.join(ROOT, p["image"])), f"이미지 없음: {p['image']}"
        for r in p.get("related", []):
            assert r in BY_SLUG, f"{p['slug']}: related slug 없음 {r}"
        for link in re.findall(r'href="/board/([^"/]+)/"', p["body"]):
            assert link in BY_SLUG, f"{p['slug']}: 본문 링크 slug 없음 {link}"
    write("board/index.html", build_index())
    for p in POSTS:
        write(f"board/{p['slug']}/index.html", build_post(p))
    write("sitemap.xml", build_sitemap())
    write("rss.xml", build_rss())
    write("privacy/index.html", build_privacy())
    update_home()
    print(f"게시판 생성 완료: 글 {len(POSTS)}개")


if __name__ == "__main__":
    main()
