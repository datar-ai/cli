# pylint: disable=E1101
from minio.error import NoSuchBucket, NoSuchKey, ResponseError

from .. import util


class TestIsRemoteDir(object):
    def test_root_is_always_dir(self):
        result = util.is_remote_dir('data://')
        assert result == True
        
    def test_main_path_is_always_dir(self):
        for uri in ['data://bucket', 'data://bucket/']:
            result = util.is_remote_dir(uri)
            assert result == True
    
    def test_missing_bucket_results_in_no_dir(self, mocker):
        get_object = mock_minio_get_object(mocker)
        get_object.side_effect = NoSuchBucket(response_error=mocker.Mock())
        result = util.is_remote_dir('data://test/path')
        assert result == False
        get_object.assert_called_with('test', 'path/')
    
    def test_path_is_not_a_dir(self, mocker):
        get_object = mock_minio_get_object(mocker)
        get_object.side_effect = NoSuchKey(response_error=mocker.Mock())
        result = util.is_remote_dir('data://test/path')
        assert result == False
        get_object.assert_called_with('test', 'path/')
    
    def test_path_is_a_dir(self, mocker):
        get_object = mock_minio_get_object(mocker)
        get_object.return_value = minio_obj(mocker, 'path/')
        result = util.is_remote_dir('data://test/path')
        assert result == True
        get_object.assert_called_with('test', 'path/')


def patch_minio_client(mocker):
    if not isinstance(util.get_minio_client, mocker.Mock):
        mocker.patch('riseml.commands.data.util.get_minio_client')

def mock_minio_get_object(mocker):
    patch_minio_client(mocker)
    return util.get_minio_client.return_value.get_object

def minio_obj(mocker, name, size=10):
    mock = mocker.Mock()
    mock.object_name = name
    mock.size = size
    return mock