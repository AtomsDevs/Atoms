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

class AtomDistribution:
    distribution_id: str
    name: str
    logo: str
    remote_structure: str
    architectures: list

    def __init__(
        self, 
        distribution_id: str, 
        name: str, 
        logo: str, 
        releases: list,
        remote_structure: str, 
        architectures: list
    ):
        self.distribution_id = distribution_id
        self.name = name
        self.logo = logo
        self.releases = releases
        self.remote_structure = remote_structure
        self.architectures = architectures

    def __str__(self):
        return f"Distribution {self.name}"
    
    def get_remote(self, architecture: str, release: str):
        return self.remote_structure.format(release, architecture)
