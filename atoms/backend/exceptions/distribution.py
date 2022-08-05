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

from atoms.backend.exceptions.exception import AtomsException


class AtomsUnknownDistribution(AtomsException):
    """
    Exception raised when the distribution id is unknown.
    """

    def __init__(self, distribution_id: str):
        super().__init__("Unknown distribution id: {}".format(distribution_id))


class AtomsUnreachableRemote(AtomsException):
    """
    Exception raised when a remote is unreachable.
    """

    def __init__(self, remote: str):
        super().__init__("Unreachable remote: {}".format(remote))
