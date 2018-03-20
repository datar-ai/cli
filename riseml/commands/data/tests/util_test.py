# pylint: disable=E1101
from .. import util
from .helpers import MinioClientMock, MinioObject

class TestIsRemoteDir(object):
    def test_root_is_always_dir(self, mocker):
        mock_minio_client(mocker, {})
        assert util.is_remote_dir('data://') is True

    def test_main_path_is_always_dir(self, mocker):
        mock_minio_client(mocker, {})
        for uri in ['data://bucket', 'data://bucket/']:
            assert util.is_remote_dir(uri) is True

    def test_missing_bucket_results_in_no_dir(self, mocker):
        mock_minio_client(mocker, {})
        assert util.is_remote_dir('data://test/path') is False

    def test_path_is_a_file(self, mocker):
        mock_minio_client(mocker, {
            "test": [MinioObject('path')]
        })
        assert util.is_remote_dir('data://test/path') is False

    def test_path_is_a_dir(self, mocker):
        mock_minio_client(mocker, {
            "test": [MinioObject('path/file.csv')]
        })
        assert util.is_remote_dir('data://test/path') is True


def mock_minio_client(mocker, objects_by_bucket):
    mocker.patch('riseml.commands.data.util.get_minio_client')
    util.get_minio_client.return_value = MinioClientMock(mocker, objects_by_bucket)
