from collections import namedtuple

from microcosm.metadata import Metadata
from hamcrest import (
    assert_that,
    equal_to,
    is_,
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
        self.loader = DummySecretsManagerLoader()
        self.metadata = Metadata("dummy")

    def test_keyname(self):
        self.metadata = Metadata("dummy")
        self.loader = DummySecretsManagerLoader(
            environment="dev"
        )
        keyname = self.loader.keyname("dummy")
        assert_that(keyname, equal_to("secrets/dev/dummy"))

    def test_load_empty_configuration(self):
        with patch.object(self.loader, "_client") as mocked:
            mocked.return_value.scan.return_value = dict(
                Items=[],
            )

            assert_that(self.loader(self.metadata), is_(equal_to(dict())))

        mocked.assert_called_with(self.metadata.name)
        mocked.return_value.scan.assert_called()
        assert_that(True, equal_to(False))

