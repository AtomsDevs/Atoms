import os


class AtomPathsUtils:

    @staticmethod
    def get_atom_path(config: "AtomsConfig", relative_path: str) -> str:
        return os.path.join(config.atoms_path, relative_path)
