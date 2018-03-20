from minio.error import InvalidBucketError, NoSuchBucket

class MinioObject(object):
    def __init__(self, name, size=10):
        self.object_name = name
        self.size = size
        self.is_dir = name.endswith('/')

    def __hash__(self):
        return self.object_name.__hash__()

    def __eq__(self, other):
        if self.object_name == other.object_name:
            return True
        return False

class MinioClientMock(object):
    def __init__(self, mocker, objects_by_bucket):
        self.mocker = mocker
        self.objects_by_bucket = objects_by_bucket

    def list_buckets(self):
        for bucket_name in self.objects_by_bucket:
            bucket = self.mocker.Mock()
            bucket.name = bucket_name
            yield bucket

    def list_objects_v2(self, bucket_name, prefix, recursive=False):
        prefix = prefix or ''
        if len(bucket_name) < 3:
            raise InvalidBucketError(message='')
        if not bucket_name in self.objects_by_bucket:
            raise NoSuchBucket(response_error=self.mocker.Mock())
        objects = self.objects_by_bucket[bucket_name]
        objects = [obj for obj in objects if obj.object_name.startswith(prefix)]
        if not recursive:
            objects = [self._limit_to_path(prefix, obj) for obj in objects]
            objects = list(set(objects))
        for obj in objects:
            yield obj

    def _limit_to_path(self, prefix, obj):
        index = obj.object_name.find('/', len(prefix))
        if index != -1:
            path_name = obj.object_name[:index]
            return MinioObject(path_name.split('/')[-1] + '/')
        else:
            return obj
