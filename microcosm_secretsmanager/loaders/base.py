from boto3 import Session

class SecretsManagerLoader:
    def __init__(self,
                 environment=None,
                 profile_name=None,
                 region=None):

        self.environment = environment
        self.profile_name = profile_name
        self.region = region

    def __call__(self, metadata, version=None):
        service = metadata if isinstance(metadata, str) else metadata.name
        client = self._client(service)
        return {}
        print(service)

    def items(self, service, version=None):
        pass

    def keyname(self, service):
        return f"secrets/{self.environment}/{service}"

    def _client(self, service):
        session = Session(profile_name=self.profile_name)
        return session.client("secretsmanager")
