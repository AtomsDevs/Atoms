# image.py
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
import time
import requests

from atoms.backend.utils.file import FileUtils
from atoms.backend.utils.download import DownloadUtils
from atoms.backend.entities.image import AtomImage
from atoms.backend.exceptions.image import AtomsFailToDownloadImage


class AtomsImageUtils:

    @staticmethod
    def get_image(
        instance: "AtomsInstance", 
        distribution: "AtomDistribution", 
        architecture: str, 
        release: str,
        update_fn: callable
    ) -> AtomImage:
        remote = distribution.get_remote(architecture, release)
        image_name = distribution.get_image_name(architecture, release)
        image_path = os.path.join(instance.config.atoms_images, image_name)
        remote_hash = distribution.read_remote_hash(architecture, release)
        hash_type = distribution.remote_hash_type

        if not os.path.exists(image_path):
            if not DownloadUtils(instance, remote, image_path, update_fn, remote_hash, hash_type).download():
                raise AtomsFailToDownloadImage(remote)

        return AtomImage(image_name, image_path, distribution.root)
    
    @staticmethod
    def get_image_list(config: "AtomsConfig"):
        image_list = []
        for image in os.listdir(config.atoms_images):
            image_list.append(AtomImage(image, os.path.join(config.atoms_images, image)))
        image_list.sort(key=lambda x: x.name)
        return image_list
