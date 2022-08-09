class AtomsInstance:
    config: 'AtomsConfig'
    client_bridge: 'ClientBridge'

    def __init__(self, config: 'AtomsConfig', client_bridge: 'ClientBridge'):
        self.config = config
        self.client_bridge = client_bridge
        