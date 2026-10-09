#!/usr/bin/env python3
"""zino.kr RSS 에서 최신 글 N개를 읽어 README 의 ZINO_POSTS 마커 사이를 갱신한다."""
import re, sys, urllib.request, html

FEED = "https://zino.kr/rss.xml"
N = 6
README = "README.md"


def main() -> None:
    try:
        xml = urllib.request.urlopen(urllib.request.Request(FEED, headers={"User-Agent": "zino-profile-bot"}), timeout=30).read().decode("utf8", "replace")
    except Exception as e:  # noqa: BLE001
        print(f"RSS 조회 실패: {e}", file=sys.stderr)
        sys.exit(1)
    items = re.findall(r"<item>(.*?)</item>", xml, re.S)[:N]
    lines = []
    for it in items:
        t = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", it, re.S)
        l = re.search(r"<link>(.*?)</link>", it, re.S)
        if not (t and l):
            continue
        title = html.unescape(t.group(1).strip())
        link = l.group(1).strip()
        lines.append(f"- [{title}]({link})")
    if not lines:
        print("item 없음", file=sys.stderr)
        sys.exit(1)
    block = "\n".join(lines)
    md = open(README, encoding="utf8").read()
    new = re.sub(
        r"(<!-- ZINO_POSTS:START -->).*?(<!-- ZINO_POSTS:END -->)",
        lambda m: f"{m.group(1)}\n{block}\n{m.group(2)}",
        md,
        flags=re.S,
    )
    if new != md:
        open(README, "w", encoding="utf8").write(new)
        print("README 갱신됨")
    else:
        print("변경 없음")


if __name__ == "__main__":
    main()
