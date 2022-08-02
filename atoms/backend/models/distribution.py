class AtomDistribution:
    distribution_id: str
    name: str
    logo: str
    remote_structure: str
    architectures: list

    def __init__(
        self, 
        distribution_id: str, 
        name: str, 
        logo: str, 
        releases: list,
        remote_structure: str, 
        architectures: list
    ):
        self.distribution_id = distribution_id
        self.name = name
        self.logo = logo
        self.releases = releases
        self.remote_structure = remote_structure
        self.architectures = architectures

    def __str__(self):
        return f"Distribution {self.name}"
    
    def get_remote(self, architecture: str, release: str):
        return self.remote_structure.format(release, architecture)
