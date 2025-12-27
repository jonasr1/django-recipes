from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):  # type: ignore[misc]
    location = ""
    file_overwrite = False
