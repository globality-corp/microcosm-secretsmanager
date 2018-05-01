from json import dumps
from json.decoder import JSONDecodeError

from collections import namedtuple

from microcosm.metadata import Metadata
from hamcrest import (
    assert_that,
    calling,
    equal_to,
    is_,
    raises,
)
from mock import patch

from microcosm_secretsmanager.loaders.base import SecretsManagerLoader


DummyValue = namedtuple("TestValue", "dummy")


class DummySecretsManagerLoader(SecretsManagerLoader):

    @property
    def value_type(self):
        return DummyValue

    def decode(self, value):
        return value.dummy

    def encode(self, value):
        return self.value_type(value)


class TestSecretsManagerLoader:

    def setup(self):
        self.loader = DummySecretsManagerLoader(environment="dev")
        self.metadata = Metadata("dummy")

    def test_keyname(self):
        self.metadata = Metadata("dummy")
        self.loader = DummySecretsManagerLoader(
            environment="dev"
        )
        keyname = self.loader.keyname("dummy")
        assert_that(keyname, equal_to("secrets/dev/dummy"))

    def test_load_empty_configuration(self):
        with patch.object(self.loader, "make_client") as mocked:
            mocked.return_value.get_secret_value.return_value = dict(
                SecretString="{}",
            )

            assert_that(self.loader(self.metadata), is_(equal_to(dict())))

        mocked.assert_called_with(self.metadata.name)
        mocked.return_value.get_secret_value.assert_called_with(
            SecretId="secrets/dev/dummy",
        )

    def test_load_nested_configuration(self):
        with patch.object(self.loader, "make_client") as mocked:
            mocked.return_value.get_secret_value.return_value = dict(
                SecretString=dumps(dict(
                    version="FAKE",
                    config=dict(
                        postgres=dict(
                            password="fake",
                        ),
                    )
                )),
            )

            assert_that(self.loader(self.metadata)["postgres"]["password"], is_(equal_to("fake")))

        mocked.assert_called_with(self.metadata.name)
        mocked.return_value.get_secret_value.assert_called_with(
            SecretId="secrets/dev/dummy",
        )

    def test_load_wrong_configuration(self):
        with patch.object(self.loader, "make_client") as mocked:
            mocked.return_value.get_secret_value.return_value = dict(
                SecretString=dumps(dict(
                    version="FAKE",
                    wrong_config_key=dict(
                        postgres=dict(
                            password="fake",
                        ),
                    )
                )),
            )

            assert_that(self.loader(self.metadata), is_(equal_to(dict())))

        mocked.assert_called_with(self.metadata.name)
        mocked.return_value.get_secret_value.assert_called_with(
            SecretId="secrets/dev/dummy",
        )

    def test_load_not_json(self):
        with patch.object(self.loader, "make_client") as mocked:
            mocked.return_value.get_secret_value.return_value = dict(
                SecretString="NotJson",
            )

            assert_that(calling(self.loader).with_args(self.metadata), raises(JSONDecodeError))

        mocked.assert_called_with(self.metadata.name)
        mocked.return_value.get_secret_value.assert_called_with(
            SecretId="secrets/dev/dummy",
        )
