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

from atoms.backend.exceptions.distribution import AtomsUnknownDistribution
from atoms.backend.entities.distribution import AtomDistribution
from atoms.backend.entities.distributions import *


class AtomsDistributionsUtils:

    @staticmethod
    def get_distribution(distribution_id: str) -> AtomDistribution:
        # Stable (know-working) images
        if distribution_id == "alpinelinux":
            return AlpineLinux()
        if distribution_id == "ubuntu":
            return Ubuntu()
        if distribution_id == "fedora":
            return Fedora()
        
        # Experimental images
        if distribution_id == "archlinux":  # pacman broken
            return ArchLinux()

        # Unimplemented images
        # if distribution_id == "fedora":
        #     return Fedora()
        # if distribution_id == "debian": # missing compatible tarball (no raw image)
        #     return Debian()
            
        return Unknown()
    
    @staticmethod
    def get_distribution_by_container_image(image: str) -> AtomDistribution:
        for distribution in AtomsDistributionsUtils.get_distributions():
            if distribution.is_container_image(image):
                return distribution
        return Unknown()
    
    @staticmethod
    def get_distributions() -> list:
        distributions = [
            AlpineLinux(),
            Ubuntu(),
            Fedora(),
        ]
        if "SHOW_EXPERIMENTAL_IMAGES" in os.environ:
            distributions.append(ArchLinux())
        return distributions
