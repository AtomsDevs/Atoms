# config.py
#
# Copyright 2022 mirkobrombin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundationat version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import orjson

from atoms.backend.params.paths import AtomsPaths
from atoms.backend.exceptions.config import AtomsCantMakeAtomsPath


class AtomsConfig:
    atoms_path: str

    def __init__(self):
        self.atoms_path = AtomsPaths.atoms
        self.__load()

    def __load(self):
        if not os.path.exists(AtomsPaths.config_file):
            self.__save()

        with open(AtomsPaths.config_file, "r") as f:
            config = orjson.loads(f.read())

        if config.get("atoms.path") not in [AtomsPaths.atoms, None]:
            if not os.path.exists(config.get("atoms.path")):
                try:
                    os.makedirs(config.get("atoms.path"))
                except PermissionError:
                    raise AtomsCantMakeAtomsPath(config.get("atoms.path"))
            self.atoms_path = config.get("atoms.path")

    def __save(self):
        os.makedirs(AtomsPaths.app_data, exist_ok=True)
        with open(AtomsPaths.config_file, "wb") as f:
            f.write(orjson.dumps(self.to_dict(), f, option=orjson.OPT_NON_STR_KEYS))
    
    def to_dict(self):
        conf = {}
        if self.atoms_path != AtomsPaths.atoms:
            conf["atoms.path"] = self.atoms_path
        return conf
