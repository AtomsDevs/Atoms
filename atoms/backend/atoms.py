import os

from atoms.backend.entities.config import AtomsConfig
from atoms.backend.entities.atom import Atom


class AtomsBackend:
    __atoms: dict
    config: AtomsConfig

    def __init__(self):
        self.config = AtomsConfig()
        self.__atoms = self.__list_atoms()
        
    def __list_atoms(self) -> dict:
        atoms = {}
        for atom in os.listdir(self.config.atoms_path):
            if atom.endswith(".atom"):
                atoms[atom] = Atom.load(self.config, atom)
        return atoms

    @property
    def atoms(self) -> dict:
        return self.__atoms

    @property
    def has_atoms(self) -> bool:
        return len(self.__atoms) > 0
