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
from atoms.backend.entities.instance import AtomsInstance
from atoms.backend.utils.image import AtomsImageUtils
from atoms.backend.wrappers.client_bridge import ClientBridge
from atoms.backend.wrappers.podman import PodmanWrapper


class AtomsBackend:
    __atoms: dict
    config: AtomsConfig

    def __init__(self, podman_support: bool = False, client_bridge: 'ClientBridge' = None):
        if client_bridge is None:
            client_bridge = ClientBridge()

        self.__config = AtomsConfig()
        self.__instance = AtomsInstance(self.__config, client_bridge)
        self.__podman_support = podman_support
        self.__atoms = self.__list_atoms()
        
    def __list_atoms(self) -> dict:
        atoms = {}
        for atom in os.listdir(self.__config.atoms_path):
            if atom.endswith(".atom"):
                atoms[atom] = Atom.load(self.__instance, atom)

        if self.__podman_support and self.has_podman_support:
            atoms.update(self.__list_podman_atoms())

        return atoms

    def __list_podman_atoms(self) -> dict:
        atoms = {}
        containers = PodmanWrapper().get_containers()
        for container_id, info in containers.items():
            atoms[container_id] = Atom.load_from_container(
                self.__instance, info["creation_date"], info["names"], info["image"], container_id
            )
        return atoms
    
    def request_new_atom(
        self,
        name: str, 
        distribution: 'AtomDistribution', 
        architecture: str, 
        release: str, 
        download_fn: callable=None,
        config_fn: callable = None,
        unpack_fn: callable = None,
        finalizing_fn: callable = None,
        error_fn: callable = None
    ):
        return Atom.new(
            self.__instance, name, distribution, architecture, release, 
            download_fn, config_fn, unpack_fn, finalizing_fn, error_fn
        )

    @property
    def atoms(self) -> dict:
        return self.__atoms

    @property
    def has_atoms(self) -> bool:
        return len(self.__atoms) > 0
    
    @property
    def local_images(self) -> list:
        return AtomsImageUtils.get_image_list(self.__config)
    
    @property
    def has_podman_support(self) -> bool:
        return PodmanWrapper().is_supported

    @property
    def client_bridge(self) -> 'ClientBridge':
        return self.__client_bridge
