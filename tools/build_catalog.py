# Copyright (C) 2026 Luca Baldini (luca.baldini@pi.infn.it)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import yaml
from pathlib import Path

import jinja2
from loguru import logger


_ROOT = Path(__file__).resolve().parents[1]
_CATALOG_DIR = _ROOT / "catalog"
_MARKUP_DIR = _ROOT / "docs" / "catalog"


def build_catalog():
    """Build the glorious catalog of books.
    """
    logger.info("Building catalog...")
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(_ROOT / "templates"),
        undefined=jinja2.StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True,
    )

    book_template = env.get_template("book.md.j2")
    index_template = env.get_template("catalog.md.j2")

    _MARKUP_DIR.mkdir(parents=True, exist_ok=True)

    books = []
    for source in sorted(_CATALOG_DIR.glob("*.yml")):
        stem = source.stem
        with source.open(encoding="utf-8") as stream:
            book = yaml.safe_load(stream)
            book["id"] = stem
            book["author_names"] = ", ".join(
                author["name"] for author in book["authors"]
            )
            books.append(book)
            rendered = book_template.render(book=book)
            (_MARKUP_DIR / f"{stem}.md").write_text(rendered, encoding="utf-8")

    rendered = index_template.render(books=books)
    (_MARKUP_DIR / "index.md").write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    build_catalog()