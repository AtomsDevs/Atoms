from atoms.backend.entities.distribution import AtomDistribution


class Unknown(AtomDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="unknown", 
            name="Unknown distribution",
            logo="pm.mirko.Atoms-symbolic",
            releases=[],
            remote_structure="",
            remote_hash_structure="",
            remote_hash_type="",
            architectures={},
            root="",
            container_image_name=""
        )
