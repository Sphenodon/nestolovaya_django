from storages.backends.s3boto3 import S3Boto3Storage

from nestolovaya_itmo.settings import AWS_BUCKET_NAME


class CustomStorage(S3Boto3Storage):
    bucket_name = AWS_BUCKET_NAME
    file_overwrite = False
