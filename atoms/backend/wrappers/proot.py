# proot.py
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

import shutil
import subprocess

from atoms.backend.exceptions.common import AtomsNoBinaryFound


class ProotWrapper:

    def __init__(self):
        self.__binary_path = self.__find_binary_path()
    
    def __find_binary_path(self) -> str:
        res = shutil.which("proot")
        if res is None:
            raise AtomsNoBinaryFound("proot")
        return res
    
    def get_proot_command_for_chroot(
        self, 
        chroot_path: str, 
        command: list = None, 
        working_directory: str = None
    ) -> list:
        if command is None:
            command = []

        if working_directory is None:
            working_directory = "/"
        
        env_bin = shutil.which("env")

        return [
            env_bin,
            "-i",
            "HOME=/root",
            "HOSTNAME=atom",
            self.__binary_path,
            "-0",
            "-w",
            working_directory,
            "-r",
            chroot_path
        ] + command
    