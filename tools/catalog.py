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

from pydantic import BaseModel, ConfigDict, TypeAdapter



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
    email: str
    website: str | None = None

    @staticmethod
    def initials(text: str) -> str:
        """Return the initials of a given piece of text.

        This turns, e.g., "Emanuele" into "E." and "Maria Chiara" into "M. C.".
        """
        return " ".join(f"{part[0]}." for part in text.split())

    def short_name(self) -> str:
        """Return a shortened version of the full name, with the initials of the
        actual name, and the full surname.

        This turns, e.g., "Emanuele Paolini" into "E. Paolini" and
        "Maria Chiara Pievatolo" into "M. C. Pievatolo."
        """
        return f"{self.initials(self.name)} {self.surname}"



def load_authors(file_path: str) -> list[Author]:
    """Load the authors from a yaml file.
    """
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
    return TypeAdapter(dict[str, Author]).validate_python(data)



if __name__ == "__main__":
    file_path = "/home/users/lbaldini/teaching/unipico/pages/catalog/_authors.yaml"
    db = load_authors(file_path)
    for author in db.values():
        print(author)
        print(author.short_name())
    print(db["luca-baldini"])