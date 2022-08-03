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
    
    def get_proot_command_for_chroot(self, chroot_path: str, command: list = None):
        if command is None:
            command = []

        return [
            self.__binary_path,
            "-0",
            "-r",
            chroot_path
        ] + command
    