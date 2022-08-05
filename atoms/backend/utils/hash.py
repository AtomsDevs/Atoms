# file.py
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
import hashlib


class HashUtils:
    
    @staticmethod
    def get_hash(file_path: str, hash_type: str) -> str:
        """
        Get the hash of a file.
        """
        if hash_type == "md5":
            hash_temp = hashlib.md5()
        elif hash_type == "sha256":
            hash_temp = hashlib.sha256()
        elif hash_type == "sha512":
            hash_temp = hashlib.sha512()
        elif hash_type == "sha1":
            hash_temp = hashlib.sha1()
        else:
            raise ValueError("Invalid hash type")

        with open(file_path, "rb") as f:
            while True:
                buffer = f.read(2 ** 20)
                if not buffer:
                    break
                hash_temp.update(buffer)
        return hash_temp.hexdigest()
