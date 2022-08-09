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
import time
import logging
import requests

from atoms.backend.utils.file import FileUtils
from atoms.backend.utils.hash import HashUtils
from atoms.backend.exceptions.download import AtomsHashMissmatchError


logger = logging.getLogger("atoms.download")


class DownloadUtils:
    """
    Download a resource from a given URL. It shows and update a progress
    bar while downloading but can also be used to update external progress
    bars using the func parameter.
    """

    def __init__(
        self, 
        instance: "AtomsInstance",
        url: str, 
        file: str, 
        func: callable = None, 
        hash_value: str = None, 
        hash_type: str = None
    ):
        self.__instance = instance
        self.start_time = None
        self.url = url
        self.file = file
        self.func = func
        self.hash_value = hash_value
        self.hash_type = hash_type

    def download(self) -> bool:
        """Start the download."""
        try:
            with open(self.file, "wb") as file:
                self.start_time = time.time()
                headers = {"User-Agent": "curl/7.79.1"}
                response = requests.get(self.url, stream=True, headers=headers)
                total_size = int(response.headers.get("content-length", 0))
                block_size = 1024
                count = 0

                if total_size != 0:
                    for data in response.iter_content(block_size):
                        file.write(data)
                        count += 1
                        if self.func:
                            self.__instance.client_bridge.exec_on_main(
                                self.func,
                                count,
                                block_size,
                                total_size
                            )
                            self.__progress(count, block_size, total_size)
                else:
                    file.write(response.content)
                    if self.func is not None:
                        self.__instance.client_bridge.exec_on_main(self.func, 1, 1, 1)
                        self.__progress(1, 1, 1)
        except requests.exceptions.SSLError:
            logger.error("Download failed due to a SSL error. Your system may have a wrong date/time or wrong certificates.")
            return False
        except (requests.exceptions.RequestException, OSError):
            logger.error("Download failed! Check your internet connection.")
            return False

        if None not in [self.hash_value, self.hash_type]:
            _hash = HashUtils.get_hash(self.file, self.hash_type)
            if _hash != self.hash_value:
                logger.error(f"Download failed! The downloaded file is corrupted.\n\tExpected {self.hash_value} got {_hash}.")
                raise AtomsHashMissmatchError()
        return True

    def __progress(self, count, block_size, total_size):
        """Update the progress bar."""
        percent = int(count * block_size * 100 / total_size)
        done_str = FileUtils.get_human_size(count * block_size)
        total_str = FileUtils.get_human_size(total_size)
        speed_str = FileUtils.get_human_size(count * block_size / (time.time() - self.start_time))
        name = self.file.split("/")[-1]
        c_close, c_complete, c_incomplete = "\033[0m", "\033[92m", "\033[90m"
        print(
            f"\r{c_incomplete if percent < 100 else c_complete}{name} ({percent}%) \
{'━' * int(percent / 2)} ({done_str}/{total_str} - {speed_str})",
            end=""
        )
        if percent == 100:
            print(f"{c_close}\n")
