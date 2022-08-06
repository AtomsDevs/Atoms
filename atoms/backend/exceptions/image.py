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

from atoms.backend.exceptions.exception import AtomsException


class AtomsFailToDownloadImage(AtomsException):
    """
    Exception raised when an image cannot be downloaded from its remote.
    """

    def __init__(self, remote: str):
        super().__init__("Failed to download image from remote: {}".format(remote))


class AtomsImageMissingRoot(AtomsException):
    """
    Exception raised when an image has no root.
    """

    def __init__(self, image: str):
        super().__init__("Image {} has no root".format(image))
