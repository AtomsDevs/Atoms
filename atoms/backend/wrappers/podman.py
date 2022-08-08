# podman.py
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
import shutil
import subprocess


class PodmanWrapper:

    def __init__(self):
        self.__is_flatpak = "FLATPAK_ID" in os.environ
        self.__binary_path = self.__find_binary_path()


    def __find_binary_path(self) -> str:
        if self.__is_flatpak:
            try:
                proc = subprocess.check_output(self.__get_flatpak_command(["which", "podman"]))
                return proc.decode("utf-8").strip()
            except FileNotFoundError:
                return

        return shutil.which("podman")
    
    def get_containers(self) -> list:
        containers = {}
        command = [self.__binary_path, "ps", "-a", "--format", 
                    "{{.ID}}+|+{{.Image}}+|+{{.Names}}+|+{{.CreatedAt}}"]

        if self.__is_flatpak:
            command = self.__get_flatpak_command(command)
            
        proc = subprocess.check_output(command)
        lines = proc.decode("utf-8").strip().split("\n")

        for line in lines:
            _id, _image, _names, _created_at = line.split("+|+")
            containers[_id] = {
                "image": _image, 
                "names": _names,
                "creation_date": _created_at
            }

        return containers

    def get_podman_command_for_container(
        self, 
        container_id: str, 
        command: list = None, 
        working_directory: str = None
    ) -> list:
        self.__start_container(container_id)

        if command is None or len(command) == 0:
            command = ["sh"]

        command = [
            self.__binary_path,
            "exec",
            "-i",
            "-t",
            container_id,
        ] + command

        if self.__is_flatpak:
            command = self.__get_flatpak_command(command)

        return command
    
    def __start_container(self, container_id: str):
        command = [self.__binary_path, "start", container_id]

        if self.__is_flatpak:
            command = self.__get_flatpak_command(command)

        subprocess.check_call(command)
    
    def destroy_container(self, container_id: str):
        command = [self.__binary_path, "rm", "-f", container_id]

        if self.__is_flatpak:
            command = self.__get_flatpak_command(command)

        subprocess.check_call(command)
    
    def stop_container(self, container_id: str):
        command = [self.__binary_path, "kill", container_id]

        if self.__is_flatpak:
            command = self.__get_flatpak_command(command)

        try:
            subprocess.check_call(command)
        except subprocess.CalledProcessError:
            pass
    
    def __get_flatpak_command(self, command: list) -> list:
        binary_path = shutil.which("flatpak-spawn")
        return [binary_path, "--host"] + command
        
    @property
    def is_supported(self) -> bool:
        return self.__binary_path is not None
