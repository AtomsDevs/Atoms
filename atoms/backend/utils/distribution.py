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

from atoms.backend.exceptions.distribution import AtomsUnknownDistribution
from atoms.backend.entities.distribution import AtomDistribution
from atoms.backend.entities.distributions import *


class AtomsDistributionsUtils:

    @staticmethod
    def get_distribution(distribution_id: str) -> AtomDistribution:
        if distribution_id == "alpinelinux":
            return AlpineLinux()
        if distribution_id == "ubuntu":
            return Ubuntu()
        if distribution_id == "archlinux":
            return ArchLinux()
        # TODO: the following distributions are not yet implemented 
        # if distribution_id == "fedora":
        #     return Fedora()
        # if distribution_id == "debian":
        #     return Debian()
            
        raise AtomsUnknownDistribution(distribution_id)
    
    @staticmethod
    def get_distributions() -> dict:
        return [
            AlpineLinux(),
            Ubuntu(),
            ArchLinux(),
        ]
