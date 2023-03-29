import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup

REASONS = {
    403: "Доступ к публикации закрыт",
    404: "Страница не найдена",
}


class TagNotFound(LookupError):
    pass


def _process(object_, handler, exception):
    if not isinstance(exception, Exception):
        raise ValueError("exception should be an Exception instance")
    if object_ is None:
        raise exception
    if not callable(handler):
        raise ValueError("handler should be callable")
    return handler(object_)


def parse(html: str):
    soup = BeautifulSoup(html, "html.parser")

    url = _process(
        soup.select_one("link[rel=canonical]"),
        lambda element: element.get("href", ""),
        TagNotFound("Can't find url"),
    )

    id_ = _process(
        re.match(r"\/.+?\/*(?P<id>\d+)\/", urlparse(url).path),
        lambda element: int(element.group("id")),
        ValueError("Can't find id from url"),
    )

    title = _process(
        soup.select_one("h1.tm-title"),
        lambda element: element.get_text(),
        TagNotFound("Can't find title"),
    )

    published = _process(
        soup.select_one("span.tm-article-datetime-published time"),
        lambda element: element.get("datetime"),
        TagNotFound("Can't find published"),
    )

    tags = _process(
        soup.select('.tm-separated-list__list')[0].select('a'),
        lambda element: [i.text for i in element],
        TagNotFound("Can't find tags"),
    )

    words_count = _process(
        soup.select_one("div.tm-article-body"),
        lambda element: len(re.findall(r"\w+", element.get_text())),
        TagNotFound("Can't find words_count"),
    )

    comments_count = _process(
        soup.select_one(".tm-article-comments-counter-link__value"),
        lambda element: int(''.join(i for i in element.get_text() if i.isdigit()) or '0'),
        TagNotFound("Can't find comments_count"),
    )

    return {
        "url": url,
        "id": id_,
        "title": title,
        "published": published,
        "tags": tags,
        "words_count": words_count,
        "comments_count": comments_count,
    }
