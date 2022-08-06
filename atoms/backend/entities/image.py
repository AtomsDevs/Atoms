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
import tarfile

from atoms.backend.utils.file import FileUtils


class AtomImage:
    name: str
    path: str
    root: str
    size: int

    def __init__(
        self,
        name: str,
        path: str,
        root: str,
    ):
        self.name = name
        self.path = path
        self.root = root

    def unpack(self, destination: str):
        if not os.path.exists(destination):
            os.makedirs(destination)

        with tarfile.open(self.path) as tar:
            if self.root != "":
                tar.extractall(destination, [self.root])
            else:
                tar.extractall(destination)

    def destroy(self):
        os.remove(self.path)
        
    @property
    def size(self):
        return os.path.getsize(self.path)
    
    @property
    def human_size(self):
        return FileUtils.get_human_size(self.size)
