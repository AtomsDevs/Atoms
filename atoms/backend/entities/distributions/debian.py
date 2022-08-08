from atoms.backend.entities.distribution import AtomDistribution


class Debian(AtomDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="debian", 
            name="Debian",
            logo="debian-symbolic",
            releases=["11",],
            remote_structure="https://cloud.debian.org/images/cloud/bullseye/latest/debian-{0}-genericcloud-{1}.tar.xz",
            remote_hash_structure="https://cloud.debian.org/images/cloud/bullseye/latest/SHA512SUMS",
            remote_hash_type="sha512",
            architectures={"x86_64": "amd64"},
            root="",
            container_image_name="debian"
        )
