# download.py
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


class AtomsHashMissmatchError(AtomsException):
    """
    Exception raised when the hash of a downloaded file is not the same as the one in the distribution file.
    """

    def __init__(self):
        super().__init__("The hash of the downloaded file is not the same as the one in the distribution file.")
