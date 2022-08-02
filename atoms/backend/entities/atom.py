import os
import orjson

from atoms.backend.exceptions.atom import AtomsWrongAtomData
from atoms.backend.utils.paths import AtomPathsUtils
from atoms.backend.utils.distribution import AtomsDistributionsUtils


class Atom:
    name: str
    distribution_id: str
    creation_date: str
    upate_date: str
    relative_path: str

    def __init__(self, config: "AtomsConfig", name: str, distribution_id: str, creation_date: str, update_date: str, relative_path: str):
        self._config = config
        self.name = name
        self.distribution_id = distribution_id
        self.creation_date = creation_date
        self.update_date = update_date
        self.relative_path = relative_path

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
            data['creationDate'],
            data['updateDate'],
            data['relativePath']
        )
    
    @classmethod
    def load(cls, config: "AtomsConfig", relative_path: str):
        path = os.path.join(AtomPathsUtils.get_atom_path(config, relative_path), "atom.json")
        with open(path, "r") as f:
            data = orjson.loads(f.read())
        return cls.from_dict(config, data)

    @classmethod
    def new(cls, name: str):
        return cls(
            name,
            datetime.datetime.now().isoformat(),
            datetime.datetime.now().isoformat()
        )

    def to_dict(self):
        return {
            "name": self.name,
            "distributionId": self.distribution_id,
            "creationDate": self.creation_date,
            "updateDate": self.update_date,
            "relativePath": self.relative_path
        }
    
    def save(self):
        path = os.path.join(self.path, "atom.json")
        with open(path, "wb") as f:
            f.write(orjson.dumps(self.to_dict(), f, option=orjson.OPT_NON_STR_KEYS))
    
    @property
    def path(self):
        return AtomPathsUtils.get_atom_path(self._config, self.relative_path)

    @property
    def distribution(self):
        return AtomsDistributionsUtils.get_distribution(self.distribution_id)
            
    def __str__(self):
        return f"Atom: {self.name}"
