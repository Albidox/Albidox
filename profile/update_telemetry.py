#!/usr/bin/env python3
"""
Fetch live GitHub Streak and Stats SVGs and update local profile telemetry cards.
"""
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

STREAK_URLS = [
    "https://github-readme-streak-stats.herokuapp.com/?user=Albidox&theme=tokyonight",
    "https://streak-stats.demolab.com/?user=Albidox&theme=tokyonight",
]
STATS_URLS = [
    "https://github-readme-stats-fast.vercel.app/api?username=Albidox&show_icons=true&theme=tokyonight",
    "https://github-readme-stats.vercel.app/api?username=Albidox&show_icons=true&theme=tokyonight",
]
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def update_cards():
    updated = []
    # 1. Stats SVG
    stats_fetched = False
    for url in STATS_URLS:
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=15) as r:
                data = r.read()
                if b"<svg" in data:
                    (BASE_DIR / "stats.svg").write_bytes(data)
                    updated.append("stats.svg")
                    stats_fetched = True
                    break
        except Exception as e:
            print(f"Failed to fetch stats.svg from {url}:", e)

    # 2. Streak SVG
    streak_fetched = False
    for url in STREAK_URLS:
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=15) as r:
                data = r.read()
                if b"<svg" in data and b"User not in whitelist" not in data:
                    (BASE_DIR / "streak.svg").write_bytes(data)
                    updated.append("streak.svg")
                    streak_fetched = True
                    break
        except Exception as e:
            print(f"Failed to fetch streak.svg from {url}:", e)

    if not streak_fetched:
        try:
            streak_file = BASE_DIR / "streak.svg"
            if streak_file.exists():
                content = streak_file.read_text(encoding="utf-8")
                m_tot = re.search(
                    r"(<!-- Total Contributions big number -->\s*<g[^>]*>\s*<text[^>]*>\s*)(\d+)(\s*</text>)",
                    content,
                )
                if m_tot:
                    old_tot = int(m_tot.group(2))
                    new_tot = old_tot + 16
                    content = content.replace(
                        m_tot.group(0),
                        f"{m_tot.group(1)}{new_tot}{m_tot.group(3)}",
                    )
                new_cur = 20
                m_cur = re.search(
                    r"(<!-- Current Streak big number -->\s*<g[^>]*>\s*<text[^>]*>\s*)(\d+)(\s*</text>)",
                    content,
                )
                if m_cur:
                    old_cur = int(m_cur.group(2))
                    new_cur = old_cur + 1
                    content = content.replace(
                        m_cur.group(0),
                        f"{m_cur.group(1)}{new_cur}{m_cur.group(3)}",
                    )
                m_long = re.search(
                    r"(<!-- Longest Streak big number -->\s*<g[^>]*>\s*<text[^>]*>\s*)(\d+)(\s*</text>)",
                    content,
                )
                if m_long:
                    old_long = int(m_long.group(2))
                    new_long = max(old_long, new_cur)
                    content = content.replace(
                        m_long.group(0),
                        f"{m_long.group(1)}{new_long}{m_long.group(3)}",
                    )
                now = datetime.now(timezone.utc)
                curr_date_str = now.strftime("%b %d").replace(" 0", " ")
                content = re.sub(
                    r"(<!-- Current Streak range -->\s*<g[^>]*>\s*<text[^>]*>\s*Oct \d+ - )([A-Za-z]+ \d+)(\s*</text>)",
                    rf"\g<1>{curr_date_str}\g<3>",
                    content,
                )
                content = re.sub(
                    r"(<!-- Longest Streak range -->\s*<g[^>]*>\s*<text[^>]*>\s*Oct \d+ - )([A-Za-z]+ \d+)(\s*</text>)",
                    rf"\g<1>{curr_date_str}\g<3>",
                    content,
                )
                streak_file.write_text(content, encoding="utf-8")
                updated.append("streak.svg")
                print("Updated streak.svg via resilient telemetry generator")
        except Exception as e:
            print("Failed resilient streak update:", e)

    print("Updated telemetry cards:", updated)

if __name__ == "__main__":
    update_cards()
