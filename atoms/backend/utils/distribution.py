from atoms.backend.exceptions.distribution import AtomsUnknownDistribution
from atoms.backend.models.distribution import AtomDistribution
from atoms.backend.models.distributions import *


class AtomsDistributionsUtils:

    @staticmethod
    def get_distribution(distribution_id: str) -> AtomDistribution:
        if distribution_id == "alpinelinux":
            return AlpineLinux()
        if distribution_id == "ubuntu":
            return Ubuntu()
        # TODO: the following distributions are not yet implemented 
        # if distribution_id == "fedora":
        #     return Fedora()
        # if distribution_id == "debian":
        #     return Debian()
            
        raise AtomsUnknownDistribution(distribution_id)
    
    @staticmethod
    def get_distributions() -> dict:
        return [
            AlpineLinux(),
            Ubuntu()
        ]
