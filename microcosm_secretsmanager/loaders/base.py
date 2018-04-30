from boto3 import Session

class SecretsManagerLoader:
    def __init__(self,
                 prefix=None,
                 profile_name=None,
                 region=None):

        self.prefix = prefix
        self.profile_name = profile_name
        self.region = region

    def __call__(self, metadata, version=None):
        service = metadata if isinstance(metadata, str) else metadata.name
        print(service)

    def items(self, service, version=None):
        pass

    def _client(self, service):
        session = Session(profile_name=self.profile_name)
        return session.client("secretsmanager")
