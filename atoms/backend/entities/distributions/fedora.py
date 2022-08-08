from atoms.backend.entities.distribution import AtomDistribution


class Fedora(AtomDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="fedora", 
            name="Fedora",
            logo="fedora-symbolic",
            releases=["36"],
            remote_structure="https://github.com/mirkobrombin/linux-rootfs-images/releases/download/fedora-{0}/Fedora-Container-Base-{0}.{1}.tar",
            remote_hash_structure="https://github.com/mirkobrombin/linux-rootfs-images/releases/download/fedora-{0}/SHA1SUMS",
            remote_hash_type="sha1",
            architectures={"x86_64": "x86_64"},
            root="",
            container_image_name="fedora"
        )
    
    def get_remote_hash(self, _, release: str) -> str:
        return self.remote_hash_structure.format(release)
