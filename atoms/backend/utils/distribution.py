from atoms.backend.exceptions.distribution import AtomsUnknownDistribution
from atoms.backend.models.distribution import *


class AtomsDistributionsUtils:

    @staticmethod
    def get_distribution(distribution_id: str) -> AtomDistribution:
        if distribution_id == "alpinelinux":
            return AlpineLinux()
        if distribution_id == "ubuntu":
            return Ubuntu()
        if distribution_id == "fedora":
            return Fedora()
            
        raise AtomsUnknownDistribution(distribution_id)
