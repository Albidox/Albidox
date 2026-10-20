#!/usr/bin/env python3
"""
Fetch live GitHub Streak and Stats SVGs and update local profile telemetry cards.
"""
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

STREAK_URL = "https://github-readme-streak-stats.herokuapp.com/?user=Albidox&theme=tokyonight"
STATS_URL = "https://github-readme-stats.vercel.app/api?username=Albidox&show_icons=true&theme=tokyonight"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def update_cards():
    updated = []
    # 1. Streak SVG
    try:
        req = urllib.request.Request(STREAK_URL, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read()
            if b"<svg" in data:
                (BASE_DIR / "streak.svg").write_bytes(data)
                updated.append("streak.svg")
    except Exception as e:
        print("Failed to fetch streak.svg:", e)

    # 2. Stats SVG
    try:
        req = urllib.request.Request(STATS_URL, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read()
            if b"<svg" in data:
                (BASE_DIR / "stats.svg").write_bytes(data)
                updated.append("stats.svg")
    except Exception as e:
        print("Failed to fetch stats.svg:", e)

    print("Updated telemetry cards:", updated)

if __name__ == "__main__":
    update_cards()
