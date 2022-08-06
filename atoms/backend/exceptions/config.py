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

from atoms.backend.exceptions.exception import AtomsException


class AtomsCantMakeAtomsPath(AtomsException):
    """
    Exception raised when it is not possible to create the atoms path
    due to a permission error.
    """

    def __init__(self, path: str):
        super().__init__("Atoms can't make the atoms path due to missing permissions: {}".format(path))


class AtomsConfigKeyNotFound(AtomsException):
    """
    Exception raised when a config key is not found.
    """

    def __init__(self, key: str):
        super().__init__("Requested Atoms config key not found: {}.\n\t\
You can't create new config keys in a managed Atoms configuration.".format(key))
