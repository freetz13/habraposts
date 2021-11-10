#!/usr/bin/env python3

import sys
from pathlib import Path

import requests

from habrakeeper.wsgi import application
from api.models import Article, AuthorTag
from habraparser import parse, REASONS


def main():
    url = sys.argv[1] if sys.argv[1:] else input("Enter url: ")
    if url.isdecimal():
        url = f"https://habr.com/ru/post/{url}/"

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

    answer = input(f"Post will be saved in Django database file. OK? [y/N]: ")
    if answer.lower() != "y":
        return

    created = None
    try:
        post, created = Article.objects.get_or_create(id=info['id'])

        post.url=info['url']
        post.title=info['title']
        post.published=info['published']
        post.words_count=info['words_count']
        post.comments_count=info['comments_count']
        post.save()

        for tag in info['tags']:
            article_tag, _ = AuthorTag.objects.get_or_create(name=tag)
            article_tag.save()
            post.author_tags.add(article_tag)
    except Exception as e:
        raise e
    else:
        print("Post created!" if created else "Post updated")


if __name__ == "__main__":
    sys.exit(main())
