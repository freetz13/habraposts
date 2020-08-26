#!/usr/bin/env python3

import sys
from pathlib import Path

import yaml
import requests
from habraparser import parse, REASONS

STORAGE_DIR = Path(__file__).absolute().parent / 'posts'


def save(data, fname):
    with open(fname, "w", encoding="utf-8", newline="\n") as fobj:
        fobj.write(yaml.dump(data, allow_unicode=True))


def main():
    url = sys.argv[1] if sys.argv[1:] else input("Enter url: ")
    if not STORAGE_DIR.exists():
        STORAGE_DIR.mkdir()

    print("Fetching...")
    try:
        response = requests.get(url)
    except requests.RequestException as exception:
        print(f"{url}: {exception}")
        return

    if response.status_code in REASONS.keys():
        if response.history:
            url = response.history[-1].url
        print(f"{url}: {REASONS[response.status_code]}")
        return

    # We can only work with "text/html" content-type
    if not response.headers.get("content-type", "").startswith("text/html"):
        print(f"{response.url}: Unexpected content-type")
        return

    print("Parsing...")
    info = parse(response.text)

    print(f"title:\t\t{info['title']}")
    print(f"url:\t\t{info['url']}")
    print(f"id:\t\t{info['id']}")
    print(f"published:\t{info['published']}")
    print(f"tags:\t\t{', '.join(info['tags'])}")
    print(f"words_count:\t{info['words_count']}")
    print(f"comments_count:\t{info['comments_count']}")
    print()

    filename = STORAGE_DIR / f"{info['id']}.yaml"
    answer = input(f"Post will be saved in '{filename}' file. OK? [y/N]: ")
    if answer.lower() != "y":
        return

    try:
        save(info, filename)
    finally:
        print("Post added!")


if __name__ == "__main__":
    sys.exit(main())
