from atoms.backend.entities.distribution import AtomDistribution


class AlpineLinux(AtomDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="alpinelinux", 
            name="Alpine Linux",
            logo="alpine-linux-symbolic",
            releases=["3.16.1", "3.16.0"],
            remote_structure="https://dl-cdn.alpinelinux.org/alpine/v{0}/releases/{1}/alpine-minirootfs-{2}-{1}.tar.gz",
            remote_hash_structure="https://dl-cdn.alpinelinux.org/alpine/v{0}/releases/{1}/alpine-minirootfs-{2}-{1}.tar.gz.sha256",
            remote_hash_type="sha256",
            architectures={"x86_64": "x86_64"},
            root="",
            container_image_name="alpine"
        )
    
    def get_remote(self, architecture: str, release: str) -> str:
        return self.remote_structure.format(
            '.'.join(release.split('.')[:2]), # only take major and minor version
            architecture, 
            release
        )
    
    def get_remote_hash(self, architecture: str, release: str) -> str:
        return self.remote_hash_structure.format(
            '.'.join(release.split('.')[:2]), # only take major and minor version
            architecture, 
            release
        )
