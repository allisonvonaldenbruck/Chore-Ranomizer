#!/usr/bin/env python3
"""Pick a random chore for today and (optionally) open a GitHub issue for it.

Usage:
    python chore_of_the_day.py              # just print today's chore
    python chore_of_the_day.py --issue      # also create a GitHub issue

For --issue, set these environment variables (GitHub Actions provides them):
    GITHUB_TOKEN        token with permission to create issues
    GITHUB_REPOSITORY   "owner/repo"
"""

import argparse
import json
import os
import random
import urllib.request
from datetime import date

CHORES = [
    "Do the dishes",
    "Take out the trash",
    "Vacuum the living room",
    "Clean the bathroom",
    "Do a load of laundry",
    "Wipe down kitchen counters",
    "Water the plants",
    "Sweep and mop the floors",
    "Tidy your desk",
    "Clean out the fridge",
    "Change the bed sheets",
    "Dust the shelves",
    "Organize one drawer",
    "Take out the recycling",
]


def pick_chore(today: date | None = None, chores: list[str] = CHORES) -> str:
    """Return a random chore. Seeded by the date, so re-running on the
    same day always gives the same answer."""
    today = today or date.today()
    rng = random.Random(today.isoformat())
    return rng.choice(chores)


def create_issue(title: str, body: str) -> str:
    token = os.environ["GITHUB_TOKEN"]
    repo = os.environ["GITHUB_REPOSITORY"]
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/issues",
        data=json.dumps({"title": title, "body": body}).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)["html_url"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Chore of the day")
    parser.add_argument("--issue", action="store_true",
                        help="create a GitHub issue for today's chore")
    args = parser.parse_args()

    today = date.today()
    chore = pick_chore(today)
    print(f"Chore for {today:%A, %B %d, %Y}: {chore}")

    if args.issue:
        url = create_issue(
            title=f"Chore of the day ({today.isoformat()}): {chore}",
            body=f"Today's randomly picked chore is **{chore}**.\n\nClose this issue when it's done!",
        )
        print(f"Created issue: {url}")


if __name__ == "__main__":
    main()
