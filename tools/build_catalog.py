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

import sys
from pathlib import Path

import jinja2
from loguru import logger

from catalog import load_author_registry, load_product


_ROOT = Path(__file__).resolve().parents[1]
_CATALOG_DIR = _ROOT / "catalog"
_PRODUCTS_DIR = _ROOT / "docs" / "products"
_AUTHORS_DIR = _ROOT / "docs" / "authors"


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

    _PRODUCTS_DIR.mkdir(parents=True, exist_ok=True)
    _AUTHORS_DIR.mkdir(parents=True, exist_ok=True)

    product_template = env.get_template("product.md.j2")
    catalog_template = env.get_template("catalog.md.j2")

    author_registry = load_author_registry(_CATALOG_DIR / "_authors.yaml")
    products = []
    for source in sorted(_CATALOG_DIR.glob("*.yaml")):
        stem = source.stem
        # Skip the special files that start with an underscore.
        if stem.startswith("_"):
            continue
        product = load_product(source, author_registry)
        products.append(product)
        for author in product.authors:
            author.products.append(product)
        rendered = product_template.render(product=product)
        (_PRODUCTS_DIR / f"{stem}.md").write_text(rendered, encoding="utf-8")

    rendered = catalog_template.render(products=products)
    (_PRODUCTS_DIR / "index.md").write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    logger.remove()
    fmt = ">>> <level>[{level}] {message}</level>"
    logger.add(sys.stderr, level="DEBUG", colorize=True, format=fmt)
    build_catalog()