from json import dumps, loads
from json.decoder import JSONDecodeError

from boto3 import Session
from botocore.exceptions import ClientError

from microcosm_logging.decorators import logger

@logger
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
        return self.get_secret_value(service, version)


    def get_secret_value(self, service, version=None):
        keyname = self.keyname(service)
        client = self._client(service)

        get_args = dict(
            SecretId=keyname,
        )

        if version:
            get_args.update(
                VersionStage=version,
            )

        try:
            response = client.get_secret_value(
                **get_args,
            )

        except ClientError as e:
            self.logger.error(f"Error from Amazon retrieving the secrets for: {keyname}, most likely resource does not exist")
            return {}
        else:
            if "SecretString" in response:
                try:
                    # It's not always valid json.
                    # We initialize with valid JSON but Amazon might send None
                    return loads(response["SecretString"]).get("config", {})
                except JSONDecodeError as e:
                    self.logger.error(
                            f"Error parsing secrets for: {keyname}, version: {version}"
                    )
                    return {}

    def keyname(self, service):
        return f"secrets/{self.environment}/{service}"

    def _client(self, service):
        session = Session(profile_name=self.profile_name)
        return session.client("secretsmanager")
