# atom.py
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
import uuid
import orjson
import datetime
from gi.repository import GLib

from atoms.backend.exceptions.atom import AtomsWrongAtomData
from atoms.backend.utils.paths import AtomsPathsUtils
from atoms.backend.utils.image import AtomsImageUtils
from atoms.backend.utils.distribution import AtomsDistributionsUtils
from atoms.backend.wrappers.proot import ProotWrapper


class Atom:
    name: str
    distribution_id: str
    creation_date: str
    upate_date: str
    relative_path: str

    def __init__(
        self, 
        config: "AtomsConfig", 
        name: str, 
        distribution_id: str, 
        relative_path: str,
        creation_date: str, 
        update_date: str=None
    ):
        if update_date is None:
            update_date = creation_date

        self._config = config
        self.name = name
        self.distribution_id = distribution_id
        self.relative_path = relative_path
        self.creation_date = creation_date
        self.update_date = update_date
        self.__proot_wrapper = ProotWrapper()

    @classmethod
    def from_dict(cls, config: "AtomsConfig", data: dict):
        if None in [
            data.get("name"),
            data.get("distributionId"),
            data.get("creationDate"),
            data.get("updateDate"),
            data.get("relativePath")
        ]:
            raise AtomsWrongAtomData(data)
        return cls(
            config,
            data['name'],
            data['distributionId'],
            data['relativePath'],
            data['creationDate'],
            data['updateDate']
        )
    
    @classmethod
    def load(cls, config: "AtomsConfig", relative_path: str):
        path = os.path.join(AtomsPathsUtils.get_atom_path(config, relative_path), "atom.json")
        with open(path, "r") as f:
            data = orjson.loads(f.read())
        return cls.from_dict(config, data)

    @classmethod
    def new(
        cls, 
        config: 'AtomConfig', 
        name: str, 
        distribution: 'AtomDistribution', 
        architecture: str, 
        release: str, 
        download_fn: callable,
        config_fn: callable,
        unpack_fn: callable,
        finalizing_fn: callable
    ):
        date = datetime.datetime.now().isoformat()
        image = AtomsImageUtils.get_image(config, distribution, architecture, release, download_fn)

        GLib.idle_add(config_fn, 0)
        relative_path = str(uuid.uuid4()) + ".atom"
        atom_path = AtomsPathsUtils.get_atom_path(config, relative_path)
        chroot_path = os.path.join(atom_path, "chroot")
        atom = cls(config, name, distribution.distribution_id, relative_path, date)
        os.makedirs(chroot_path)
        GLib.idle_add(config_fn, 1)

        GLib.idle_add(unpack_fn, 0)
        image.unpack(chroot_path)
        GLib.idle_add(unpack_fn, 1)

        GLib.idle_add(finalizing_fn, 0)
        atom.save()
        GLib.idle_add(finalizing_fn, 1)

        return atom

    def to_dict(self):
        return {
            "name": self.name,
            "distributionId": self.distribution_id,
            "relativePath": self.relative_path,
            "creationDate": self.creation_date,
            "updateDate": self.update_date
        }
    
    def save(self):
        path = os.path.join(self.path, "atom.json")
        with open(path, "wb") as f:
            f.write(orjson.dumps(self.to_dict(), f, option=orjson.OPT_NON_STR_KEYS))
    
    def generate_command(self, command: list, environment: list=None) -> tuple:
        if environment is None:
            environment = []

        _command = self.__proot_wrapper.get_proot_command_for_chroot(self.fs_path, command)
        return _command, environment, self.root_path
    
    @property
    def path(self):
        return AtomsPathsUtils.get_atom_path(self._config, self.relative_path)
    
    @property
    def fs_path(self):
        return os.path.join(
            AtomsPathsUtils.get_atom_path(self._config, self.relative_path),
            "chroot"
        )
    
    @property
    def root_path(self):
        return os.path.join(self.fs_path, "root")

    @property
    def distribution(self):
        return AtomsDistributionsUtils.get_distribution(self.distribution_id)
    
    @property
    def enter_command(self):
        return self.generate_command([])
            
    def __str__(self):
        return f"Atom: {self.name}"
