import shutil
import subprocess

from atoms.backend.exceptions.common import AtomsNoBinaryFound


class ProotWrapper:

    def __init__(self):
        self.__binary_path = self.__find_binary_path()
    
    def __find_binary_path(self):
        res = shutil.which("proot")
        if res is None:
            raise AtomsNoBinaryFound("proot")
        return res
    
    def get_proot_command_for_chroot(self, chroot_path: str, command: list = None, working_directory: str = None):
        if command is None:
            command = []

        if working_directory is None:
            working_directory = "/"

        return [
            self.__binary_path,
            "-0",
            "-w",
            working_directory,
            "-r",
            chroot_path
        ] + command
    