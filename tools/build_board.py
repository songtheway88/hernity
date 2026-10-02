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
ASSET_VER = "15"

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


def head(title, description, canonical, keywords="", og_image=f"{SITE}/img/og-image.jpg", og_type="website", ld=()):
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
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="index, follow">
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
  <link rel="stylesheet" href="/board/board.css?v={ASSET_VER}">
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
          <p class="post-meta"><time datetime="{p['date']}">{fmt_date(p['date'])}</time> · 남성역 헤르니티 분양소식</p>
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
    update_home()
    print(f"게시판 생성 완료: 글 {len(POSTS)}개")


if __name__ == "__main__":
    main()
