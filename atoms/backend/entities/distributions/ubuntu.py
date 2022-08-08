from atoms.backend.entities.distribution import AtomDistribution


class Ubuntu(AtomDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="ubuntu", 
            name="Ubuntu", 
            logo="ubuntu-symbolic",
            releases=["22.04", "20.04"],
            remote_structure="http://cdimage.ubuntu.com/ubuntu-base/releases/{0}/release/ubuntu-base-{0}-base-{1}.tar.gz",
            remote_hash_structure="http://cdimage.ubuntu.com/ubuntu-base/releases/{0}/release/SHA256SUMS",
            remote_hash_type="sha256",
            architectures={"x86_64": "amd64"},
            root="",
            container_image_name="ubuntu"
        )
    
    def get_remote_hash(self, _, release: str) -> str:
        return self.remote_hash_structure.format(release)
