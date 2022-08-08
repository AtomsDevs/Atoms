# distribution.py
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
import re
import requests
import shlex

from atoms.backend.exceptions.distribution import AtomsUnreachableRemote


class AtomDistribution:
    distribution_id: str
    name: str
    logo: str
    remote_structure: str
    remote_hash_structure: str
    architectures: dict

    def __init__(
        self, 
        distribution_id: str, 
        name: str, 
        logo: str, 
        releases: list,
        remote_structure: str, 
        remote_hash_structure: str,
        remote_hash_type: str,
        architectures: dict,
        root: str,
        container_image_name: str
    ):
        self.distribution_id = distribution_id
        self.name = name
        self.logo = logo
        self.releases = releases
        self.remote_structure = remote_structure
        self.remote_hash_structure = remote_hash_structure
        self.remote_hash_type = remote_hash_type
        self.architectures = architectures
        self.root = root
        self.container_image_name = container_image_name

    def __str__(self):
        return f"Distribution {self.name}"
    
    def get_remote(self, architecture: str, release: str) -> str:
        return self.remote_structure.format(release, architecture)

    def get_remote_hash(self, architecture: str, release: str) -> str:
        return self.remote_hash_structure.format(release, architecture)
    
    def get_image_name(self, architecture: str, release: str) -> str:
        remote = self.get_remote(architecture, release)
        return os.path.basename(remote)
    
    def read_remote_hash(self, architecture: str, release: str) -> str:
        remote_hash = self.get_remote_hash(architecture, release)
        response = requests.get(remote_hash)

        if response.status_code != 200:
            raise AtomsUnreachableRemote(remote_hash)
            
        content = response.text.split("\n")
        for line in content:
            _hash, _file = re.split(r"\s+", line, maxsplit=1)
            if self.get_image_name(architecture, release) in _file:
                return _hash.strip()

        raise ValueError(f"Unknown check_type method: {check_type}")
    
    def is_container_image(self, image: str) -> bool:
        return self.container_image_name in image
