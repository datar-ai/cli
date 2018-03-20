# pylint: disable=E1101
from operator import itemgetter

from .. import cp
from .helpers import MinioClientMock, MinioObject

class TestGatherRemoteFiles(object):
    def test_no_bucket(self, mocker):
        mock_minio_client(mocker, {
            "bucket1": [MinioObject('file.csv')],
            "bucket2": [MinioObject('file.csv')]
        })
        uri = 'data://'
        files = cp.gather_remote_files(uri)
        files = sorted([(file.uri, file.relpath) for file in files], key=itemgetter(1))
        assert len(files) == 2
        assert files == [
            (uri + 'bucket1/file.csv', 'bucket1/file.csv'),
            (uri + 'bucket2/file.csv', 'bucket2/file.csv')
        ]

    def test_bucket_only(self, mocker):
        mock_minio_client(mocker, {
            "bucket": [MinioObject('file.csv')]
        })
        uri = 'data://bucket'
        files = cp.gather_remote_files(uri)
        files = [file for file in files]
        assert len(files) == 1
        assert files[0].uri == uri + '/file.csv'
        assert files[0].relpath == 'file.csv'

    def test_single_file(self, mocker):
        mock_minio_client(mocker, {
            "bucket": [MinioObject('file.csv', size=10)]
        })
        uri = 'data://bucket/file.csv'
        files = cp.gather_remote_files(uri)
        files = [file for file in files]
        assert len(files) == 1
        assert files[0].uri == uri
        assert files[0].relpath == 'file.csv'
        assert files[0].size == 10
    
    def test_single_file_with_path(self, mocker):
        mock_minio_client(mocker, {
            "bucket": [MinioObject('path/file.csv', size=10)]
        })
        uri = 'data://bucket/path/file.csv'
        files = cp.gather_remote_files(uri)
        files = [file for file in files]
        assert len(files) == 1
        assert files[0].uri == uri
        assert files[0].relpath == 'file.csv'
        assert files[0].size == 10
    
    def test_multiple_files_with_same_prefix_in_name(self, mocker):
        mock_minio_client(mocker, {
            "bucket": [
                MinioObject('path/file.csv'),
                MinioObject('path/file.csvv')
            ]
        })
        uri = 'data://bucket/path/file.csv'
        files = cp.gather_remote_files(uri)
        files = [file for file in files]
        assert len(files) == 1
        assert files[0].uri == uri

    def test_single_path(self, mocker):
        mock_minio_client(mocker, {
            "bucket": [
                MinioObject(name='path/path2/file.csv'),
                MinioObject(name='path/file2.csv')
            ]
        })
        uris = ['data://bucket/path', 'data://bucket/path/']
        for uri in uris:
            files = cp.gather_remote_files(uri)
            files = [file for file in files]
            assert len(files) == 2
            assert files[0].relpath == 'path2/file.csv'
            assert files[1].relpath == 'file2.csv'
    
    def test_multiple_paths_with_same_prefix(self, mocker):
        mock_minio_client(mocker, {
            "bucket": [
                MinioObject('path/file.csv'),
                MinioObject('path2/file2.csv')
            ]
        })
        uris = ['data://bucket/path', 'data://bucket/path/']
        for uri in uris:
            files = cp.gather_remote_files(uri)
            files = [file for file in files]
            assert len(files) == 1
            assert files[0].relpath == 'file.csv'


def mock_minio_client(mocker, objects_by_bucket):
    mocker.patch('riseml.commands.data.cp.util.get_minio_client')
    cp.util.get_minio_client.return_value = MinioClientMock(mocker, objects_by_bucket)
