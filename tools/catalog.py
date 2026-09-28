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

"""Collection of utilities to parse and process the yaml files for the catalog.
"""

import yaml
from enum import StrEnum

import pycountry
from packaging.licenses import (
    InvalidLicenseExpression,
    canonicalize_license_expression
)
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    HttpUrl,
    TypeAdapter,
    ValidationInfo,
    field_validator
)


class Role(StrEnum):

    """Enumeration of the possible academic roles of an author in a book.
    """

    STUDENT = "student"
    POSTDOC = "postdoc"
    STAFF = "staff"



class Author(BaseModel):

    """Representation of an author of a book.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str
    surname: str
    institution: str
    department: str
    role: Role
    email: EmailStr
    website: HttpUrl | None = None

    @staticmethod
    def initials(text: str) -> str:
        """Return the initials of a given piece of text.

        This turns, e.g., "Emanuele" into "E." and "Maria Chiara" into "M. C.".

        Arguments
        ---------
        text: str
            The text to extract the initials from.

        Returns
        -------
        str
            The initials of the text, with a dot after each initial.
        """
        return " ".join(f"{part[0]}." for part in text.split())

    def short_name(self) -> str:
        """Return a shortened version of the full name, with the initials of the
        actual name, and the full surname.

        This turns, e.g., "Emanuele Paolini" into "E. Paolini" and
        "Maria Chiara Pievatolo" into "M. C. Pievatolo."

        Returns
        -------
        str
            The shortened version of the full name.
        """
        return f"{self.initials(self.name)} {self.surname}"


class Product(BaseModel):

    """Representation of a product in the catalog.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    title: str
    authors: list[Author]
    language: str
    license: str
    links: dict[str, HttpUrl]
    topics: list[str] = Field(default_factory=list)

    @field_validator("authors", mode="before")
    @classmethod
    def validate_authors(cls, author_ids: list[str], info: ValidationInfo) -> list[Author]:
        """Validate the list of authors.

        Note the underlying yaml file contains the list of author unique
        identifiers, in the form of plain strings. This function does two things:

        1. it makes sure that all the author identifiers are present in the registry;
        2. it replaces the list of identifiers with the actual list of Author objects.

        Arguments
        ---------
        author_ids: list[str]
            The list of author identifiers to validate.

        info: ValidationInfo
            The validation info, which contains the context with the author registry.

        Returns
        -------
        list[Author]
            The list of Author objects corresponding to the validated identifiers.
        """
        # Make sure we have the author registry in the context, otherwise we
        # cannot validate the author list.
        try:
            registry = info.context["author_registry"]
        except (AttributeError, KeyError):
            raise RuntimeError("The author registry was not provided")
        # Loop over the list of author identifiers, and build the list of Author objects.
        author_list = []
        for author_id in author_ids:
            try:
                author = registry[author_id]
            except KeyError:
                raise ValueError(f"Author '{author_id}' not found in the registry")
            author_list.append(author)
        return author_list

    @field_validator("language")
    @classmethod
    def validate_language(cls, language: str) -> str:
        """Validate the language of the product.

        This function makes sure that the language is a valid ISO 639-1 code, and
        uses pycountry under the hood, see
        https://github.com/pycountry/pycountry

        Note we accept only the two-letter codes. The language code is automatically
        converted to lowercase, so that "EN" and "en" are both accepted.

        Arguments
        ---------
        language: str
            The language to validate.

        Returns
        -------
        str
            The validated language.
        """
        language = language.lower()
        if not pycountry.languages.get(alpha_2=language):
            raise ValueError(f"Language '{language}' is not a valid ISO 639-1 code")
        return language

    @field_validator("license")
    @classmethod
    def validate_license(cls, license: str) -> str:
        """Validate the license of the product.

        This function makes sure that the license is a valid SPDX identifier.
        See https://spdx.org/licenses/ for the list of valid identifiers.

        Arguments
        ---------
        license: str
            The license to validate.

        Returns
        -------
        str
            The validated license, in canonical form.
        """
        if license.lower() == "n/a":
            return "n/a"
        try:
            return canonicalize_license_expression(license)
        except InvalidLicenseExpression as error:
            raise ValueError(f"Invalid SPDX licence: {error}") from error



def load_author_registry(file_path: str) -> dict[str, Author]:

    """Load the authors from a yaml file.
    """

    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
    return TypeAdapter(dict[str, Author]).validate_python(data)


def load_product(file_path: str, author_registry: dict[str: Author]) -> Product:

    """Load a single catalog product from a yaml file.
    """

    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
    return Product.model_validate(data, context={"author_registry": author_registry})


if __name__ == "__main__":
    import pathlib

    root_dir = pathlib.Path(__file__).resolve().parents[1] / "catalog"
    author_registry = load_author_registry(root_dir / "_authors.yaml")
    print(author_registry)
    for source in sorted(root_dir.glob("*.yaml")):
        if source.name.startswith("_"):
            continue
        print(source)
        product = load_product(source, author_registry)
        print(product)
