# pylint: disable=E1101
from .. import cp


class TestGatherRemoteFiles(object):
    def test_no_bucket(self, mocker):
        mock_minio_list_buckets(mocker, ['bucket1', 'bucket2'])
        mock_minio_list_objects(mocker, [
            minio_obj(mocker, name='file.csv'),
        ])
        uri = 'data://'
        files = cp.gather_remote_files(uri)
        files = [file for file in files]
        assert len(files) == 2
        assert files[0].uri == uri + 'bucket1/file.csv'
        assert files[1].uri == uri + 'bucket2/file.csv'
    
    def test_bucket_only(self, mocker):
        mock_minio_list_objects(mocker, [
            minio_obj(mocker, name='file.csv')
        ])
        uri = 'data://bucket'
        files = cp.gather_remote_files(uri)
        files = [file for file in files]
        assert len(files) == 1
        assert files[0].uri == uri + '/file.csv'
        assert files[0].relpath == 'file.csv'

    def test_single_file(self, mocker):
        mock_minio_list_objects(mocker, [
            minio_obj(mocker, name='file.csv', size=10)
        ])
        uri = 'data://bucket/file.csv'
        files = cp.gather_remote_files(uri)
        files = [file for file in files]
        assert len(files) == 1
        assert files[0].uri == uri
        assert files[0].relpath == 'file.csv'
        assert files[0].size == 10
    
    def test_single_file_with_path(self, mocker):
        mock_minio_list_objects(mocker, [
            minio_obj(mocker, name='path/file.csv', size=10)
        ])
        uri = 'data://bucket/path/file.csv'
        files = cp.gather_remote_files(uri)
        files = [file for file in files]
        assert len(files) == 1
        assert files[0].uri == uri
        assert files[0].relpath == 'file.csv'
        assert files[0].size == 10
    
    def test_multiple_files_with_same_prefix_in_name(self, mocker):
        mock_minio_list_objects(mocker, [
            minio_obj(mocker, name='path/file.csv'),
            minio_obj(mocker, name='path/file.csvv')
        ])
        uri = 'data://bucket/path/file.csv'
        files = cp.gather_remote_files(uri)
        files = [file for file in files]
        assert len(files) == 1
        assert files[0].uri == uri
    
    def test_single_path(self, mocker):
        mock_minio_list_objects(mocker, [
            minio_obj(mocker, name='path/path2/file.csv'),
            minio_obj(mocker, name='path/file2.csv')
        ])
        uris = ['data://bucket/path', 'data://bucket/path/']
        for uri in uris:
            files = cp.gather_remote_files(uri)
            files = [file for file in files]
            assert len(files) == 2
            assert files[0].relpath == 'path2/file.csv'
            assert files[1].relpath == 'file2.csv'
    
    def test_multiple_paths_with_same_prefix(self, mocker):
        mock_minio_list_objects(mocker, [
            minio_obj(mocker, name='path/file.csv'),
            minio_obj(mocker, name='path2/file2.csv')
        ])
        uris = ['data://bucket/path', 'data://bucket/path/']
        for uri in uris:
            files = cp.gather_remote_files(uri)
            files = [file for file in files]
            assert len(files) == 1
            assert files[0].relpath == 'file.csv'


def patch_minio_client(mocker):
    if not isinstance(cp.util.get_minio_client, mocker.Mock):
        mocker.patch('riseml.commands.data.cp.util.get_minio_client')

def mock_minio_list_buckets(mocker, buckets):
    patch_minio_client(mocker)
    cp.util.get_minio_client.return_value.list_buckets.return_value = buckets        
    
def mock_minio_list_objects(mocker, objects):
    patch_minio_client(mocker)
    cp.util.get_minio_client.return_value.list_objects.return_value = objects

def minio_obj(mocker, name, size=10):
    mock = mocker.Mock()
    mock.object_name = name
    mock.size = size
    return mock