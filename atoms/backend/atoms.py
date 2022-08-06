# atoms.py
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

from atoms.backend.entities.config import AtomsConfig
from atoms.backend.entities.atom import Atom
from atoms.backend.utils.image import AtomsImageUtils


class AtomsBackend:
    __atoms: dict
    config: AtomsConfig

    def __init__(self):
        self.config = AtomsConfig()
        self.__atoms = self.__list_atoms()
        
    def __list_atoms(self) -> dict:
        atoms = {}
        for atom in os.listdir(self.config.atoms_path):
            if atom.endswith(".atom"):
                atoms[atom] = Atom.load(self.config, atom)
        return atoms

    @property
    def atoms(self) -> dict:
        return self.__atoms

    @property
    def has_atoms(self) -> bool:
        return len(self.__atoms) > 0
    
    @property
    def local_images(self) -> list:
        return AtomsImageUtils.get_image_list(self.config)
