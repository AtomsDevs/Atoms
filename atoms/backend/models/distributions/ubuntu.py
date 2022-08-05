from atoms.backend.models.distribution import AtomDistribution


class Ubuntu(AtomDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="ubuntu", 
            name="Ubuntu", 
            logo="ubuntu-symbolic",
            releases=["21.04", "22.04"],
            remote_structure="http://cdimage.ubuntu.com/ubuntu-base/releases/{0}/release/ubuntu-base-{0}-base-{1}.tar.gz",
            remote_hash_structure="http://cdimage.ubuntu.com/ubuntu-base/releases/{0}/SHA256SUMS",
            remote_hash_type="sha256",
            architectures={"x86_64": "amd64"}
        )
    
    def get_remote_hash(self, architecture: str, release: str):
        return self.remote_hash_structure.format(release)
