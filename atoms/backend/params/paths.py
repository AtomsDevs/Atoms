# paths.py
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
from pathlib import Path


class AtomsPaths:
    xdg_data_home = os.environ.get("XDG_DATA_HOME", os.path.join(Path.home(), ".local/share"))
    app_data = os.path.join(xdg_data_home, "atoms")

    atoms = os.path.join(app_data, "atoms")
    images = os.path.join(app_data, "images")
    config_file = os.path.join(app_data, "config.json")
    