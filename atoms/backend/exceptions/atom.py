# atom.py
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


class AtomsWrongAtomData(AtomsException):
    """
    Exception raised when the atom data is wrong.
    """

    def __init__(self, data: dict):
        super().__init__("Wrong atom data: {}".format(str(data)))


class AtomsCannotSavePodmanContainers(AtomsException):
    """
    Exception raised when the save method is asked for a podman container
    """

    def __init__(self, data: dict):
        super().__init__("Atoms cannot save podman containers configurations: {}".format(str(data)))


class AtomsCannotRenamePodmanContainers(AtomsException):
    """
    Exception raised when the rename method is asked for a podman container
    """

    def __init__(self, data: dict):
        super().__init__("Atoms cannot rename podman containers: {}".format(str(data)))