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

import pathlib
from tomlkit import value
import yaml
from enum import StrEnum

import pycountry
from loguru import logger
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

    STUDENT = "studente"
    POSTDOC = "postdoc"
    STAFF = "staff"
    RETIRED = "retired"


class LinkType(StrEnum):

    """Enumeration of the possible link types of a book.
    """

    PDF = "pdf"
    EPUB = "epub"
    HTML = "html"
    REPO = "repo"


class AudienceLevel(StrEnum):

    """Enumeration of the possible audience levels of a book.
    """

    LT = "LT"
    LM = "LM"
    PHD = "PhD"


class Author(BaseModel):

    """Representation of an author of a book.

    Arguments
    ---------
    name: str
        The first name of the author.

    surname: str
        The surname of the author.

    institution: str
        The institution of the author.

    department: str
        The department of the author.

    role: Role
        The academic role of the author.

    email: EmailStr
        The email address of the author.

    website: HttpUrl | None
        The website of the author, if any.

    products: list
        The list of products authored by this author. This is automatically
        populated when the catalog is built, and should not be set manually.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str
    name: str
    surname: str
    institution: str
    department: str
    role: Role
    email: EmailStr | None = None
    website: HttpUrl | None = None
    products: list = Field(default_factory=list)

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

    def full_name(self) -> str:
        """Return the full name of the author, with the actual name and the surname.

        Returns
        -------
        str
            The full version of the name.
        """
        return f"{self.name} {self.surname}"


class Licensing(BaseModel):

    """Representation of the licenses of a product.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    content: str
    code: str | None = None

    @field_validator("content", "code")
    @classmethod
    def validate(cls, identifier: str | None) -> str | None:
        """Validate a license identifier.

        This function makes sure that the license is a valid SPDX identifier.
        See https://spdx.org/licenses/ for the list of valid identifiers.

        Arguments
        ---------
        identifier: str | None
            The license identifier to validate.

        Returns
        -------
        str | None
            The validated license, in canonical form.
        """
        if identifier is None:
            return None
        if identifier == "n/a":
            logger.warning("License is set to 'n/a', which is not a valid SPDX identifier")
            return "n/a"
        try:
            return canonicalize_license_expression(identifier)
        except InvalidLicenseExpression as error:
            raise ValueError(f"Invalid SPDX expression: {error}") from error


class Product(BaseModel):

    """Representation of a product in the catalog.

    Arguments
    ---------
    id: str
        The unique identifier of the product.

    title: str
        The title of the product.

    authors: list[Author]
        The list of authors of the product.

    language: str
        The language of the product, in ISO 639-1 (2-digits) format.

    license: str
        The license of the product, in SPDX format.

    links: dict[str, HttpUrl]
        The dictionary of links to the product, with the link type as key,
        and the URL as value.

    topics: list[str]
        The list of topics of the product, as a list of strings.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str
    title: str
    authors: list[Author]
    language: str
    licensing: Licensing
    links: dict[LinkType, HttpUrl]
    level: AudienceLevel
    topics: list[str] = Field(default_factory=list)
    targets: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)

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

    def author_list(self) -> str:
        """Return a string with the list of authors, in the form of "A. Surname,
        B. Surname, C. Surname".

        Returns
        -------
        str
            The list of authors, in the form of "A. Surname, B. Surname, C. Surname".
        """
        return ", ".join(author.short_name() for author in self.authors)



def load_author_registry(file_path: str) -> dict[str, Author]:
    """Load the authors from a yaml file.
    """
    logger.info(f"Loading author registry from {file_path}...")
    with open(file_path, "r", encoding="utf-8") as input_file:
        data = yaml.safe_load(input_file)
    for author_id, author_data in data.items():
        author_data["id"] = author_id
    return TypeAdapter(dict[str, Author]).validate_python(data)


def load_product(file_path: str, author_registry: dict[str: Author]) -> Product:
    """Load a single catalog product from a yaml file.
    """
    logger.info(f"Loading product from {file_path}...")
    with open(file_path, "r", encoding="utf-8") as input_file:
        data = yaml.safe_load(input_file)
    # Add the stem of the file name as the product id, so that the pydantic
    # validator can pick it up.
    data["id"] = pathlib.Path(file_path).stem
    return Product.model_validate(data, context={"author_registry": author_registry})
