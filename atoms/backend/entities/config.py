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
from atoms.backend.exceptions.config import AtomsCantMakeAtomsPath, AtomsConfigKeyNotFound


class AtomsConfig:
    atoms_path: str

    def __init__(self):
        self.atoms_path = AtomsPaths.atoms
        self.atoms_images = AtomsPaths.images
        self.__load()

    def __load(self):
        if not os.path.exists(AtomsPaths.config_file):
            self.__save()

        with open(AtomsPaths.config_file, "r") as f:
            config = orjson.loads(f.read())

        if config.get("atoms.path"):
            self.atoms_path = config["atoms.path"]

        if config.get("images.path"):
            self.atoms_images = config["images.path"]

        if not os.path.exists(self.atoms_path):
            try:
                os.makedirs(self.atoms_path)
            except PermissionError:
                raise AtomsCantMakeAtomsPath(self.atoms_path)
                
        if not os.path.exists(self.atoms_images):
            try:
                os.makedirs(self.atoms_images)
            except PermissionError:
                raise AtomsCantMakeAtomsPath(self.atoms_images)

    def __save(self):
        os.makedirs(AtomsPaths.app_data, exist_ok=True)
        with open(AtomsPaths.config_file, "wb") as f:
            f.write(orjson.dumps(self.to_dict(), f, option=orjson.OPT_NON_STR_KEYS))
    
    def to_dict(self) -> dict:
        conf = {}
        if self.atoms_path != AtomsPaths.atoms:
            conf["atoms.path"] = self.atoms_path
        if self.atoms_images != AtomsPaths.images:
            conf["images.path"] = self.atoms_images
        return conf
    
    def restore_default(self, config_key: str):
        if config_key == "atoms.path":
            self.atoms_path = AtomsPaths.atoms
        elif config_key == "images.path":
            self.atoms_images = AtomsPaths.images
        else:
            raise AtomsConfigKeyNotFound(config_key)
            
        self.__save()

    def is_default(self, config_key: str) -> bool:
        if config_key == "atoms.path":
            return self.atoms_path == AtomsPaths.atoms
        elif config_key == "images.path":
            return self.atoms_images == AtomsPaths.images
        return False
    
    def set_value(self, config_key: str, config_value: str):
        if config_key == "atoms.path":
            self.atoms_path = config_value
        elif config_key == "images.path":
            self.atoms_images = config_value
        else:
            raise AtomsConfigKeyNotFound(config_key)
            
        self.__save()
